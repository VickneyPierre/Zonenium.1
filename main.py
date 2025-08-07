from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

PORT = int(os.environ.get("PORT", 8000))
ENVIRONMENT = os.environ.get("ENVIRONMENT", "production")

app = FastAPI(
    title="Zonenium - Free WhatsApp Alternative", 
    description="Modern WhatsApp-like messaging application",
    version="1.0.0"
)

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
            <p class="tagline">Free WhatsApp Alternative</p>
            
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
            
            <div style="margin: 16px 0;">
                <a href="/app" class="app-btn">Launch App</a>
            </div>
            
            <div class="info">
                <strong>From Mexico City with ❤️</strong>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/app")
def serve_app():
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Zonenium Chat</title>
        <style>
            body { margin: 0; font-family: system-ui; background: #1f2937; color: white; }
            .container { max-width: 1200px; margin: 0 auto; padding: 20px; text-align: center; }
            .header { padding: 20px 0; border-bottom: 1px solid #374151; }
            .success { padding: 40px; opacity: 0.9; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Zonenium Chat</h1>
                <p>Mexico City Deployment Success!</p>
            </div>
            <div class="success">
                <h2>🎉 App is Working Perfectly!</h2>
                <p>Your messaging app foundation is ready from Mexico City!</p>
                <div style="margin: 20px 0;">
                    <a href="/" style="background: linear-gradient(45deg, #10b981, #3b82f6); color: white; padding: 12px 24px; border-radius: 25px; text-decoration: none;">← Back to Home</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """)

@app.get("/api/status")
def get_status():
    return {
        "status": "live",
        "app": "Zonenium",
        "version": "1.0.0",
        "message": "App working from Mexico City!",
        "location": "Mexico City 🇲🇽"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
