#!/usr/bin/env node
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const fs = require('fs');
const path = require('path');

const DATA_DIR = '/home/ubuntu/.openclaw/whatsapp-data';

// Clear previous session
const sessionDir = path.join(DATA_DIR, 'session');
if (fs.existsSync(sessionDir)) {
    fs.rmSync(sessionDir, { recursive: true, force: true });
}

const client = new Client({
    authStrategy: new LocalAuth({ dataPath: DATA_DIR }),
    puppeteer: {
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
        executablePath: process.env.PUPPETEER_EXECUTABLE_PATH || undefined
    }
});

client.on('qr', (qr) => {
    console.log('\n╔══════════════════════════════════════════════════╗');
    console.log('║   SCAN THIS QR CODE WITH WHATSAPP ON YOUR PHONE  ║');
    console.log('╚══════════════════════════════════════════════════╝\n');
    qrcode.generate(qr, { small: true });
    console.log('\nWaiting for pairing... (60 seconds)\n');
});

client.on('authenticated', () => {
    console.log('✅ Authenticated! Scan complete.');
});

client.on('ready', () => {
    const number = client.info.wid.user;
    console.log(`✅ WhatsApp Ready! Number: +${number}`);
    console.log('You can now close this and use WhatsApp in OpenClaw.');
    process.exit(0);
});

client.on('auth_failure', (msg) => {
    console.error('❌ Auth failed:', msg);
    process.exit(1);
});

console.log('Starting WhatsApp pairing for +918780809933...');
client.initialize();

// Timeout after 60 seconds
setTimeout(() => {
    console.log('\n⚠️  Timeout: QR code expired. Run again to retry.');
    process.exit(1);
}, 60000);
