#!/usr/bin/env node
/**
 * Kernel Observer Bridge
 * 
 * Connects eBPF tracing events to OpenClaw Gateway via WebSocket.
 * 
 * Usage: sudo node bridge.js
 * 
 * Requires: bpftrace, WebSocket connection to Gateway
 */

const { spawn } = require('child_process');
const WebSocket = require('ws');
const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
    gatewayUrl: 'ws://localhost:18789/kernel-events',
    scriptsDir: path.join(__dirname, 'scripts'),
    logFile: path.join(__dirname, 'events.log'),
    privacyFilters: {
        excludePaths: [
            '/home/csilva/.ssh/',
            '/home/csilva/.gnupg/',
            '/home/csilva/.password-store/',
        ],
        excludeProcesses: [
            'password-manager',
            'keepassxc',
            'gnome-keyring',
        ],
        redactPatterns: [
            { pattern: /password[=:]\S+/gi, replacement: 'password=***' },
            { pattern: /token[=:]\S+/gi, replacement: 'token=***' },
            { pattern: /key[=:]\S+/gi, replacement: 'key=***' },
            { pattern: /secret[=:]\S+/gi, replacement: 'secret=***' },
        ]
    }
};

class KernelObserverBridge {
    constructor() {
        this.ws = null;
        this.bpftraceProcess = null;
        this.eventBuffer = [];
        this.isConnected = false;
    }

    /**
     * Parse bpftrace output line
     */
    parseEvent(line) {
        // Remove ANSI codes
        line = line.replace(/\x1b\[[0-9;]*m/g, '').trim();
        if (!line) return null;

        // Pattern: [CATEGORY]  PID      Process          Event
        // Or: [HH:MM:SS] PID Process action
        
        // Category pattern
        const catMatch = line.match(/\[(\w+)\]\s+(\d+)\s+([\w-]+)\s+(\w+)\s*(.*)/);
        if (catMatch) {
            return {
                timestamp: new Date().toISOString(),
                category: catMatch[1],
                pid: parseInt(catMatch[2]),
                process: catMatch[3],
                event: catMatch[4],
                details: catMatch[5] || '',
                raw: line
            };
        }

        // Time pattern
        const timeMatch = line.match(/\[(\d{2}:\d{2}:\d{2})\]\s+(\d+)\s+([\w-]+)\s+(.*)/);
        if (timeMatch) {
            return {
                timestamp: new Date().toISOString(),
                time: timeMatch[1],
                pid: parseInt(timeMatch[2]),
                process: timeMatch[3],
                action: timeMatch[4],
                raw: line
            };
        }

        // Raw event
        return {
            timestamp: new Date().toISOString(),
            raw: line
        };
    }

    /**
     * Apply privacy filters to event
     */
    applyPrivacyFilters(event) {
        // Exclude sensitive paths
        for (const excludePath of CONFIG.privacyFilters.excludePaths) {
            if (event.raw && event.raw.includes(excludePath)) {
                return null; // Drop event
            }
        }

        // Exclude sensitive processes
        if (CONFIG.privacyFilters.excludeProcesses.includes(event.process)) {
            return null;
        }

        // Redact sensitive patterns
        let details = event.details || event.action || '';
        for (const { pattern, replacement } of CONFIG.privacyFilters.redactPatterns) {
            details = details.replace(pattern, replacement);
        }

        event.details = details;
        return event;
    }

    /**
     * Start WebSocket connection to Gateway
     */
    async connectToGateway() {
        return new Promise((resolve, reject) => {
            try {
                this.ws = new WebSocket(CONFIG.gatewayUrl);
                
                this.ws.on('open', () => {
                    console.log('[Bridge] Connected to Gateway');
                    this.isConnected = true;
                    resolve();
                });

                this.ws.on('error', (error) => {
                    console.error('[Bridge] WebSocket error:', error.message);
                    this.isConnected = false;
                });

                this.ws.on('close', () => {
                    console.log('[Bridge] Disconnected from Gateway');
                    this.isConnected = false;
                });
            } catch (error) {
                reject(error);
            }
        });
    }

    /**
     * Send event to Gateway
     */
    sendEvent(event) {
        if (!this.isConnected || !this.ws) {
            // Buffer if not connected
            this.eventBuffer.push(event);
            if (this.eventBuffer.length > 1000) {
                this.eventBuffer.shift();
            }
            return;
        }

        const message = JSON.stringify({
            type: 'kernel_event',
            timestamp: event.timestamp,
            data: event
        });

        try {
            this.ws.send(message);
        } catch (error) {
            console.error('[Bridge] Failed to send event:', error.message);
            this.eventBuffer.push(event);
        }
    }

    /**
     * Start bpftrace process
     */
    startBpftrace(scriptPath) {
        console.log(`[Bridge] Starting bpftrace: ${scriptPath}`);
        
        this.bpftraceProcess = spawn('bpftrace', ['-f', 'json', scriptPath], {
            stdio: ['ignore', 'pipe', 'pipe']
        });

        this.bpftraceProcess.stdout.on('data', (data) => {
            const lines = data.toString().split('\n');
            for (const line of lines) {
                const event = this.parseEvent(line);
                if (!event) continue;

                // Apply privacy filters
                const filteredEvent = this.applyPrivacyFilters(event);
                if (!filteredEvent) continue;

                // Log to file
                this.logEvent(filteredEvent);

                // Send to Gateway
                this.sendEvent(filteredEvent);

                // Console output
                console.log(`[${filteredEvent.category || 'EVENT'}] ${filteredEvent.process || 'unknown'} (pid:${filteredEvent.pid || 0}) ${filteredEvent.event || filteredEvent.action || ''}`);
            }
        });

        this.bpftraceProcess.stderr.on('data', (data) => {
            console.error(`[bpftrace stderr] ${data.toString()}`);
        });

        this.bpftraceProcess.on('close', (code) => {
            console.log(`[Bridge] bpftrace exited with code ${code}`);
            this.bpftraceProcess = null;
        });

        this.bpftraceProcess.on('error', (error) => {
            console.error(`[Bridge] bpftrace error:`, error);
        });
    }

    /**
     * Log event to file
     */
    logEvent(event) {
        const logLine = JSON.stringify(event) + '\n';
        fs.appendFile(CONFIG.logFile, logLine, (err) => {
            if (err) console.error('[Bridge] Failed to log event:', err.message);
        });
    }

    /**
     * Extract patterns from events
     */
    async extractPatterns() {
        // Read last N events from log
        const events = [];
        const fileStream = fs.createReadStream(CONFIG.logFile, { encoding: 'utf8' });
        const readline = require('readline');
        const rl = readline.createInterface({ input: fileStream });

        let count = 0;
        for await (const line of rl) {
            if (count++ > 10000) break; // Last 10k events
            try {
                events.push(JSON.parse(line));
            } catch {}
        }

        // Count patterns
        const patterns = {};
        for (const event of events) {
            const key = `${event.process}:${event.event || event.action}`;
            patterns[key] = (patterns[key] || 0) + 1;
        }

        // Sort by frequency
        const sorted = Object.entries(patterns)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 50);

        return sorted.map(([pattern, count]) => ({
            pattern,
            frequency: count,
            confidence: count / events.length
        }));
    }

