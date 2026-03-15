#!/usr/bin/env node
/**
 * Kernel Observer Daemon - Smart On-Demand Manager
 * 
 * Automatically starts kernel observer when needed, stops when idle.
 * 
 * Conditions to START:
 *   - Gateway running AND user active
 *   - Suspicious activity detected
 *   - Debug mode enabled
 *   - Explicitly requested
 * 
 * Conditions to STOP:
 *   - System idle >30 minutes
 *   - Battery low (<20%)
 *   - User logged out
 *   - Gateway stopped
 *   - Explicitly stopped
 */

const { exec, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const CONFIG = {
    pidFile: '/tmp/kernel-observer.pid',
    logFile: '/tmp/kernel-observer.log',
    bridgeScript: path.join(__dirname, 'bridge.js'),
    
    // Start conditions
    gatewayRunning: true,
    userActive: true,
    notOnBattery: true,
    
    // Stop conditions
    idleThreshold: 30 * 60 * 1000, // 30 minutes in ms
    batteryThreshold: 20, // Stop if battery < 20%
    
    // Check interval
    checkInterval: 60 * 1000, // Check every minute
    
    // Auto-start/stop
    autoManage: true,
};

class KernelObserverDaemon {
    constructor() {
        this.pid = null;
        this.lastActivity = Date.now();
        this.isRunning = false;
        this.checkTimer = null;
    }
    
    /**
     * Check if observer is running
     */
    async checkRunning() {
        try {
            const result = await this.exec('pgrep -f "kernel-observer/bridge.js"');
            return result.trim().length > 0;
        } catch {
            return false;
        }
    }
    
    /**
     * Check if gateway is running
     */
    async checkGateway() {
        try {
            const result = await this.exec('pgrep -f "openclaw gateway"');
            return result.trim().length > 0;
        } catch {
            return false;
        }
    }
    
    /**
     * Check user idle time (requires xprintidle)
     */
    async getIdleTime() {
        try {
            const result = await this.exec('xprintidle 2>/dev/null || echo 0');
            return parseInt(result.trim());
        } catch {
            return 0;
        }
    }
    
    /**
     * Check battery status
     */
    async getBatteryStatus() {
        try {
            const status = await this.exec('cat /sys/class/power_supply/BAT0/status 2>/dev/null || echo "Unknown"');
            const capacity = await this.exec('cat /sys/class/power_supply/BAT0/capacity 2>/dev/null || echo "100"');
            
            return {
                status: status.trim(),
                capacity: parseInt(capacity.trim()),
                isDischarging: status.trim() === 'Discharging'
            };
        } catch {
            return { status: 'Unknown', capacity: 100, isDischarging: false };
        }
    }
    
    /**
     * Check for suspicious activity (from logs)
     */
    async checkSuspiciousActivity() {
        try {
            // Check auth.log for failed logins
            const authLog = await this.exec('tail -100 /var/log/auth.log 2>/dev/null | grep -c "Failed password" || echo 0');
            const failedLogins = parseInt(authLog.trim());
            
            // Check for unusual processes
            const processes = await this.exec('ps aux | wc -l');
            const processCount = parseInt(processes.trim());
            
            return {
                failedLogins,
                processCount,
                suspicious: failedLogins > 5 // Threshold
            };
        } catch {
            return { failedLogins: 0, processCount: 0, suspicious: false };
        }
    }
    
    /**
     * Determine if should start
     */
    async shouldStart() {
        const reasons = [];
        
        // Check gateway
        const gatewayRunning = await this.checkGateway();
        if (!gatewayRunning) {
            return { start: false, reason: 'Gateway not running' };
        }
        
        // Check idle
        const idleTime = await this.getIdleTime();
        if (idleTime > CONFIG.idleThreshold) {
            return { start: false, reason: `User idle ${Math.floor(idleTime / 60000)} minutes` };
        }
        
        // Check battery
        const battery = await this.getBatteryStatus();
        if (battery.isDischarging && battery.capacity < CONFIG.batteryThreshold) {
            return { start: false, reason: `Battery low (${battery.capacity}%)` };
        }
        
        // Check suspicious activity
        const suspicious = await this.checkSuspiciousActivity();
        if (suspicious.suspicious) {
            reasons.push('Suspicious activity detected');
        }
        
        // All conditions met
        reasons.push('Gateway running');
        reasons.push('User active');
        if (!battery.isDischarging) {
            reasons.push('On AC power');
        }
        
        return { start: true, reasons };
    }
    
    /**
     * Determine if should stop
     */
    async shouldStop() {
        const reasons = [];
        
        // Check if running
        if (!await this.checkRunning()) {
            return { stop: false, reason: 'Not running' };
        }
        
        // Check gateway stopped
        const gatewayRunning = await this.checkGateway();
        if (!gatewayRunning) {
            return { stop: true, reason: 'Gateway stopped' };
        }
        
        // Check idle
        const idleTime = await this.getIdleTime();
        if (idleTime > CONFIG.idleThreshold) {
            return { stop: true, reason: `User idle ${Math.floor(idleTime / 60000)} minutes` };
        }
        
        // Check battery
        const battery = await this.getBatteryStatus();
        if (battery.isDischarging && battery.capacity < CONFIG.batteryThreshold) {
            return { stop: true, reason: `Battery low (${battery.capacity}%)` };
        }
        
        return { stop: false, reason: 'Conditions OK' };
    }
    
    /**
     * Start kernel observer
     */
    async start() {
        if (await this.checkRunning()) {
            console.log('[KernelObserver] Already running');
            return false;
        }
        
        const should = await this.shouldStart();
        if (!should.start) {
            console.log(`[KernelObserver] Not starting: ${should.reason}`);
            return false;
        }
        
        console.log(`[KernelObserver] Starting: ${should.reasons.join(', ')}`);
        
        return new Promise((resolve) => {
            const child = spawn('sudo', ['node', CONFIG.bridgeScript, '--scope=all'], {
                detached: true,
                stdio: ['ignore', fs.openSync(CONFIG.logFile, 'a'), fs.openSync(CONFIG.logFile, 'a')]
            });
            
            child.unref();
            this.pid = child.pid;
            this.isRunning = true;
            this.lastActivity = Date.now();
            
            console.log(`[KernelObserver] Started (PID: ${this.pid})`);
            resolve(true);
        });
    }
    
    /**
     * Stop kernel observer
     */
    async stop() {
        if (!await this.checkRunning()) {
            console.log('[KernelObserver] Not running');
            return false;
        }
        
        const should = await this.shouldStop();
        
        // Force stop if explicitly requested
        console.log(`[KernelObserver] Stopping: ${should.reason}`);
        
        try {
            await this.exec('sudo pkill -f "kernel-observer/bridge.js"');
            this.isRunning = false;
            console.log('[KernelObserver] Stopped');
            return true;
        } catch (error) {
            console.error('[KernelObserver] Failed to stop:', error.message);
            return false;
        }
    }
    
    /**
     * Main check loop
     */
    async check() {
        const running = await this.checkRunning();
        
        if (!running && CONFIG.autoManage) {
            // Should we start?
            const should = await this.shouldStart();
            if (should.start) {
                await this.start();
            }
        } else if (running && CONFIG.autoManage) {
            // Should we stop?
            const should = await this.shouldStop();
            if (should.stop) {
                await this.stop();
            }
        }
        
        // Log status
        console.log(`[KernelObserver] Status: ${running ? 'Running' : 'Stopped'}, Gateway: ${await this.checkGateway()}`);
    }
    
    /**
     * Start monitoring loop
     */
    startMonitoring() {
        console.log('[KernelObserver] Daemon starting...');
        console.log(`[KernelObserver] Check interval: ${CONFIG.checkInterval / 1000}s`);
        console.log(`[KernelObserver] Idle threshold: ${CONFIG.idleThreshold / 60000}m`);
        console.log(`[KernelObserver] Battery threshold: ${CONFIG.batteryThreshold}%`);
        console.log(`[KernelObserver] Auto-manage: ${CONFIG.autoManage}`);
        
        // Initial check
        this.check().catch(err => {
            console.error('[KernelObserver] Check failed:', err.message);
        });
        
        // Periodic checks
        this.checkTimer = setInterval(() => {
            this.check().catch(err => {
                console.error('[KernelObserver] Check failed:', err.message);
            });
        }, CONFIG.checkInterval);
        
        // Handle signals
        process.on('SIGINT', () => this.shutdown());
        process.on('SIGTERM', () => this.shutdown());
    }
    
    /**
     * Shutdown daemon
     */
    shutdown() {
        console.log('[KernelObserver] Shutting down...');
        
        if (this.checkTimer) {
            clearInterval(this.checkTimer);
        }
        
        process.exit(0);
    }
    
    /**
     * Execute shell command
     */
    exec(command) {
        return new Promise((resolve, reject) => {
            exec(command, (error, stdout, stderr) => {
                if (error) {
                    reject(error);
                } else {
                    resolve(stdout);
                }
            });
        });
    }
}

// CLI
if (require.main === module) {
    const daemon = new KernelObserverDaemon();
    
    const args = process.argv.slice(2);
    
    if (args.includes('--start')) {
        daemon.start().then(() => process.exit(0));
    } else if (args.includes('--stop')) {
        daemon.stop().then(() => process.exit(0));
    } else if (args.includes('--status')) {
        daemon.checkRunning().then(running => {
            console.log(running ? 'Running' : 'Stopped');
            process.exit(running ? 0 : 1);
        });
    } else if (args.includes('--daemon')) {
        daemon.startMonitoring();
    } else {
        console.log(`
Usage: node daemon.js [options]

Options:
  --start    Start kernel observer (if conditions met)
  --stop     Stop kernel observer
  --status   Check if running
  --daemon   Run as daemon (auto-start/stop based on conditions)

Configuration:
  Auto-start: Gateway running + User active + Not on battery
  Auto-stop:  User idle >30m OR Battery <20% OR Gateway stopped
`);
        process.exit(1);
    }
}

module.exports = KernelObserverDaemon;