import os
import logging
from functools import wraps
from flask import Flask, render_template_string, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from markupsafe import escape
from google import genai
from google.genai import types
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Security configuration
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- [SECURE API KEYS FROM ENVIRONMENT] ---
GEMINI_KEY = os.getenv('GEMINI_API_KEY')
OPENAI_KEY = os.getenv('OPENAI_API_KEY')
MASTER_NAME = os.getenv('MASTER_NAME', 'System Administrator')
SECRET_KEY = os.getenv('SECRET_KEY', 'change-me-in-production')

# Validate API keys are configured
if not GEMINI_KEY or not OPENAI_KEY:
    logger.error("CRITICAL: API keys not configured. Set GEMINI_API_KEY and OPENAI_API_KEY environment variables.")
    raise ValueError("Missing required API keys. Check your .env file.")

# Initialize AI clients
try:
    gemini_client = genai.Client(api_key=GEMINI_KEY)
    openai_client = OpenAI(api_key=OPENAI_KEY)
except Exception as e:
    logger.error(f"Failed to initialize AI clients: {str(e)}")
    raise

# --- [SECURE SYSTEM ARCHITECTURE] ---
SYSTEM_PROMPT = f"""
Identity: MARCO V50 SECURE (Production Edition).
Master: {escape(MASTER_NAME)}.
Personality: High-Intelligence Digital Entity. Witty, precise, and human-like.
Directives:
1. Secure operation with validated inputs.
2. Mix Google AI Studio's technical depth with practical functionality.
3. Handle Trading, Shopify, Cyber Security, and App Dev with expert logic.
4. Voice Command: Respond to 'MARCO' and deactivate on 'STOP MARCO'.
5. Rate-limited to prevent abuse.
6. All inputs validated and sanitized.
"""

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'">
    <title>MARCO V50 // SECURE</title>
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="mobile-web-app-capable" content="yes">
    <style>
        :root { --cyan: #00ffcc; --bg: #050505; --panel: #0d0d0d; --text: #e0e0e0; }
        * { box-sizing: border-box; }
        body { background: var(--bg); color: var(--text); font-family: 'Consolas', monospace; margin: 0; display: flex; height: 100vh; overflow: hidden; }

        /* Sidebar - Google AI Studio Remix Style */
        .sidebar { width: 300px; background: var(--panel); border-right: 1px solid #1a1a1a; padding: 25px; display: flex; flex-direction: column; }
        .sidebar h1 { color: var(--cyan); font-size: 22px; margin: 0; letter-spacing: 3px; }
        .status { font-size: 10px; color: #444; margin-bottom: 30px; border-bottom: 1px solid #222; padding-bottom: 10px; }
        
        .menu { flex: 1; list-style: none; padding: 0; font-size: 13px; }
        .menu li { padding: 12px 0; color: #666; cursor: pointer; transition: 0.3s; }
        .menu li:hover, .menu li.active { color: var(--cyan); text-shadow: 0 0 10px var(--cyan); }

        /* Main Workspace */
        .workspace { flex: 1; display: flex; flex-direction: column; }
        .top-dash { height: 60px; border-bottom: 1px solid #1a1a1a; display: flex; align-items: center; padding: 0 25px; gap: 30px; font-size: 11px; }
        .top-dash span { color: var(--cyan); }

        #chat { flex: 1; overflow-y: auto; padding: 30px; display: flex; flex-direction: column; gap: 20px; }
        .block { animation: slideIn 0.4s ease; border-left: 2px solid #222; padding-left: 15px; }
        .role { font-size: 10px; color: var(--cyan); font-weight: bold; margin-bottom: 5px; }
        .content { font-size: 15px; color: #bbb; line-height: 1.5; word-break: break-word; }

        /* Assistant-like Input */
        .footer { padding: 25px; background: linear-gradient(transparent, var(--bg)); }
        .input-wrap { background: #111; border: 1px solid #222; border-radius: 8px; display: flex; padding: 10px 20px; align-items: center; }
        input { flex: 1; background: transparent; border: none; color: #fff; outline: none; font-size: 16px; font-family: inherit; }
        input::placeholder { color: #444; }
        .mic { color: var(--cyan); font-size: 22px; cursor: pointer; margin-right: 15px; transition: 0.3s; }
        .mic.active { color: #ff3b3b; text-shadow: 0 0 15px red; }
        button { background: var(--cyan); border: none; padding: 8px 20px; font-weight: bold; cursor: pointer; border-radius: 4px; color: #000; }
        button:hover { background: #00e6b8; }

        @keyframes slideIn { from { opacity: 0; transform: translateX(-10px); } to { opacity: 1; transform: translateX(0); } }
        pre { background: #000; padding: 15px; border-radius: 5px; border: 1px solid #222; color: #00ffaa; overflow-x: auto; font-size: 12px; }
        .error { color: #ff6b6b; }
    </style>
</head>
<body>
    <div class="sidebar">
        <h1>MARCO</h1>
        <div class="status">V50 // SECURE_EDITION</div>
        <ul class="menu">
            <li class="active">> TERMINAL</li>
            <li>> NEURAL SCAN</li>
            <li>> SECURITY</li>
            <li>> LIVE ASSISTANT</li>
            <li>> ASSET SYNC</li>
        </ul>
        <div style="border: 1px solid var(--cyan); padding: 10px; background: rgba(0,255,204,0.01);">
            <div style="font-size: 9px; color: #555;">SYSTEM MASTER</div>
            <div style="color: var(--cyan); font-weight: bold;" id="master-name">System Admin</div>
        </div>
    </div>

    <div class="workspace">
        <div class="top-dash">
            <div>STATUS: <span>ACTIVE</span></div>
            <div>SYNC: <span id="sync">92.4%</span></div>
            <div>LOAD: <span id="load">12%</span></div>
            <div style="margin-left:auto; color: var(--cyan);">MARCO_SECURE_LINK</div>
        </div>

        <div id="chat">
            <div class="block">
                <div class="role">MARCO_SYSTEM</div>
                <div class="content">Neural link established 100%. System ready for secure commands. Rate limit: 5 requests/minute.</div>
            </div>
        </div>

        <div class="footer">
            <div class="input-wrap">
                <div id="mic-btn" class="mic" onclick="toggleVoice()">🎙</div>
                <input type="text" id="user-in" maxlength="5000" placeholder="Say 'MARCO' or Type Command..." onkeypress="if(event.key==='Enter') send()">
                <button onclick="send()">RUN</button>
            </div>
            <div style="text-align:center; font-size:9px; color:#222; margin-top:8px;">POWERED BY MARCO SECURE CORE // PRODUCTION READY</div>
        </div>
    </div>

    <script>
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.continuous = true;
        recognition.lang = 'en-US';
        let listening = false;
        let requestCount = 0;
        let lastRequestTime = Date.now();

        function speak(t) {
            window.speechSynthesis.cancel();
            const s = new SpeechSynthesisUtterance(t);
            s.pitch = 0.9; s.rate = 1.0;
            window.speechSynthesis.speak(s);
        }

        function sanitizeHTML(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        recognition.onresult = (e) => {
            const text = e.results[e.results.length - 1][0].transcript.trim().toLowerCase();
            if (text.includes("marco")) {
                speak("Yes, I am listening.");
                document.getElementById('mic-btn').classList.add('active');
            } else if (text.includes("stop marco")) {
                speak("Going to standby mode.");
                document.getElementById('mic-btn').classList.remove('active');
            } else {
                send(text);
            }
        };

        async function send(manual) {
            const input = document.getElementById('user-in'), chat = document.getElementById('chat');
            const val = manual || input.value;
            if(!val || val.trim() === '') return;
            if(val.length > 5000) {
                alert('Message too long (max 5000 characters)');
                return;
            }

            chat.innerHTML += `<div class="block"><div class="role">USER</div><div class="content">${sanitizeHTML(val)}</div></div>`;
            input.value = "";
            chat.scrollTop = chat.scrollHeight;

            try {
                const res = await fetch('/ask', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({prompt: val})
                });
                const d = await res.json();
                
                if (!res.ok) {
                    chat.innerHTML += `<div class="block error"><div class="role">MARCO_ERROR</div><div class="content">${sanitizeHTML(d.reply || 'An error occurred')}</div></div>`;
                } else {
                    let formatted = d.reply.replace(/```([\s\S]*?)```/g, '<pre>$1</pre>');
                    chat.innerHTML += `<div class="block"><div class="role">MARCO_RESPONSE</div><div class="content">${formatted}</div></div>`;
                    speak(d.reply.replace(/<[^>]*>?/gm, '').substring(0, 500));
                }
            } catch (error) {
                chat.innerHTML += `<div class="block error"><div class="role">MARCO_ERROR</div><div class="content">Connection error. Please try again.</div></div>`;
            }
            chat.scrollTop = chat.scrollHeight;
        }

        function toggleVoice() {
            try { 
                recognition.start(); 
                document.getElementById('mic-btn').classList.add('active'); 
            } catch(e) {
                console.error('Voice recognition not available');
            }
        }

        setInterval(() => {
            document.getElementById('sync').innerText = (90 + Math.random() * 5).toFixed(1) + "%";
            document.getElementById('load').innerText = Math.floor(Math.random() * 15 + 10) + "%";
        }, 3000);
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_template)

@app.route('/ask', methods=['POST'])
@limiter.limit("5 per minute")
def ask():
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"reply": "Invalid request format"}), 400
        
        user_input = data['prompt'].strip()
        
        # Validate input
        if not user_input:
            return jsonify({"reply": "Empty input"}), 400
        if len(user_input) > 5000:
            return jsonify({"reply": "Input too long (max 5000 characters)"}), 400
        
        logger.info(f"Processing request from {request.remote_addr}")
        
        # GPT-4o logic
        gpt_res = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ],
            max_tokens=1000
        )
        
        # Gemini 2.0 Fusion
        gem_res = gemini_client.models.generate_content(
            model='gemini-2.0-flash',
            contents=f"Command: {user_input}. Context: {gpt_res.choices[0].message.content}. Provide a comprehensive response.",
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
        )
        
        logger.info("Request processed successfully")
        return jsonify({"reply": gem_res.text})
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({"reply": "System error: Unable to process your request. Please try again."}), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    logger.warning(f"Rate limit exceeded for {request.remote_addr}")
    return jsonify({"reply": "Too many requests. Please wait a moment."}), 429

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal server error: {str(e)}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    if os.getenv('FLASK_ENV') == 'production':
        logger.info(">>> MARCO SECURE EDITION DEPLOYED - PRODUCTION MODE")
        from waitress import serve
        serve(app, host='0.0.0.0', port=port)
    else:
        logger.info(">>> MARCO SECURE EDITION RUNNING - DEVELOPMENT MODE")
        app.run(debug=False, host='0.0.0.0', port=port)