    /**
     * Start the bridge
     */
    async start(scope = 'all') {
        console.log('[Bridge] Starting Kernel Observer Bridge');
        
        // Map scope to script
        const scripts = {
            syscalls: 'syscalls.bt',
            files: 'files.bt',
            network: 'network.bt',
            processes: 'processes.bt',
            all: 'full.bt'
        };

        const scriptFile = scripts[scope] || scripts.all;
        const scriptPath = path.join(CONFIG.scriptsDir, scriptFile);

        // Check if script exists
        if (!fs.existsSync(scriptPath)) {
            throw new Error(`Script not found: ${scriptPath}`);
        }

        // Try to connect to Gateway
        try {
            await this.connectToGateway();
        } catch (error) {
            console.warn('[Bridge] Gateway not available, running in standalone mode');
        }

        // Start bpftrace
        this.startBpftrace(scriptPath);

        // Handle shutdown
        process.on('SIGINT', () => this.stop());
        process.on('SIGTERM', () => this.stop());
    }

    /**
     * Stop the bridge
     */
    stop() {
        console.log('[Bridge] Stopping...');
        
        if (this.bpftraceProcess) {
            this.bpftraceProcess.kill('SIGINT');
            this.bpftraceProcess = null;
        }

        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }

        // Print pattern summary
        this.extractPatterns().then(patterns => {
            console.log('\n[Bridge] Pattern Summary (Top 10):');
            patterns.slice(0, 10).forEach(p => {
                console.log(`  ${p.pattern}: ${p.frequency} times (${(p.confidence * 100).toFixed(1)}%)`);
            });
        });

        process.exit(0);
    }
}

// CLI
if (require.main === module) {
    const args = process.argv.slice(2);
    const scope = args.find(a => a.startsWith('--scope='))?.split('=')[1] || 'all';
    
    const bridge = new KernelObserverBridge();
    bridge.start(scope).catch(error => {
        console.error('[Bridge] Error:', error.message);
        process.exit(1);
    });
}

module.exports = KernelObserverBridge;