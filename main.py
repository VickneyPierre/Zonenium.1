from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os

app = FastAPI(title="Zonenium", description="Messaging App")

@app.get("/")
def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Zonenium - Messaging App</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="theme-color" content="#3182ce">
        <link rel="manifest" href="/manifest.json">
    </head>
    <body style="font-family: Arial; text-align: center; padding: 50px; background: #1a202c; color: white;">
        <div style="max-width: 500px; margin: auto; padding: 30px; background: rgba(255,255,255,0.1); border-radius: 20px;">
            <h1 style="font-size: 3em; color: #3182ce; margin: 0;">Zonenium</h1>
            <p style="font-size: 1.2em; margin: 20px 0;">Free WhatsApp Alternative</p>
            
            <div style="margin: 30px 0;">
                <h2>🎤 Voice Messages</h2>
                <h2>📁 File Sharing</h2>
                <h2>⚡ Real-time Chat</h2>
                <h2>📱 Works on Mobile</h2>
            </div>
            
            <button onclick="installApp()" 
                style="padding: 15px 30px; background: #10b981; color: white; border: none; border-radius: 25px; font-size: 1.1em; cursor: pointer;">
                📱 Install App
            </button>
            
            <p style="margin-top: 30px; font-size: 0.9em; opacity: 0.8;">
                Add to home screen for the best experience!<br>
                🌐 zonenium.top
            </p>
        </div>
        
        <script>
            let deferredPrompt;
            
            window.addEventListener('beforeinstallprompt', (e) => {
                deferredPrompt = e;
                document.querySelector('button').style.display = 'block';
            });
            
            function installApp() {
                if (deferredPrompt) {
                    deferredPrompt.prompt();
                    deferredPrompt.userChoice.then((result) => {
                        if (result.outcome === 'accepted') {
                            console.log('PWA installed');
                        }
                        deferredPrompt = null;
                    });
                } else {
                    alert('To install: Use browser menu → "Add to Home Screen"');
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(html)

@app.get("/manifest.json")
def manifest():
    return {
        "name": "Zonenium",
        "short_name": "Zonenium",
        "description": "Free WhatsApp alternative",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#1a202c",
        "theme_color": "#3182ce",
        "icons": [
            {
                "src": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='50' r='40' fill='%233182ce'/%3E%3Ctext x='50' y='60' text-anchor='middle' fill='white' font-size='30' font-family='Arial'%3EZ%3C/text%3E%3C/svg%3E",
                "sizes": "192x192",
                "type": "image/svg+xml"
            }
        ]
    }

@app.get("/api/status")
def status():
    return {"status": "live", "app": "Zonenium"}
