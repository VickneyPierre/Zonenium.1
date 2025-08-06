from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os

app = FastAPI(title="Zonenium", description="WhatsApp-like messaging app")

@app.get("/")
def read_root():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Zonenium - Free Messaging App</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
                background: rgba(255,255,255,0.1);
                border-radius: 20px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            }
            .logo-text { 
                font-size: 3.5em; 
                font-weight: 800;
                margin-bottom: 20px;
                background: linear-gradient(45deg, #3182ce, #10b981, #f59e0b);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                letter-spacing: -2px;
                text-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }
            .subtitle {
                font-size: 1.2em;
                margin-bottom: 30px;
                opacity: 0.9;
            }
            .features {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin: 30px 0;
                text-align: left;
            }
            .feature {
                padding: 15px;
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
            }
            .cta-button {
                display: inline-block;
                padding: 15px 30px;
                background: #10b981;
                color: white;
                text-decoration: none;
                border-radius: 50px;
                font-weight: 600;
                font-size: 1.1em;
                margin: 20px 10px;
                transition: transform 0.2s;
            }
            .cta-button:hover {
                transform: translateY(-2px);
            }
            .install-note {
                margin-top: 30px;
                font-size: 0.9em;
                opacity: 0.8;
            }
            @media (max-width: 600px) {
                .features { grid-template-columns: 1fr; }
                .logo-text { font-size: 2.8em; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo-text">Zonenium</div>
            <p class="subtitle">🚀 Free WhatsApp Alternative</p>
            
            <div class="features">
                <div class="feature">
                    <h3>🎤 Voice Messages</h3>
                    <p>Record and send voice messages instantly</p>
                </div>
                <div class="feature">
                    <h3>📁 File Sharing</h3>
                    <p>Share photos, documents, and media</p>
                </div>
                <div class="feature">
                    <h3>⚡ Real-time Chat</h3>
                    <p>Lightning-fast messaging experience</p>
                </div>
                <div class="feature">
                    <h3>📱 Works Everywhere</h3>
                    <p>Install on any device like a native app</p>
                </div>
            </div>
            
            <a href="/docs" class="cta-button">🚀 Try Demo</a>
            <a href="/api/status" class="cta-button">📊 API Status</a>
            
            <div class="install-note">
                📱 <strong>Install as App:</strong> Add to home screen for the best experience!<br>
                🌐 <strong>Domain:</strong> zonenium.top<br>
                ✅ <strong>Status:</strong> Live and running!
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
        "domain": "zonenium.top"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
