// Kalpana Voice Input - Speech Recognition
let recognition = null;
let isListening = false;

// Initialize Speech Recognition
function initVoiceRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
        console.error('Speech Recognition not supported in this browser');
        return;
    }
    
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';
    
    recognition.onstart = () => {
        console.log('Voice recognition started');
        isListening = true;
        const core = document.getElementById('arc-core');
        core.classList.add('listening');
        log('<b style="color: #ff6b35">[MIC]:</b> Listening...');
    };
    
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        const confidence = event.results[0][0].confidence;
        
        console.log(`Transcript: ${transcript} (${Math.round(confidence * 100)}% confidence)`);
        log(`<b style="color: #ffaa00">[YOU]:</b> ${transcript}`);
        
        // Send to backend for processing
        processVoiceInput(transcript);
    };
    
    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        
        if (event.error === 'not-allowed') {
            log('<b style="color: #ff3300">[ERROR]:</b> Microphone access denied. Please grant permission.');
        } else {
            log(`<b style="color: #ff3300">[ERROR]:</b> ${event.error}`);
        }
        
        stopListening();
    };
    
    recognition.onend = () => {
        console.log('Voice recognition ended');
        stopListening();
    };
}

// Text‑to‑speech helper
function speak(text) {
    if (!('speechSynthesis' in window)) {
        console.warn('Speech Synthesis not supported');
        return;
    }
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    window.speechSynthesis.speak(utterance);
}

function toggleVoiceInput() {
    if (!recognition) {
        initVoiceRecognition();
    }
    
    if (isListening) {
        recognition.stop();
    } else {
        try {
            recognition.start();
        } catch (error) {
            console.error('Failed to start recognition:', error);
            log('<b style="color: #ff3300">[ERROR]:</b> Failed to start microphone');
        }
    }
}

function stopListening() {
    isListening = false;
    const core = document.getElementById('arc-core');
    core.classList.remove('listening', 'processing');
}

async function processVoiceInput(transcript) {
    // Change to processing state
    const core = document.getElementById('arc-core');
    core.classList.remove('listening');
    core.classList.add('processing');
    
    log('<b style="color: #00d9ff">[KALPANA]:</b> Processing...');
    
    try {
        const response = await fetch('/api/voice/process', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ transcript: transcript })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            log(`<b style="color: var(--cyber-blue)">[KALPANA]:</b> ${data.response}`);
        } else {
            log(`<b style="color: #ff3300">[ERROR]:</b> ${data.message}`);
        }
    } catch (error) {
        console.error('Voice processing error:', error);
        log('<b style="color: #ff3300">[ERROR]:</b> Failed to process voice input');
    } finally {
        stopListening();
    }
}

// Initialize on page load
window.addEventListener('DOMContentLoaded', () => {
    console.log('Voice recognition module loaded');
});
