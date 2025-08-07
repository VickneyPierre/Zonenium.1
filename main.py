

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
import os

PORT = int(os.environ.get("PORT", 8000))
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

app = FastAPI(
    title="Zoneium Messenger - Premium Messaging Experience", 
    description="Reliable. Private. Beautiful. The most elegant messaging app for modern communication.",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Zoneium - Premium Messaging Experience</title>
        <meta name="theme-color" content="#FF6B35">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            :root {
                --primary-orange: #FF6B35;
                --primary-orange-hover: #E55D2B;
                --primary-orange-light: #FF8F66;
                --secondary-orange: #FFF4F0;
                --gradient-primary: linear-gradient(135deg, #FF6B35 0%, #FF8F66 100%);
                --gradient-secondary: linear-gradient(135deg, #FFF4F0 0%, #FFEDE5 100%);
                --white: #FFFFFF;
                --gray-50: #FAFBFC;
                --gray-100: #F3F4F6;
                --gray-200: #E5E7EB;
                --gray-300: #D1D5DB;
                --gray-400: #9CA3AF;
                --gray-500: #6B7280;
                --gray-600: #4B5563;
                --gray-700: #374151;
                --gray-800: #1F2937;
                --gray-900: #111827;
                --shadow-soft: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                --shadow-medium: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
                --shadow-large: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            }

            * { margin: 0; padding: 0; box-sizing: border-box; }

            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background: var(--gradient-primary);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                line-height: 1.6;
                color: var(--gray-800);
                overflow: hidden;
                position: relative;
            }

            .bg-decoration {
                position: absolute;
                width: 200px;
                height: 200px;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.1);
                animation: float 6s ease-in-out infinite;
            }
            .bg-decoration:nth-child(1) {
                top: 10%;
                left: 10%;
                animation-delay: 0s;
            }
            .bg-decoration:nth-child(2) {
                top: 70%;
                right: 10%;
                animation-delay: 2s;
                width: 150px;
                height: 150px;
            }
            .bg-decoration:nth-child(3) {
                bottom: 20%;
                left: 20%;
                animation-delay: 4s;
                width: 100px;
                height: 100px;
            }

            @keyframes float {
                0%, 100% { transform: translateY(0px) rotate(0deg); }
                50% { transform: translateY(-20px) rotate(180deg); }
            }

            .container {
                max-width: 420px;
                width: 90%;
                position: relative;
                z-index: 10;
            }

            .login-card {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 24px;
                padding: 40px 32px;
                box-shadow: var(--shadow-large);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                animation: slideUp 0.8s ease-out;
            }

            @keyframes slideUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .logo-container {
                text-align: center;
                margin-bottom: 32px;
            }

            .logo {
                width: 80px;
                height: 80px;
                margin: 0 auto 16px;
                background: var(--gradient-primary);
                border-radius: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: var(--shadow-medium);
                transition: transform 0.3s ease;
                font-size: 32px;
                font-weight: 900;
                color: white;
            }

            .logo:hover {
                transform: scale(1.05);
            }

            .app-title {
                font-size: 28px;
                font-weight: 800;
                color: var(--gray-800);
                margin-bottom: 8px;
                letter-spacing: -0.02em;
            }

            .app-subtitle {
                color: var(--gray-500);
                font-size: 16px;
                font-weight: 500;
                margin-bottom: 32px;
            }

            .form-group {
                margin-bottom: 24px;
            }

            .form-label {
                display: block;
                font-size: 14px;
                font-weight: 600;
                color: var(--gray-700);
                margin-bottom: 8px;
            }

            .form-input {
                width: 100%;
                padding: 16px 18px;
                border: 2px solid var(--gray-200);
                border-radius: 12px;
                font-size: 16px;
                font-weight: 500;
                color: var(--gray-800);
                background: var(--white);
                transition: all 0.3s ease;
                outline: none;
            }

            .form-input:focus {
                border-color: var(--primary-orange);
                box-shadow: 0 0 0 4px rgba(255, 107, 53, 0.1);
                transform: translateY(-1px);
            }

            .form-input::placeholder {
                color: var(--gray-400);
                font-weight: 400;
            }

            .primary-button {
                width: 100%;
                padding: 18px 24px;
                background: var(--gradient-primary);
                color: var(--white);
                border: none;
                border-radius: 12px;
                font-size: 16px;
                font-weight: 700;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: var(--shadow-medium);
                margin-bottom: 20px;
                text-decoration: none;
                display: inline-block;
                text-align: center;
            }

            .primary-button:hover {
                background: linear-gradient(135deg, var(--primary-orange-hover) 0%, var(--primary-orange) 100%);
                transform: translateY(-2px);
                box-shadow: var(--shadow-large);
            }

            .secondary-button {
                width: 100%;
                padding: 16px 24px;
                background: transparent;
                color: var(--gray-600);
                border: 2px solid var(--gray-200);
                border-radius: 12px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                margin-bottom: 20px;
                text-decoration: none;
                display: inline-block;
                text-align: center;
            }

            .secondary-button:hover {
                border-color: var(--primary-orange);
                color: var(--primary-orange);
                background: rgba(255, 107, 53, 0.05);
                transform: translateY(-1px);
            }

            .launch-button {
                background: linear-gradient(135deg, #10B981 0%, #059669 100%);
                margin-bottom: 16px;
            }
            
            .launch-button:hover {
                background: linear-gradient(135deg, #059669 0%, #047857 100%);
            }

            .divider {
                text-align: center;
                margin: 24px 0;
                position: relative;
                color: var(--gray-400);
                font-size: 14px;
                font-weight: 500;
            }

            .divider::before {
                content: '';
                position: absolute;
                top: 50%;
                left: 0;
                right: 0;
                height: 1px;
                background: var(--gray-200);
                z-index: 1;
            }

            .divider span {
                background: var(--white);
                padding: 0 16px;
                position: relative;
                z-index: 2;
            }

            .features {
                margin-top: 32px;
                text-align: center;
            }

            .features-title {
                font-size: 18px;
                font-weight: 700;
                color: var(--gray-800);
                margin-bottom: 16px;
            }

            .features-list {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 12px;
                font-size: 14px;
                color: var(--gray-600);
            }

            .feature-item {
                display: flex;
                align-items: center;
                gap: 8px;
                padding: 8px 12px;
                background: var(--secondary-orange);
                border-radius: 8px;
                font-weight: 500;
            }

            .feature-icon {
                width: 16px;
                height: 16px;
                background: var(--primary-orange);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 10px;
                font-weight: bold;
            }

            @media (max-width: 480px) {
                .container { width: 95%; }
                .login-card { padding: 32px 24px; }
                .app-title { font-size: 24px; }
                .form-input, .primary-button { font-size: 16px; }
                .features-list { grid-template-columns: 1fr; }
            }
        </style>
    </head>
    <body>
        <div class="bg-decoration"></div>
        <div class="bg-decoration"></div>
        <div class="bg-decoration"></div>
        
        <div class="container">
            <div class="login-card">
                <div class="logo-container">
                    <div class="logo">Z</div>
                    <h1 class="app-title">Zonenium</h1>
                    <p class="app-subtitle">Reliable • Private • Beautiful</p>
                </div>

                <form id="loginForm">
                    <div class="form-group">
                        <label class="form-label" for="phone">Phone Number</label>
                        <input 
                            type="tel" 
                            id="phone" 
                            name="phone" 
                            class="form-input" 
                            placeholder="+1 (555) 123-4567"
                            required
                        />
                    </div>

                    <div class="form-group">
                        <label class="form-label" for="password">Password</label>
                        <input 
                            type="password" 
                            id="password" 
                            name="password" 
                            class="form-input" 
                            placeholder="Enter your password"
                            required
                        />
                    </div>

                    <a href="/app" class="primary-button launch-button">
                        🚀 Launch App
                    </a>

                    <button type="submit" class="primary-button">
                        Sign In to Zonenium
                    </button>
                </form>

                <div class="divider">
                    <span>or</span>
                </div>

                <a href="/register" class="secondary-button">
                    Create New Account
                </a>

                <div class="features">
                    <h3 class="features-title">Why Choose Zonenium?</h3>
                    <div class="features-list">
                        <div class="feature-item">
                            <div class="feature-icon">🔒</div>
                            <span>End-to-End Encrypted</span>
                        </div>
                        <div class="feature-item">
                            <div class="feature-icon">⚡</div>
                            <span>Lightning Fast</span>
                        </div>
                        <div class="feature-item">
                            <div class="feature-icon">🎵</div>
                            <span>Voice Messages</span>
                        </div>
                        <div class="feature-item">
                            <div class="feature-icon">👥</div>
                            <span>Group Chats</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            document.getElementById('loginForm').addEventListener('submit', function(e) {
                e.preventDefault();
                window.location.href = '/app';
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/app")
def messenger_app():
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html><head><title>Zonenium - Messaging App</title></head>
    <body style="font-family: Arial; text-align: center; padding: 50px; background: #1F2937; color: white;">
        <div style="max-width: 400px; margin: 0 auto;">
            <div style="width: 60px; height: 60px; margin: 0 auto 20px; background: linear-gradient(135deg, #FF6B35, #FF8F66); border-radius: 15px; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; color: white;">Z</div>
            <h1>Welcome to Zonenium</h1>
            <p>Premium messaging experience coming soon!</p>
            <div style="margin: 30px 0;">
                <h3>Demo Accounts:</h3>
                <p>Username: demo_user, Password: demo123</p>
                <p>Username: test_user, Password: test123</p>
            </div>
            <p><a href="/" style="color: #FF6B35;">← Back to Home</a></p>
        </div>
    </body></html>
    """)

@app.get("/api/status")
def get_status():
    return {
        "status": "live",
        "app": "Zoneium Messenger Premium",
        "version": "3.0.0",
        "message": "Premium messaging experience with your branding - Reliable. Private. Beautiful.",
        "features": [
            "Beautiful landing page with your Zonenium branding",
            "Launch App button for seamless navigation", 
            "Premium UI with glass-morphism effects",
            "Mobile responsive design",
            "Ready for full messaging features"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
