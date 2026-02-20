/**
 * OpenClaw Web App
 * PWA with Talk Mode, WebSocket chat, and Web Speech API
 */

// Configuration
const CONFIG = {
    WS_URL: 'ws://127.0.0.1:18789',
    WS_RECONNECT_DELAY: 3000,
    WS_MAX_RECONNECT_ATTEMPTS: 10,
    TTS_RATE: 1.0,
    TTS_PITCH: 1.0,
    TTS_VOLUME: 1.0
};

// State
const state = {
    ws: null,
    wsConnected: false,
    wsReconnectAttempts: 0,
    wsReconnectTimer: null,
    isListening: false,
    isSpeaking: false,
    recognition: null,
    synthesis: window.speechSynthesis,
    messages: [],
    audioContext: null,
    analyser: null,
    micStream: null
};

// DOM Elements
const elements = {
    messages: document.getElementById('messages'),
    messageInput: document.getElementById('messageInput'),
    sendBtn: document.getElementById('sendBtn'),
    micBtn: document.getElementById('micBtn'),
    shareBtn: document.getElementById('shareBtn'),
    connectionStatus: document.getElementById('connectionStatus'),
    voiceVisualizer: document.getElementById('voiceVisualizer'),
    permissionModal: document.getElementById('permissionModal'),
    grantMicBtn: document.getElementById('grantMicBtn'),
    toast: document.getElementById('toast'),
    chatContainer: document.getElementById('chatContainer')
};

// ============================================
// WebSocket Connection
// ============================================

function initWebSocket() {
    if (state.ws?.readyState === WebSocket.CONNECTING) return;

    try {
        state.ws = new WebSocket(CONFIG.WS_URL);

        state.ws.onopen = () => {
            console.log('WebSocket connected');
            state.wsConnected = true;
            state.wsReconnectAttempts = 0;
            updateConnectionStatus(true);
            showToast('Connected to OpenClaw');
        };

        state.ws.onmessage = (event) => {
            handleGatewayMessage(event.data);
        };

        state.ws.onclose = () => {
            console.log('WebSocket closed');
            state.wsConnected = false;
            updateConnectionStatus(false);
            scheduleReconnect();
        };

        state.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            state.wsConnected = false;
            updateConnectionStatus(false);
        };
    } catch (err) {
        console.error('Failed to create WebSocket:', err);
        scheduleReconnect();
    }
}

function scheduleReconnect() {
    if (state.wsReconnectAttempts >= CONFIG.WS_MAX_RECONNECT_ATTEMPTS) {
        showToast('Connection failed. Please refresh.');
        return;
    }

    state.wsReconnectAttempts++;
    const delay = Math.min(CONFIG.WS_RECONNECT_DELAY * state.wsReconnectAttempts, 30000);
    
    console.log(`Reconnecting in ${delay}ms (attempt ${state.wsReconnectAttempts})`);
    
    state.wsReconnectTimer = setTimeout(() => {
        initWebSocket();
    }, delay);
}

function updateConnectionStatus(connected) {
    elements.connectionStatus.classList.toggle('connected', connected);
    elements.connectionStatus.title = connected ? 'Connected' : 'Disconnected';
}

function sendToGateway(message) {
    if (state.wsConnected && state.ws?.readyState === WebSocket.OPEN) {
        state.ws.send(JSON.stringify(message));
    } else {
        showToast('Not connected. Message queued.');
    }
}

function handleGatewayMessage(data) {
    try {
        const msg = JSON.parse(data);
        
        if (msg.type === 'response' || msg.text) {
            addMessage(msg.text || msg.content, 'assistant');
            if (msg.speak !== false) {
                speakText(msg.text || msg.content);
            }
        } else if (msg.type === 'error') {
            addMessage(`Error: ${msg.message}`, 'system');
        } else if (msg.type === 'status') {
            showToast(msg.message);
        }
    } catch (err) {
        // Plain text response
        addMessage(data, 'assistant');
        speakText(data);
    }
}

// ============================================
// Speech Recognition (Web Speech API)
// ============================================

function initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
        console.warn('Speech Recognition not supported');
        elements.micBtn.style.display = 'none';
        return false;
    }

    state.recognition = new SpeechRecognition();
    state.recognition.continuous = false;
    state.recognition.interimResults = true;
    state.recognition.lang = 'en-US';

    state.recognition.onstart = () => {
        state.isListening = true;
        elements.micBtn.classList.add('listening');
        elements.voiceVisualizer.classList.remove('hidden');
        showToast('Listening...');
        startVoiceVisualization();
    };

    state.recognition.onresult = (event) => {
        let finalTranscript = '';
        let interimTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript;
            } else {
                interimTranscript += transcript;
            }
        }

        if (interimTranscript) {
            elements.messageInput.value = interimTranscript;
        }

        if (finalTranscript) {
            elements.messageInput.value = finalTranscript;
            sendMessage(finalTranscript);
        }
    };

    state.recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        if (event.error === 'not-allowed') {
            showToast('Microphone access denied');
            elements.permissionModal.classList.remove('hidden');
        } else if (event.error === 'no-speech') {
            showToast('No speech detected');
        }
        stopListening();
    };

    state.recognition.onend = () => {
        stopListening();
    };

    return true;
}

function startListening() {
    if (!state.recognition) {
        if (!initSpeechRecognition()) {
            showToast('Voice input not supported');
            return;
        }
    }

    try {
        state.recognition.start();
    } catch (err) {
        console.error('Failed to start recognition:', err);
        showToast('Could not start listening');
    }
}

function stopListening() {
    state.isListening = false;
    elements.micBtn.classList.remove('listening');
    elements.voiceVisualizer.classList.add('hidden');
    stopVoiceVisualization();
    
    try {
        state.recognition?.stop();
    } catch (err) {
        // Ignore
    }
}

function toggleListening() {
    if (state.isListening) {
        stopListening();
    } else {
        elements.messageInput.value = '';
        startListening();
    }
}

// ============================================
// Voice Visualization
// ============================================

async function startVoiceVisualization() {
    try {
        if (!state.audioContext) {
            state.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }

        state.micStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const source = state.audioContext.createMediaStreamSource(state.micStream);
        state.analyser = state.audioContext.createAnalyser();
        state.analyser.fftSize = 64;
        source.connect(state.analyser);

        visualize();
    } catch (err) {
        console.error('Failed to start visualization:', err);
    }
}

function stopVoiceVisualization() {
    if (state.micStream) {
        state.micStream.getTracks().forEach(track => track.stop());
        state.micStream = null;
    }
}

function visualize() {
    if (!state.isListening || !state.analyser) return;

    const dataArray = new Uint8Array(state.analyser.frequencyBinCount);
    state.analyser.getByteFrequencyData(dataArray);

    const bars = elements.voiceVisualizer.querySelectorAll('.voice-waves span');
    const step = Math.floor(dataArray.length / bars.length);

    bars.forEach((bar, i) => {
        const value = dataArray[i * step] || 0;
        const height = Math.max(10, (value / 255) * 60);
        bar.style.height = `${height}px`;
    });

    requestAnimationFrame(visualize);
}

// ============================================
// Text-to-Speech
// ============================================

