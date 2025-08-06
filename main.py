from fastapi import FastAPI, HTTPException, Depends, status, File, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import socketio
import os
import sys
import base64
from datetime import datetime, timedelta
from typing import Optional, List
from jose import JWTError, jwt
from passlib.context import CryptContext

# Add backend directory to path to import modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

try:
    # Import models and database from backend
    from models import (
        StatusCheck, User, UserCreate, UserLogin, Token, TokenData, UserResponse,
        Message, MessageCreate, Chat, ChatListResponse, MessageListResponse,
        GroupCreateRequest, GroupUpdateRequest, GroupMemberAction, GroupInfo
    )
    from database import db
    from socket_manager import socket_manager
    BACKEND_AVAILABLE = True
except ImportError as e:
    print(f"Backend modules not available: {e}")
    BACKEND_AVAILABLE = False

# Railway/Production configuration
PORT = int(os.environ.get("PORT", 8001))  # Default to 8001 for production
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
ENVIRONMENT = os.environ.get("ENVIRONMENT", "production")

# CORS origins from environment
CORS_ORIGINS = os.environ.get(
    "CORS_ORIGINS", 
    "http://localhost:3000,http://localhost:3001,https://zonenium.top,https://www.zonenium.top,https://zonenium-1.onrender.com"
).split(",")

# Security setup
SECRET_KEY = os.getenv("SECRET_KEY", "zonenium-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

if BACKEND_AVAILABLE:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print(f"🚀 Starting Zonenium server on port {PORT}")
    print(f"🌍 Environment: {ENVIRONMENT}")
    print(f"🔗 CORS Origins: {CORS_ORIGINS}")
    
    # Connect to database if backend is available
    if BACKEND_AVAILABLE:
        try:
            await db.connect_to_database()
            print("✅ Database connected successfully")
            
            # Create sample data if in development
            if ENVIRONMENT == "development":
                await db.initialize_sample_data()
                
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
    
    yield
    
    # Shutdown
    print("📴 Shutting down Zonenium server")
    if BACKEND_AVAILABLE:
        try:
            await db.close_database_connection()
        except:
            pass

app = FastAPI(
    title="Zonenium - Free WhatsApp Alternative", 
    description="Modern WhatsApp-like messaging application with voice messages, file sharing, and real-time chat",
    version="1.0.0",
    docs_url="/docs" if DEBUG else None,
    redoc_url="/redoc" if DEBUG else None,
    lifespan=lifespan
)

# Socket.IO integration (if backend available)
if BACKEND_AVAILABLE:
    socket_app = socketio.ASGIApp(socket_manager.sio, app)

# Serve static files (Frontend build) 
static_dir = os.path.join(os.path.dirname(__file__), "frontend", "dist")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    app.mount("/assets", StaticFiles(directory=os.path.join(static_dir, "assets")), name="assets")

# Serve public images and PWA files
public_dir = os.path.join(os.path.dirname(__file__), "frontend", "public")
if os.path.exists(public_dir):
    app.mount("/images", StaticFiles(directory=os.path.join(public_dir, "images")), name="images")

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

            // Listen for install prompt
            window.addEventListener('beforeinstallprompt', (e) => {
                console.log('PWA install prompt available');
                e.preventDefault();
                deferredPrompt = e;
                installButton.style.display = 'inline-block';
            });

            // Install function
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
                    // Fallback instructions
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

            // Check if already installed
            if (window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone) {
                installButton.innerHTML = '✅ App Installed';
                installButton.disabled = true;
                installButton.style.opacity = '0.7';
            }

            // Service worker registration
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
    """Serve the React application"""
    # Check if static frontend exists
    frontend_path = os.path.join(os.path.dirname(__file__), "frontend", "dist", "index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    else:
        # Fallback: serve a simple chat interface if React build doesn't exist
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
                .message { background: #374151; padding: 16px; margin: 8px 0; border-radius: 12px; }
                .input-area { position: fixed; bottom: 0; left: 0; right: 0; background: #1f2937; padding: 20px; border-top: 1px solid #374151; }
                .message-input { width: 100%; padding: 12px; border: 1px solid #374151; border-radius: 25px; background: #374151; color: white; }
                .coming-soon { text-align: center; padding: 40px; opacity: 0.7; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 Zonenium Chat</h1>
                    <p>Full React app is being loaded...</p>
                </div>
                <div class="chat-area">
                    <div class="coming-soon">
                        <h2>Chat Interface Loading</h2>
                        <p>The full messaging experience with authentication, real-time chat, voice messages, and file sharing is being prepared.</p>
                        <div style="margin: 20px 0;">
                            <a href="/" style="background: linear-gradient(45deg, #10b981, #3b82f6); color: white; padding: 12px 24px; border-radius: 25px; text-decoration: none; margin: 8px;">← Back to Home</a>
                        </div>
                    </div>
                </div>
            </div>
            <div class="input-area">
                <input type="text" class="message-input" placeholder="Type your message... (Coming soon)" disabled />
            </div>
        </body>
        </html>
        """)

@app.get("/api/status")
def get_status():
    backend_status = "available" if BACKEND_AVAILABLE else "unavailable"
    return {
        "status": "live",
        "app": "Zonenium",
        "version": "1.0.0",
        "message": "🎉 App is working perfectly!",
        "domain": "zonenium.top", 
        "backend": backend_status,
        "features": ["PWA", "Installable", "Offline Ready", "Real-time Chat", "Voice Messages", "File Sharing"]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "backend_available": BACKEND_AVAILABLE}

if __name__ == "__main__":
    import uvicorn
    if BACKEND_AVAILABLE:
        # Run with Socket.IO support
        uvicorn.run(socket_app, host="0.0.0.0", port=PORT)
    else:
        # Run basic FastAPI app
        uvicorn.run(app, host="0.0.0.0", port=PORT)
