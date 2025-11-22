// UI Interaction and Animation Logic

document.addEventListener('DOMContentLoaded', () => {
    initClock();
    initAudioVisualizer();
    initMatrixBackground();
});

function initClock() {
    const clockEl = document.getElementById('clock');
    setInterval(() => {
        const now = new Date();
        clockEl.textContent = now.toLocaleTimeString('en-US', { hour12: false });
    }, 1000);
}

function initAudioVisualizer() {
    const container = document.getElementById('audio-viz');
    const barCount = 20;
    
    // Create bars
    for (let i = 0; i < barCount; i++) {
        const bar = document.createElement('div');
        bar.className = 'wave-bar';
        bar.style.height = '10px';
        container.appendChild(bar);
    }

    // Animate bars
    setInterval(() => {
        const bars = document.querySelectorAll('.wave-bar');
        bars.forEach(bar => {
            // Random height between 10% and 100%
            const height = Math.floor(Math.random() * 90) + 10;
            bar.style.height = `${height}%`;
            
            // Random color opacity
            const opacity = Math.random() * 0.5 + 0.5;
            bar.style.opacity = opacity;
        });
    }, 100);
}

function initMatrixBackground() {
    // Create a canvas for matrix rain effect
    const canvas = document.createElement('canvas');
    canvas.classList.add('data-stream');
    document.body.appendChild(canvas);
    
    const ctx = canvas.getContext('2d');
    
    // Set canvas size
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    const katakana = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const characters = katakana.split('');
    
    const fontSize = 14;
    const columns = canvas.width / fontSize;
    
    const drops = [];
    for (let i = 0; i < columns; i++) {
        drops[i] = 1;
    }
    
    function draw() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = '#00aaff'; // Blue text
        ctx.fillStyle = 'rgba(0, 170, 255, 0.3)'; // Blue text for Kalpana
        ctx.font = fontSize + 'px monospace';
        
        for (let i = 0; i < drops.length; i++) {
            const text = characters[Math.floor(Math.random() * characters.length)];
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            
            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    }
    
    setInterval(draw, 33);
    
    // Handle resize
    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
}
