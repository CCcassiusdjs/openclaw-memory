#!/usr/bin/env node
/**
 * Intervention Manager
 * 
 * Handles automatic fixes and user confirmation for system issues.
 * 
 * Usage: node manager.js
 */

const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

const CONFIG_PATH = path.join(process.env.HOME, '.openclaw/workspace/intervention-rules.yaml');
const LOG_PATH = path.join(process.env.HOME, '.openclaw/logs/interventions.log');

class InterventionManager {
    constructor() {
        this.rules = [];
        this.whitelist = new Map();
        this.blocked = [];
        this.rateLimiter = new Map();
        this.autoActionsCount = new Map();
        this.loadRules();
    }
    
    loadRules() {
        try {
            const content = fs.readFileSync(CONFIG_PATH, 'utf8');
            const config = yaml.load(content);
            this.rules = config.rules || [];
            this.whitelist = new Map(
                (config.whitelisted_auto_actions || []).map(a => [a.command, a.safe])
            );
            this.blocked = config.blocked_auto_actions || [];
            this.safety = config.safety || {};
            console.log(`[InterventionManager] Loaded ${this.rules.length} rules`);
        } catch (error) {
            console.error('[InterventionManager] Failed to load rules:', error.message);
            this.rules = [];
        }
    }
    
    /**
     * Check if command is whitelisted for auto-execution
     */
    isWhitelisted(command) {
        // Check blocked first
        for (const blocked of this.blocked) {
            if (new RegExp(blocked.pattern).test(command)) {
                return { allowed: false, reason: blocked.reason };
            }
        }
        
        // Check whitelist
        if (this.whitelist.has(command)) {
            return { allowed: true };
        }
        
        // Check if command is safe
        const safePatterns = [
            /^find .+ -delete$/,  // find with delete
            /^rm -rf .+\.cache/,  // clean cache
            /^rm -rf \/tmp/,      // clean temp
            /^cargo clean$/,       // cargo clean
            /^npm cache clean/,    // npm clean
        ];
        
        for (const pattern of safePatterns) {
            if (pattern.test(command)) {
                return { allowed: true };
            }
        }
        
        return { allowed: false, reason: 'Not in whitelist' };
    }
    
    /**
     * Check rate limit
     */
    checkRateLimit(rule) {
        if (!rule.rate_limit) return true;
        
        const last = this.rateLimiter.get(rule.name);
        if (!last) return true;
        
        const now = Date.now();
        const limitMs = this.parseDuration(rule.rate_limit);
        
        return (now - last) > limitMs;
    }
    
    /**
     * Check hourly auto-action limit
     */
    checkHourlyLimit() {
        const now = Date.now();
        const hourAgo = now - 3600000;
        
        // Clean old entries
        for (const [key, timestamps] of this.autoActionsCount) {
            const recent = timestamps.filter(t => t > hourAgo);
            if (recent.length === 0) {
                this.autoActionsCount.delete(key);
            } else {
                this.autoActionsCount.set(key, recent);
            }
        }
        
        // Count this hour
        const thisHour = Math.floor(now / 3600000);
        const count = this.autoActionsCount.get(thisHour) || [];
        
        const maxPerHour = this.safety.max_auto_actions_per_hour || 5;
        return count.length < maxPerHour;
    }
    
    /**
     * Record auto-action
     */
    recordAutoAction() {
        const now = Date.now();
        const thisHour = Math.floor(now / 3600000);
        const count = this.autoActionsCount.get(thisHour) || [];
        count.push(now);
        this.autoActionsCount.set(thisHour, count);
    }
    
    parseDuration(duration) {
        if (!duration) return 0;
        const units = { s: 1000, m: 60000, h: 3600000, d: 86400000 };
        const match = duration.match(/^(\d+)([smhd])$/);
        return match ? parseInt(match[1]) * units[match[2]] : 0;
    }
    
    /**
     * Handle event
     */
    async handleEvent(event) {
        // Find matching rule
        const rule = this.findMatchingRule(event);
        if (!rule) return;
        
        // Check rate limit
        if (!this.checkRateLimit(rule)) {
            console.log(`[InterventionManager] Rate limited: ${rule.name}`);
            return;
        }
        
        // Update rate limiter
        this.rateLimiter.set(rule.name, Date.now());
        
        // Handle based on level
        switch (rule.level) {
            case 'notify':
                await this.notify(rule, event);
                break;
            case 'ask':
                await this.ask(rule, event);
                break;
            case 'auto':
                await this.autoFix(rule, event);
                break;
            case 'block':
                await this.block(rule, event);
                break;
        }
    }
    
    /**
     * Find matching rule
     */
    findMatchingRule(event) {
        return this.rules.find(rule => {
            // This would be evaluated by the kernel observer
            // For now, return first matching condition
            if (rule.trigger.condition && event.condition) {
                return rule.trigger.condition === event.condition;
            }
            return false;
        });
    }
    
    /**
     * Notify only (no action)
     */
    async notify(rule, event) {
        const message = this.renderMessage(rule.message, event);
        
        // Use notification manager
        const { NotificationManager } = require('../notification/manager');
        const notifier = new NotificationManager();
        
        await notifier.send({
            title: 'OpenClaw Alert',
            message: message,
            priority: rule.priority || 'medium',
            channels: rule.channels || ['desktop']
        });
        
        this.logIntervention(rule, event, 'notified');
    }
    
