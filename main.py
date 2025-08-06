from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
def home():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Zonenium</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { 
                background: linear-gradient(135deg, #1e3a8a, #3730a3); 
                color: white; 
                text-align: center; 
                padding: 20px; 
                font-family: Arial; 
                min-height: 100vh; 
                display: flex; 
                align-items: center; 
                justify-content: center; 
                margin: 0; 
            }
            .container { 
                background: rgba(255,255,255,0.1); 
                padding: 40px; 
                border-radius: 20px; 
                backdrop-filter: blur(10px); 
                max-width: 400px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            }
            h1 { 
                color: #60a5fa; 
                font-size: 3em; 
                margin-bottom: 20px; 
                font-weight: bold;
            }
            .feature {
                font-size: 1.1em;
                margin: 15px 0;
                padding: 10px;
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
            }
            .btn { 
                background: linear-gradient(45deg, #10b981, #3b82f6); 
                color: white; 
                border: none; 
                padding: 15px 30px; 
                border-radius: 25px; 
                font-size: 1.1em; 
                cursor: pointer; 
                margin: 20px 0;
                font-weight: bold;
            }
            .status {
                background: rgba(16, 185, 129, 0.2);
                border: 1px solid rgba(16, 185, 129, 0.3);
                border-radius: 15px;
                padding: 15px;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Zonenium</h1>
            <p style="font-size: 1.3em; margin: 20px 0;">🚀 Free WhatsApp Alternative</p>
            
            <div class="feature">🎤 Voice Messages</div>
            <div class="feature">📁 File Sharing</div>
            <div class="feature">⚡ Real-time Chat</div>
            <div class="feature">📱 Install as App</div>
            
            <button class="btn" onclick="alert('Add to home screen to install!')">📱 Install Zonenium</button>
            
            <div class="status">
                <strong>✅ App is Live & Working!</strong><br>
                🌐 zozenium.top<br>
                📊 All systems operational
            </div>
        </div>
    </body>
    </html>
    """)

@app.get("/api/status")
def status():
    return {
        "status": "live", 
        "app": "zozenium", 
        "message": "🎉 Working perfectly!",
        "domain": "zozenium.top"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
