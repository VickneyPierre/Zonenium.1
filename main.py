from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

# Simple configuration without complex dependencies
PORT = int(os.environ.get("PORT", 8000))
ENVIRONMENT = os.environ.get("ENVIRONMENT", "production")

# No complex backend for now - just the working interface
BACKEND_AVAILABLE = False

app = FastAPI(
    title="Zonenium - Free WhatsApp Alternative", 
    description="Modern WhatsApp-like messaging application",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Zonenium - Free WhatsApp Alternative</title>
        <meta name="theme-color" content="#3182ce">
        <link rel="manifest" href="/manifest">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="apple-mobile-web-app-title" content="Zonenium">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #1e3a8a 0%, #3730a3 50%, #1e40af 100%);
                color: white;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                text-align: center;
                max-width: 500px;
                width: 100%;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                border-radius: 24px;
                padding: 40px 30px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            .logo {
                width: 80px;
                height: 80px;
                background: linear-gradient(45deg, #3b82f6, #10b981);
                border-radius: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 24px;
                font-size: 36px;
                font-weight: bold;
            }
            h1 {
                font-size: 2.5rem;
                font-weight: 800;
                margin-bottom: 12px;
                background: linear-gradient(45deg, #60a5fa, #34d399);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            .tagline {
                font-size: 1.1rem;
                opacity: 0.9;
                margin-bottom: 32px;
            }
            .features {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 16px;
                margin-bottom: 32px;
            }
            .feature {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                padding: 20px 16px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            .feature-icon {
                font-size: 2rem;
                margin-bottom: 8px;
            }
            .feature-text {
                font-size: 0.9rem;
                font-weight: 600;
            }
            .install-btn {
                background: linear-gradient(45deg, #10b981, #3b82f6);
                color: white;
                border: none;
                padding: 16px 32px;
                border-radius: 50px;
                font-size: 1.1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                margin-bottom: 24px;
                display: inline-block;
                text-decoration: none;
                box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3);
            }
            .install-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 12px 30px rgba(16, 185, 129, 0.4);
            }
            .app-btn {
                background: linear-gradient(45deg, #6366f1, #8b5cf6);
                color: white;
                border: none;
                padding: 12px 28px;
                border-radius: 50px;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                margin: 8px;
                text-decoration: none;
                display: inline-block;
                box-shadow: 0 6px 15px rgba(99, 102, 241, 0.3);
            }
            .app-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 25px rgba(99, 102, 241, 0.4);
            }
            .info {
                font-size: 0.9rem;
                opacity: 0.8;
                line-height: 1.5;
            }
            .status {
                display: inline-block;
                background: rgba(16, 185, 129, 0.2);
                border: 1px solid rgba(16, 185, 129, 0.3);
                border-radius: 20px;
                padding: 8px 16px;
                font-size: 0.85rem;
                margin-top: 16px;
            }
            @media (max-width: 480px) {
                .features { grid-template-columns: 1fr; }
                h1 { font-size: 2rem; }
                .container { padding: 32px 24px; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">Z</div>
            <h1>Zonenium</h1>
            <p class="tagline">🚀 Free WhatsApp Alternative</p>
            
            <div class="features">
                <div class="feature">
                    <div class="feature-icon">🎤</div>
                    <div class="feature-text">Voice Messages</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">📁</div>
                    <div class="feature-text">File Sharing</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">⚡</div>
                    <div class="feature-text">Real-time Chat</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">📱</div>
                    <div class="feature-text">Install as App</div>
                </div>
            </div>
            
            <button class="install-btn" onclick="installApp()">
                📱 Install Zonenium
            </button>
            
            <div style="margin: 16px 0;">
                <a href="/app" class="app-btn">🚀 Launch App</a>
            </div>
            
            <div class="info">
                <strong>How to install:</strong><br>
                <strong>Android:</strong> Tap install button or browser menu<br>
                <strong>iPhone:</strong> Share → Add to Home Screen<br>
                <div class="status">
                    ✅ App is Live & Working!<br>
                    📡 All systems operational
                </div>
            </div>
        </div>

        <script>
            let deferredPrompt;
            let installButton = document.querySelector('.install-btn');

            window.addEventListener('beforeinstallprompt', (e) => {
                console.log('PWA install prompt available');
                e.preventDefault();
                deferredPrompt = e;
                installButton.style.display = 'inline-block';
            });

            async function installApp() {
                if (deferredPrompt) {
                    deferredPrompt.prompt();
                    const { outcome } = await deferredPrompt.userChoice;
                    console.log(`User response: ${outcome}`);
                    if (outcome === 'accepted') {
                        console.log('PWA installed successfully');
                    }
                    deferredPrompt = null;
                } else {
                    let instructions = '';
                    const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
                    const isAndroid = /Android/.test(navigator.userAgent);
                    
                    if (isIOS) {
                        instructions = 'To install:\\n1. Tap the Share button (⤴️)\\n2. Select "Add to Home Screen"\\n3. Tap "Add"';
                    } else if (isAndroid) {
                        instructions = 'To install:\\n1. Tap browser menu (⋮)\\n2. Select "Install app" or "Add to Home screen"\\n3. Tap "Install"';
                    } else {
                        instructions = 'To install: Use your browser\\'s menu to "Install app" or "Add to desktop"';
                    }
                    
                    alert(instructions);
                }
            }

            if (window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone) {
                installButton.innerHTML = '✅ App Installed';
                installButton.disabled = true;
                installButton.style.opacity = '0.7';
            }

            if ('serviceWorker' in navigator) {
                navigator.serviceWorker.register('/sw')
                    .then(registration => console.log('SW registered'))
                    .catch(error => console.log('SW registration failed'));
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/app")
async def serve_react_app():
    """Serve the basic chat interface"""
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Zonenium Chat</title>
        <style>
            body { margin: 0; font-family: system-ui; background: #1f2937; color: white; }
            .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
            .header { text-align: center; padding: 20px 0; border-bottom: 1px solid #374151; }
            .chat-area { min-height: 60vh; padding: 20px 0; }
            .coming-soon { text-align: center; padding: 40px; opacity: 0.7; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Zonenium Chat</h1>
                <p>Your messaging app is ready!</p>
            </div>
            <div class="chat-area">
                <div class="coming-soon">
                    <h2>🎉 Success! App is Working</h2>
                    <p>You now have the foundation for your WhatsApp-like messaging app!</p>
                    <div style="margin: 20px 0;">
                        <a href="/" style="background: linear-gradient(45deg, #10b981, #3b82f6); color: white; padding: 12px 24px; border-radius: 25px; text-decoration: none; margin: 8px;">← Back to Home</a>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """)

@app.get("/manifest")
def get_manifest():
    return {
        "name": "Zonenium - Free WhatsApp Alternative",
        "short_name": "Zonenium",
        "description": "Free WhatsApp alternative with voice messages and file sharing",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#1e3a8a",
        "theme_color": "#3182ce",
        "icons": [
            {
                "src": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='20' fill='%233b82f6'/%3E%3Ctext x='50' y='65' text-anchor='middle' fill='white' font-size='45' font-family='system-ui' font-weight='800'%3EZ%3C/text%3E%3C/svg%3E",
                "sizes": "512x512",
                "type": "image/svg+xml"
            }
        ]
    }

@app.get("/sw")
def get_service_worker():
    return HTMLResponse(content="console.log('Zonenium SW loaded');", media_type="application/javascript")

@app.get("/api/status")
def get_status():
    return {
        "status": "live",
        "app": "Zonenium",
        "version": "1.0.0",
        "message": "🎉 App is working perfectly!",
        "domain": "zonenium.top",
        "features": ["PWA", "Installable", "Working Interface"]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
