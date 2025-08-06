from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
def home():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Zozenium</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { background: linear-gradient(135deg, #1e3a8a, #3730a3); color: white; 
                   text-align: center; padding: 50px; font-family: Arial; min-height: 100vh; 
                   display: flex; align-items: center; justify-content: center; margin: 0; }
            .container { background: rgba(255,255,255,0.1); padding: 40px; border-radius: 20px; 
                        backdrop-filter: blur(10px); max-width: 400px; }
            h1 { color: #60a5fa; font-size: 3em; margin-bottom: 20px; }
            .btn { background: linear-gradient(45deg, #10b981, #3b82f6); color: white; 
                   border: none; padding: 15px 30px; border-radius: 25px; font-size: 1.1em; 
                   cursor: pointer; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Zozenium</h1>
            <p style="font-size: 1.2em; margin: 20px 0;">🚀 Free WhatsApp Alternative</p>
            <div style="margin: 30px 0;">
                <p>🎤 Voice Messages</p>
                <p>📁 File Sharing</p>
                <p>⚡ Real-time Chat</p>
                <p>📱 Install as App</p>
            </div>
            <button class="btn">📱 Coming Soon!</button>
            <p style="font-size: 0.9em; margin-top: 30px;">✅ App is Live<br>🌐 zozenium.top</p>
        </div>
    </body>
    </html>
    """)

@app.get("/api/status")
def status():
    return {"status": "live", "app": "zozenium", "message": "Working perfectly!"}