function speakText(text) {
    if (!state.synthesis) return;
    
    // Stop any current speech
    state.synthesis.cancel();

    // Clean text for speech
    const cleanText = text
        .replace(/https?:\/\/\S+/g, 'link')
        .replace(/[*_`#]/g, '')
        .substring(0, 500); // Limit length

    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = CONFIG.TTS_RATE;
    utterance.pitch = CONFIG.TTS_PITCH;
    utterance.volume = CONFIG.TTS_VOLUME;

    // Try to find a good voice
    const voices = state.synthesis.getVoices();
    const preferredVoice = voices.find(v => v.name.includes('Google') || v.name.includes('Samantha'));
    if (preferredVoice) {
        utterance.voice = preferredVoice;
    }

    utterance.onstart = () => {
        state.isSpeaking = true;
    };

    utterance.onend = () => {
        state.isSpeaking = false;
    };

    state.synthesis.speak(utterance);
}

function stopSpeaking() {
    if (state.synthesis) {
        state.synthesis.cancel();
        state.isSpeaking = false;
    }
}

// ============================================
// Chat Interface
// ============================================

function addMessage(text, role) {
    const messageEl = document.createElement('div');
    messageEl.className = `message ${role}`;
    
    const contentEl = document.createElement('div');
    contentEl.className = 'message-content';
    
    // Simple markdown-like formatting
    const formattedText = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.+?)\*/g, '<em>$1</em>')
        .replace(/`(.+?)`/g, '<code>$1</code>')
        .replace(/\n/g, '<br>');
    
    contentEl.innerHTML = formattedText;
    messageEl.appendChild(contentEl);
    
    const timeEl = document.createElement('span');
    timeEl.className = 'message-time';
    timeEl.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    messageEl.appendChild(timeEl);
    
    elements.messages.appendChild(messageEl);
    scrollToBottom();
    
    // Store in history
    state.messages.push({ role, text, time: Date.now() });
    
    // Keep only last 100 messages
    if (state.messages.length > 100) {
        state.messages.shift();
    }
}

function sendMessage(text) {
    text = text || elements.messageInput.value.trim();
    if (!text) return;

    addMessage(text, 'user');
    elements.messageInput.value = '';

    sendToGateway({
        type: 'message',
        text: text,
        timestamp: Date.now()
    });
}

function scrollToBottom() {
    elements.chatContainer.scrollTop = elements.chatContainer.scrollHeight;
}

// ============================================
// Web Share API
// ============================================

async function shareContent() {
    const shareData = {
        title: 'OpenClaw',
        text: 'Check out OpenClaw - AI assistant with voice!',
        url: window.location.href
    };

    if (navigator.share) {
        try {
            await navigator.share(shareData);
        } catch (err) {
            if (err.name !== 'AbortError') {
                console.error('Share failed:', err);
                fallbackShare();
            }
        }
    } else {
        fallbackShare();
    }
}

function fallbackShare() {
    // Copy to clipboard
    navigator.clipboard.writeText(window.location.href).then(() => {
        showToast('Link copied to clipboard!');
    }).catch(() => {
        showToast('Share not available');
    });
}

// ============================================
// UI Helpers
// ============================================

function showToast(message) {
    elements.toast.textContent = message;
    elements.toast.classList.remove('hidden');
    
    setTimeout(() => {
        elements.toast.classList.add('hidden');
    }, 3000);
}

// ============================================
// Event Listeners
// ============================================

function initEventListeners() {
    // Send button
    elements.sendBtn.addEventListener('click', () => sendMessage());

    // Enter key to send
    elements.messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Microphone button - support both click and hold
    let micTimer = null;
    
    elements.micBtn.addEventListener('mousedown', () => {
        micTimer = setTimeout(() => {
            toggleListening();
        }, 100);
    });
    
    elements.micBtn.addEventListener('mouseup', () => {
        clearTimeout(micTimer);
        if (state.isListening) {
            // Keep listening until speech ends or clicked again
        }
    });
    
    elements.micBtn.addEventListener('mouseleave', () => {
        clearTimeout(micTimer);
    });

    // Touch events for mobile
    elements.micBtn.addEventListener('touchstart', (e) => {
        e.preventDefault();
        toggleListening();
    });

    elements.micBtn.addEventListener('touchend', (e) => {
        e.preventDefault();
    });

    // Share button
    elements.shareBtn.addEventListener('click', shareContent);

    // Permission modal
    elements.grantMicBtn.addEventListener('click', () => {
        elements.permissionModal.classList.add('hidden');
        startListening();
    });

    // Stop speaking on click anywhere
    document.addEventListener('click', (e) => {
        if (state.isSpeaking && !e.target.closest('.message.assistant')) {
            stopSpeaking();
        }
    });

    // Visibility change - reconnect when visible
    document.addEventListener('visibilitychange', () => {
        if (!document.hidden && !state.wsConnected) {
            initWebSocket();
        }
    });
}

// ============================================
// Service Worker Registration
// ============================================

function registerServiceWorker() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('sw.js')
            .then(reg => console.log('SW registered:', reg))
            .catch(err => console.log('SW registration failed:', err));
    }
}

// ============================================
// Initialization
// ============================================

function init() {
    initSpeechRecognition();
    initWebSocket();
    initEventListeners();
    registerServiceWorker();

    // Load voices for TTS
    if (state.synthesis) {
        state.synthesis.getVoices();
        state.synthesis.onvoiceschanged = () => {
            state.synthesis.getVoices();
        };
    }

    console.log('OpenClaw Web App initialized');
}

// Start when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
