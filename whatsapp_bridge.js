#!/usr/bin/env node
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const fs = require('fs');
const path = require('path');

const DATA_DIR = '/home/ubuntu/.openclaw/whatsapp-data';
const CONFIG_FILE = path.join(DATA_DIR, 'config.json');

// Ensure data directory exists
if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
}

const client = new Client({
    authStrategy: new LocalAuth({ dataPath: DATA_DIR }),
    puppeteer: {
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

// Store paired status
let isReady = false;
let myNumber = null;

client.on('qr', (qr) => {
    console.log('\n╔══════════════════════════════════════════════════╗');
    console.log('║   Scan this QR code with WhatsApp on your phone  ║');
    console.log('╚══════════════════════════════════════════════════╝\n');
    qrcode.generate(qr, { small: true });
    console.log('\nWaiting for pairing...');
});

client.on('ready', () => {
    isReady = true;
    myNumber = client.info.wid.user;
    console.log(`✅ WhatsApp Ready! Number: +${myNumber}`);
    fs.writeFileSync(CONFIG_FILE, JSON.stringify({ 
        number: myNumber, 
        ready: true,
        pairedAt: new Date().toISOString()
    }));
});

client.on('authenticated', () => {
    console.log('🔐 Authenticated');
});

client.on('auth_failure', (msg) => {
    console.error('❌ Auth failure:', msg);
});

client.on('disconnected', (reason) => {
    console.log('⚠️  Disconnected:', reason);
    isReady = false;
});

// Handle incoming messages
client.on('message_create', async (msg) => {
    if (msg.fromMe) return; // Ignore own messages
    
    const data = {
        id: msg.id.id,
        from: msg.from,
        body: msg.body,
        timestamp: msg.timestamp,
        type: msg.type,
        hasMedia: msg.hasMedia
    };
    
    // Write to stdin for OpenClaw to read
    console.log('::WHATSAPP::' + JSON.stringify(data));
});

// Initialize
console.log('Initializing WhatsApp...');
client.initialize();

// Handle commands from OpenClaw
process.stdin.on('data', async (data) => {
    const line = data.toString().trim();
    if (!line.startsWith('SEND:')) return;
    
    try {
        const [, to, ...messageParts] = line.split(':');
        const message = messageParts.join(':');
        
        if (!isReady) {
            console.error('❌ WhatsApp not ready yet');
            return;
        }
        
        await client.sendMessage(to + '@c.us', message);
        console.log('✅ Sent to', to);
    } catch (e) {
        console.error('❌ Send failed:', e.message);
    }
});