    /**
     * Ask for permission
     */
    async ask(rule, event) {
        const message = this.renderMessage(rule.message, event);
        
        // Use notification manager to ask
        const { NotificationManager } = require('../notification/manager');
        const notifier = new NotificationManager();
        
        // TODO: Implement proper question/answer flow
        // For now, just notify
        await notifier.send({
            title: 'OpenClaw Question',
            message: message,
            priority: rule.priority || 'high',
            channels: ['desktop', 'whatsapp']
        });
        
        this.logIntervention(rule, event, 'asked');
    }
    
    /**
     * Auto-fix
     */
    async autoFix(rule, event) {
        // Check hourly limit
        if (!this.checkHourlyLimit()) {
            console.log(`[InterventionManager] Hourly auto-action limit reached`);
            return;
        }
        
        // Execute auto-actions
        const results = [];
        
        for (const action of rule.auto_actions || []) {
            // Check whitelist
            const check = this.isWhitelisted(action.command);
            if (!check.allowed) {
                console.log(`[InterventionManager] Blocked non-whitelisted: ${action.command}`);
                continue;
            }
            
            // Execute
            console.log(`[InterventionManager] Auto-executing: ${action.name}`);
            
            try {
                const result = await this.execute(action.command, event);
                results.push({ action: action.name, result, success: true });
                this.recordAutoAction();
            } catch (error) {
                console.error(`[InterventionManager] Failed: ${action.name}`, error.message);
                results.push({ action: action.name, error: error.message, success: false });
            }
        }
        
        // Log intervention
        this.logIntervention(rule, event, 'auto', results);
        
        // Notify after
        if (rule.notify_after) {
            const summary = results
                .filter(r => r.success)
                .map(r => r.action)
                .join(', ');
            
            const { NotificationManager } = require('../notification/manager');
            const notifier = new NotificationManager();
            
            await notifier.send({
                title: 'OpenClaw Auto-Fix',
                message: `${rule.name}: ${summary || 'No actions taken'}`,
                priority: 'medium',
                channels: ['desktop']
            });
        }
        
        return results;
    }
    
    /**
     * Block operation
     */
    async block(rule, event) {
        console.log(`[InterventionManager] Blocked: ${rule.name}`);
        this.logIntervention(rule, event, 'blocked');
        
        // This would require kernel-level integration to actually block
        // For now, just log and notify
    }
    
    /**
     * Execute command
     */
    async execute(command, event) {
        // Render command with event variables
        const rendered = this.renderCommand(command, event);
        
        return new Promise((resolve, reject) => {
            exec(rendered, (error, stdout, stderr) => {
                if (error) {
                    reject(new Error(stderr || error.message));
                } else {
                    resolve(stdout);
                }
            });
        });
    }
    
    /**
     * Render message with variables
     */
    renderMessage(template, event) {
        return template
            .replace(/\${mount}/g, event.mount || '')
            .replace(/\${percent}/g, event.percent || '')
            .replace(/\${process}/g, event.process || '')
            .replace(/\${pid}/g, event.pid || '')
            .replace(/\${cpu}/g, event.cpu || '')
            .replace(/\${available}/g, event.available || '')
            .replace(/\${ip}/g, event.ip || '')
            .replace(/\${description}/g, event.description || '');
    }
    
    /**
     * Render command with variables
     */
    renderCommand(template, event) {
        return template
            .replace(/\${mount}/g, event.mount || '')
            .replace(/\${path}/g, event.path || '')
            .replace(/\${pid}/g, event.pid || '')
            .replace(/\${ip}/g, event.ip || '')
            .replace(/\${service}/g, event.service || '');
    }
    
    /**
     * Log intervention
     */
    logIntervention(rule, event, status, results = []) {
        const logPath = path.join(process.env.HOME, '.openclaw/logs/interventions.log');
        const logDir = path.dirname(logPath);
        
        if (!fs.existsSync(logDir)) {
            fs.mkdirSync(logDir, { recursive: true });
        }
        
        const logEntry = JSON.stringify({
            timestamp: new Date().toISOString(),
            rule: rule.name,
            level: rule.level,
            event: event,
            status: status,
            results: results
        }) + '\n';
        
        fs.appendFileSync(logPath, logEntry);
    }
    
    /**
     * Start manager
     */
    start() {
        console.log('[InterventionManager] Starting...');
        
        // Reload rules every minute
        setInterval(() => {
            this.loadRules();
        }, 60 * 1000);
        
        console.log('[InterventionManager] Ready');
    }
}

// CLI
if (require.main === module) {
    const manager = new InterventionManager();
    
    // Test intervention
    if (process.argv.includes('--test')) {
        manager.handleEvent({
            condition: 'disk_usage > 85%',
            mount: '/home',
            percent: '92'
        }).then(() => {
            console.log('[InterventionManager] Test completed');
            process.exit(0);
        }).catch(err => {
            console.error('[InterventionManager] Test failed:', err.message);
            process.exit(1);
        });
    } else {
        manager.start();
    }
}

module.exports = InterventionManager;