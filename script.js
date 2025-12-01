// --- JAVASCRIPT: LÓGICA DEL CLIENTE ---

const translations = {
    es: {
        title: "🛡️ AI Spam Hunter",
        subtitle: "Inserta un mensaje para analizar con Inteligencia Artificial",
        placeholder: "Ej: ¡Urgente! Tu cuenta ha sido bloqueada. Haz clic aquí...",
        analyzeBtn: "Analizar Mensaje",
        analyzing: "Analizando...",
        keywordAnalysis: "🔍 Análisis de palabras clave:",
        disclaimer: "⚠️ Nota: Esta IA es una herramienta orientativa. Resultados no 100% precisos.",
        spamDetected: "SPAM DETECTADO",
        safeMessage: "MENSAJE SEGURO",
        confidence: "Confianza del modelo",
        error: "Error conectando con el servidor. Asegúrate de que 'api.py' esté ejecutándose.",
        emptyAlert: "Por favor escribe algo.",
        patterns: "Patrones técnicos detectados:"
    },
    en: {
        title: "🛡️ AI Spam Hunter",
        subtitle: "Insert a message to analyze with Artificial Intelligence",
        placeholder: "Ex: Urgent! Your account has been locked. Click here...",
        analyzeBtn: "Analyze Message",
        analyzing: "Analyzing...",
        keywordAnalysis: "🔍 Keyword Analysis:",
        disclaimer: "⚠️ Note: This AI is for guidance only. Results not 100% accurate.",
        spamDetected: "SPAM DETECTED",
        safeMessage: "SAFE MESSAGE",
        confidence: "Model Confidence",
        error: "Error connecting to server. Ensure 'api.py' is running.",
        emptyAlert: "Please write something.",
        patterns: "Technical patterns detected:"
    }
};

let currentLang = localStorage.getItem('lang') || 'es';

document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const messageInput = document.getElementById('messageInput');
    const langBtn = document.getElementById('langBtn');

    updateLanguage(currentLang);

    langBtn.addEventListener('click', () => {
        currentLang = currentLang === 'es' ? 'en' : 'es';
        localStorage.setItem('lang', currentLang);
        updateLanguage(currentLang);
    });

    messageInput.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') checkSpam();
    });

    analyzeBtn.addEventListener('click', checkSpam);
});

function updateLanguage(lang) {
    const t = translations[lang];
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (t[key]) el.innerText = t[key];
    });
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (t[key]) el.placeholder = t[key];
    });
    document.getElementById('langBtn').innerText = lang === 'es' ? '🇺🇸 EN' : '🇪🇸 ES';
}

async function checkSpam() {
    const textInput = document.getElementById('messageInput');
    const resultArea = document.getElementById('result-area');
    const text = textInput.value;
    const t = translations[currentLang];

    if (!text.trim()) {
        shakeInput(textInput);
        textInput.focus();
        return;
    }

    setLoading(true);
    resultArea.style.display = 'none';

    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const data = await response.json();
        displayResult(data);

    } catch (error) {
        console.error("Error:", error);
        alert(t.error);
    } finally {
        setLoading(false);
    }
}

function setLoading(isLoading) {
    const btn = document.getElementById('analyzeBtn');
    const span = btn.querySelector('span'); // Asegúrate de que tu HTML tenga un <span> dentro del botón
    const spinner = document.querySelector('.spinner'); // Y un div con clase spinner
    const t = translations[currentLang];

    if (isLoading) {
        btn.disabled = true;
        if (span) span.innerText = t.analyzing;
        if (spinner) spinner.style.display = 'block';
    } else {
        btn.disabled = false;
        if (span) span.innerText = t.analyzeBtn;
        if (spinner) spinner.style.display = 'none';
    }
}

function displayResult(data) {
    console.log("📡 Datos recibidos de Python:", data);
    console.log("🔥 Palabras culpables:", data.spam_words);
    const resultArea = document.getElementById('result-area');
    const title = document.getElementById('result-title');
    const desc = document.getElementById('result-desc');
    const bar = document.getElementById('score-fill');
    const explanationContainer = document.getElementById('explanation-container');
    const explainedText = document.getElementById('explained-text');
    const messageInput = document.getElementById('messageInput');
    const t = translations[currentLang];

    resultArea.style.display = 'block';

    // Limpiamos clases previas
    resultArea.className = '';
    explanationContainer.style.display = 'none';

    if (data.is_spam) {
        resultArea.classList.add('result-spam'); // Necesitas CSS para esto
        title.innerHTML = `🚨 ${t.spamDetected}`;
        title.style.color = "var(--spam-color)";
        bar.style.backgroundColor = "var(--spam-color)";

        // --- LÓGICA DE RESALTADO MEJORADA ---
        if (data.spam_words && data.spam_words.length > 0) {
            let originalText = messageInput.value;
            // Sanitizar HTML básico para evitar inyecciones
            let htmlContent = originalText.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

            // 1. Separar Tokens (__TOKEN__) de Palabras normales
            const tokens = data.spam_words.filter(w => w.startsWith("__"));
            const words = data.spam_words.filter(w => !w.startsWith("__"));

            // 2. Resaltar palabras normales en el texto
            // Ordenamos por longitud para reemplazar primero las frases largas
            words.sort((a, b) => b.length - a.length);

            words.forEach(word => {
                const escapedWord = word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
                const regex = new RegExp(`\\b(${escapedWord})\\b`, 'gi');
                htmlContent = htmlContent.replace(regex, '<span class="highlight-spam">$1</span>');
            });

            // 3. Añadir los tokens técnicos al final (si los hay)
            if (tokens.length > 0) {
                htmlContent += `<br><br><div class="tokens-area"><small>${t.patterns}</small><br>`;
                tokens.forEach(token => {
                    // Limpiar el token visualmente: __TIENE_DINERO__ -> TIENE DINERO
                    const readable = token.replace(/__/g, '').replace(/_/g, ' ');
                    htmlContent += `<span class="highlight-token">${readable}</span> `;
                });
                htmlContent += `</div>`;
            }

            explainedText.innerHTML = htmlContent;
            explanationContainer.style.display = 'block';
        } else {
            // Si es spam pero no devolvió palabras clave
            explainedText.innerHTML = messageInput.value + "<br><br><em>(Patrón complejo detectado)</em>";
            explanationContainer.style.display = 'block';
        }

    } else {
        resultArea.classList.add('result-ham'); // Necesitas CSS para esto
        title.innerHTML = `✅ ${t.safeMessage}`;
        title.style.color = "var(--ham-color)";
        bar.style.backgroundColor = "var(--ham-color)";
    }

    desc.innerText = `${t.confidence}: ${data.confidence}%`;

    // Animación barra
    bar.style.width = '0%';
    setTimeout(() => { bar.style.width = `${data.confidence}%`; }, 100);
}

function shakeInput(element) {
    element.animate([
        { transform: 'translateX(0)' }, { transform: 'translateX(-10px)' },
        { transform: 'translateX(10px)' }, { transform: 'translateX(0)' }
    ], { duration: 300 });
}
