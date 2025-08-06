from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="Zonenium", description="WhatsApp-like messaging app")

# Serve static files (if you have a static directory)
# app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Zonenium - Free Messaging App</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="icon" type="image/png" href="https://raw.githubusercontent.com/VickneyPierre/Zonenium.1/main/zonenium-logo.png">
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
                color: white; 
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }
            .container {
                text-align: center;
                max-width: 600px;
                padding: 40px;
                background: rgba(255,255,255,0.05);
                border-radius: 20px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
                border: 1px solid rgba(255,255,255,0.1);
            }
            .logo-img {
                width: 120px;
                height: 120px;
                margin-bottom: 20px;
                border-radius: 20px;
                box-shadow: 0 8px 25px rgba(49, 130, 206, 0.3);
                object-fit: contain;
            }
            .title {
                font-size: 3em;
                margin-bottom: 10px;
                font-weight: 800;
                background: linear-gradient(45deg, #3182ce, #10b981);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            .subtitle {
                font-size: 1.3em;
                margin-bottom: 30px;
                opacity: 0.9;
                color: #a0aec0;
            }
            .features {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin: 30px 0;
                text-align: left;
            }
            .feature {
                padding: 20px;
                background: rgba(49, 130, 206, 0.1);
                border-radius: 12px;
                border: 1px solid rgba(49, 130, 206, 0.2);
            }
            .feature h3 {
                margin-top: 0;
                color: #3182ce;
            }
            .cta-button {
                display: inline-block;
                padding: 15px 30px;
                background: linear-gradient(45deg, #3182ce, #10b981);
                color: white;
                text-decoration: none;
                border-radius: 50px;
                font-weight: 600;
                font-size: 1.1em;
                margin: 20px 10px;
                transition: all 0.3s;
                box-shadow: 0 4px 15px rgba(49, 130, 206, 0.3);
            }
            .cta-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(49, 130, 206, 0.4);
            }
            .install-note {
                margin-top: 30px;
                font-size: 0.95em;
                opacity: 0.8;
                padding: 20px;
                background: rgba(16, 185, 129, 0.1);
                border-radius: 12px;
                border: 1px solid rgba(16, 185, 129, 0.2);
            }
            @media (max-width: 600px) {
                .features { grid-template-columns: 1fr; }
                .title { font-size: 2.2em; }
                .logo-img { width: 100px; height: 100px; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <img src="https://raw.githubusercontent.com/VickneyPierre/Zonenium.1/main/zonenium-logo.png" 
                 alt="Zonenium Logo" class="logo-img" 
                 onerror="this.style.display='none'; document.querySelector('.title').style.marginTop='20px';">
            <h1 class="title">Zonenium</h1>
            <p class="subtitle">🚀 The Future of Messaging</p>
            
            <div class="features">
                <div class="feature">
                    <h3>🎤 Voice Messages</h3>
                    <p>Crystal clear voice messages with waveform visualization</p>
                </div>
                <div class="feature">
                    <h3>📁 Smart File Sharing</h3>
                    <p>Share any file type with preview and progress tracking</p>
                </div>
                <div class="feature">
                    <h3>⚡ Real-time Chat</h3>
                    <p>Lightning-fast messaging with typing indicators</p>
                </div>
                <div class="feature">
                    <h3>🌍 Multi-language</h3>
                    <p>Available in 6 languages with RTL support</p>
                </div>
            </div>
            
            <a href="/docs" class="cta-button">🚀 Explore API</a>
            <a href="/api/status" class="cta-button">📊 System Status</a>
            
            <div class="install-note">
                <strong>📱 Install as Native App</strong><br>
                Add Zonenium to your home screen for the full experience!<br>
                <small>🌐 zonenium.top • ✅ PWA Ready • 🔒 Secure</small>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/api/status")
def get_status():
    return {
        "status": "healthy",
        "app": "Zonenium", 
        "version": "1.0.0",
        "message": "🎉 Zonenium is live!",
        "domain": "zonenium.top",
        "branding": "official_logo"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
