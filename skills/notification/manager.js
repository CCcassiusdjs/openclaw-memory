#!/usr/bin/env node
/**
 * Notification Manager
 * 
 * Sends desktop notifications, WhatsApp messages, and handles user interaction.
 * 
 * Usage: node manager.js
 */

const { exec } = require('child_process');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

const CONFIG_PATH = path.join(process.env.HOME, '.openclaw/workspace/notification-rules.yaml');
const LOG_PATH = path.join(process.env.HOME, '.openclaw/logs/notifications.log');

class NotificationManager {
    constructor() {
        this.rules = [];
        this.rateLimiter = new Map();
        this.queue = [];
        this.loadRules();
    }
    
    loadRules() {
        try {
            const content = fs.readFileSync(CONFIG_PATH, 'utf8');
            const config = yaml.load(content);
            this.rules = config.rules || [];
            this.quietHours = config.quiet_hours || {};
            this.channels = config.channels || {};
            console.log(`[NotificationManager] Loaded ${this.rules.length} rules`);
        } catch (error) {
            console.error('[NotificationManager] Failed to load rules:', error.message);
            this.rules = [];
        }
    }
    
    /**
     * Check if we're in quiet hours
     */
    isQuietHours(priority) {
        const now = new Date();
        const hour = now.getHours();
        const day = now.getDay();
        
        // Weekend vs weekday
        const isWeekend = day === 0 || day === 6;
        const config = isWeekend ? this.quietHours.weekends : this.quietHours.weekdays;
        
        if (!config) return false;
        
        const startHour = parseInt(config.start.split(':')[0]);
        const endHour = parseInt(config.end.split(':')[0]);
        
        // Check if current hour is in quiet range
        const inQuietHours = hour >= startHour || hour < endHour;
        
        // Exceptions
        if (inQuietHours && this.quietHours.exceptions) {
            const exception = this.quietHours.exceptions[priority];
            if (exception === 'always') return false;
            if (exception === 'queue') return 'queue';
        }
        
        return inQuietHours;
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
    
    parseDuration(duration) {
        if (!duration) return 0;
        const units = { s: 1000, m: 60000, h: 3600000, d: 86400000 };
        const match = duration.match(/^(\d+)([smhd])$/);
        return match ? parseInt(match[1]) * units[match[2]] : 0;
    }
    
    /**
     * Find matching rule
     */
    findMatchingRule(event) {
        return this.rules.find(rule => {
            // Check condition
            if (rule.trigger.condition) {
                // This would be evaluated by the kernel observer
                // For now, simple matching
                return true;
            }
            return false;
        });
    }
    
    /**
     * Send notification via all channels
     */
    async send(options) {
        const { title, message, priority = 'medium', channels = ['desktop'] } = options;
        
        // Check quiet hours
        const quietStatus = this.isQuietHours(priority);
        if (quietStatus === true) {
            console.log(`[NotificationManager] Quiet hours, skipping ${priority} notification`);
            return;
        }
        if (quietStatus === 'queue') {
            console.log(`[NotificationManager] Queuing ${priority} notification for morning`);
            this.queue.push(options);
            return;
        }
        
        // Send to each channel
        for (const channel of channels) {
            try {
                await this.sendToChannel(channel, title, message, priority);
            } catch (error) {
                console.error(`[NotificationManager] Failed to send via ${channel}:`, error.message);
            }
        }
        
        // Log notification
        this.log(options);
    }
    
    /**
     * Send to specific channel
     */
    async sendToChannel(channel, title, message, priority) {
        switch (channel) {
            case 'desktop':
                return await this.sendDesktop(title, message, priority);
            case 'whatsapp':
                return await this.sendWhatsApp(title, message);
            case 'email':
                return await this.sendEmail(title, message);
            case 'log':
                return await this.sendLog(title, message);
            default:
                console.warn(`[NotificationManager] Unknown channel: ${channel}`);
        }
    }
    
    /**
     * Desktop notification (notify-send)
     */
    async sendDesktop(title, message, priority) {
        const channelConfig = this.channels.desktop;
        if (!channelConfig?.enabled) return;
        
        const urgency = channelConfig.options?.urgency?.[priority] || '--urgency=normal';
        const expire = channelConfig.options?.expire?.[priority] || 5000;
        
        const cmd = `notify-send "${title}" "${message}" ${urgency} --expire-time=${expire}`;
        
        return new Promise((resolve, reject) => {
            exec(cmd, (error) => {
                if (error) reject(error);
                else resolve();
            });
        });
    }
    
    /**
     * WhatsApp message (via OpenClaw message tool)
     */
    async sendWhatsApp(title, message) {
        const channelConfig = this.channels.whatsapp;
        if (!channelConfig?.enabled) return;
        
        // Use OpenClaw's message tool (would need to call through Gateway)
        // For now, log that we would send
        console.log(`[WhatsApp] ${title}: ${message}`);
        
        // TODO: Call Gateway message API
        // await fetch('http://localhost:18789/api/message', {
        //     method: 'POST',
        //     body: JSON.stringify({
        //         channel: 'whatsapp',
        //         to: channelConfig.to,
        //         message: `${title}\n\n${message}`
        //     })
        // });
    }
    
    /**
     * Email notification
     */
    async sendEmail(title, message) {
        const channelConfig = this.channels.email;
        if (!channelConfig?.enabled) return;
        
        // Use SMTP skill
        const smtpScript = path.join(process.env.HOME, '.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js');
        
        return new Promise((resolve, reject) => {
            exec(`node ${smtpScript} send --to ${channelConfig.to} --subject "[OpenClaw] ${title}" --body "${message}"`, (error) => {
                if (error) reject(error);
                else resolve();
            });
        });
    }
    
    /**
     * Log notification
     */
    async sendLog(title, message) {
        const channelConfig = this.channels.log;
        if (!channelConfig?.enabled) return;
        
        const logPath = channelConfig.path?.replace('~', process.env.HOME) || LOG_PATH;
        const logDir = path.dirname(logPath);
        
        if (!fs.existsSync(logDir)) {
            fs.mkdirSync(logDir, { recursive: true });
        }
        
        const logEntry = JSON.stringify({
            timestamp: new Date().toISOString(),
            title,
            message
        }) + '\n';
        
        fs.appendFileSync(logPath, logEntry);
    }
    
    /**
     * Log notification to audit log
     */
    log(options) {
        const logPath = path.join(process.env.HOME, '.openclaw/logs/notifications.log');
        const logDir = path.dirname(logPath);
        
        if (!fs.existsSync(logDir)) {
            fs.mkdirSync(logDir, { recursive: true });
        }
        
        const logEntry = JSON.stringify({
            timestamp: new Date().toISOString(),
            ...options
        }) + '\n';
        
        fs.appendFileSync(logPath, logEntry);
    }
    
    /**
     * Ask user a question with options
     */
    async ask(question, options = []) {
        // For desktop, use notify-send with actions (requires notification daemon support)
        // For WhatsApp, send message and wait for reply
        
        console.log(`[Ask] ${question}`);
        console.log(`Options: ${options.join(', ')}`);
        
        // TODO: Implement proper question/answer flow
        // This would require a separate service to handle responses
        
        return new Promise((resolve) => {
            // For now, just send desktop notification
            this.sendDesktop('OpenClaw Question', question, 'high')
                .then(() => resolve(null))
                .catch(() => resolve(null));
        });
    }
    
    /**
     * Process queued notifications (for quiet hours)
     */
    processQueue() {
        if (this.queue.length === 0) return;
        
        console.log(`[NotificationManager] Processing ${this.queue.length} queued notifications`);
        
        for (const options of this.queue) {
            this.send(options).catch(err => {
                console.error('[NotificationManager] Failed to send queued notification:', err.message);
            });
        }
        
        this.queue = [];
    }
    
    /**
     * Start processing loop
     */
    start() {
        console.log('[NotificationManager] Starting...');
        
        // Process queue every 5 minutes
        setInterval(() => {
            this.processQueue();
        }, 5 * 60 * 1000);
        
        // Reload rules every minute
        setInterval(() => {
            this.loadRules();
        }, 60 * 1000);
        
        console.log('[NotificationManager] Ready');
    }
}

// CLI
if (require.main === module) {
    const manager = new NotificationManager();
    
    // Test notification
    if (process.argv.includes('--test')) {
        manager.send({
            title: 'OpenClaw Test',
            message: 'Notification system working!',
            priority: 'medium',
            channels: ['desktop', 'log']
        }).then(() => {
            console.log('[NotificationManager] Test notification sent');
            process.exit(0);
        }).catch(err => {
            console.error('[NotificationManager] Test failed:', err.message);
            process.exit(1);
        });
    } else {
        manager.start();
    }
}

module.exports = NotificationManager;