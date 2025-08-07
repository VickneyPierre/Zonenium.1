from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import json

PORT = int(os.environ.get("PORT", 8000))
ENVIRONMENT = os.environ.get("ENVIRONMENT", "production")

# Simple user storage (in production, use proper database)
users_db = {}
messages_db = []

app = FastAPI(
    title="Zoneium Messenger - Premium Messaging Experience", 
    description="Reliable. Private. Beautiful. The most elegant messaging app for modern communication.",
    version="2.0.0"
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
                --gray-100: #F4F6F8;
                --gray-200: #E8EBED;
                --gray-300: #D2D8DD;
                --gray-400: #9DA4AE;
                --gray-500: #6C737F;
                --gray-600: #4D5562;
                --gray-700: #394150;
                --gray-800: #212936;
                --gray-900: #121926;
                --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.02);
                --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
                --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.12);
                --shadow-xl: 0 12px 48px rgba(0, 0, 0, 0.15);
                --border-radius-sm: 8px;
                --border-radius-md: 12px;
                --border-radius-lg: 16px;
                --border-radius-xl: 24px;
            }
            
            * { 
                margin: 0; 
                padding: 0; 
                box-sizing: border-box; 
            }
            
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: var(--gradient-primary);
                color: var(--gray-800);
                min-height: 100vh;
                -webkit-font-smoothing: antialiased;
                -moz-osx-font-smoothing: grayscale;
            }
            
            .auth-container {
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 24px;
                position: relative;
                overflow: hidden;
            }
            
            .auth-container::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="20" cy="20" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="80" cy="40" r="0.8" fill="rgba(255,255,255,0.08)"/><circle cx="40" cy="80" r="1.2" fill="rgba(255,255,255,0.06)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
                opacity: 0.3;
            }
            
            .floating-shapes {
                position: absolute;
                width: 100%;
                height: 100%;
                pointer-events: none;
                overflow: hidden;
            }
            
            .floating-shape {
                position: absolute;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.1);
                animation: float 20s infinite linear;
            }
            
            .floating-shape:nth-child(1) {
                width: 80px;
                height: 80px;
                top: 10%;
                left: 10%;
                animation-delay: 0s;
            }
            
            .floating-shape:nth-child(2) {
                width: 120px;
                height: 120px;
                top: 70%;
                right: 10%;
                animation-delay: -8s;
            }
            
            .floating-shape:nth-child(3) {
                width: 60px;
                height: 60px;
                bottom: 20%;
                left: 20%;
                animation-delay: -15s;
            }
            
            @keyframes float {
                0%, 100% { transform: translateY(0px) rotate(0deg); }
                25% { transform: translateY(-20px) rotate(90deg); }
                50% { transform: translateY(0px) rotate(180deg); }
                75% { transform: translateY(-10px) rotate(270deg); }
            }
            
            .auth-card {
                background: var(--white);
                border-radius: var(--border-radius-xl);
                padding: 48px 40px;
                box-shadow: var(--shadow-xl);
                max-width: 440px;
                width: 100%;
                position: relative;
                z-index: 10;
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            .brand-section {
                text-align: center;
                margin-bottom: 40px;
            }
            
            .logo-container {
                display: inline-block;
                position: relative;
                margin-bottom: 24px;
            }
            
            .logo {
                width: 88px;
                height: 88px;
                background: var(--gradient-primary);
                border-radius: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: var(--shadow-lg);
                position: relative;
                transform: rotate(-5deg);
                transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
            }
            
            .logo:hover {
                transform: rotate(0deg) scale(1.05);
                box-shadow: var(--shadow-xl);
            }
            
            .logo::before {
                content: '';
                position: absolute;
                bottom: -8px;
                right: -8px;
                width: 28px;
                height: 28px;
                background: var(--primary-orange);
                border-radius: 6px 6px 0 6px;
                transform: rotate(45deg);
                box-shadow: var(--shadow-md);
            }
            
            .logo-text {
                color: var(--white);
                font-size: 36px;
                font-weight: 800;
                z-index: 2;
                position: relative;
                text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            }
            
            .brand-name {
                font-size: 32px;
                font-weight: 800;
                color: var(--gray-800);
                margin-bottom: 8px;
                letter-spacing: -0.02em;
            }
            
            .brand-tagline {
                font-size: 16px;
                color: var(--gray-500);
                font-weight: 500;
                letter-spacing: 0.02em;
            }
            
            .auth-form {
                display: flex;
                flex-direction: column;
                gap: 24px;
            }
            
            .form-group {
                position: relative;
            }
            
            .form-label {
                display: block;
                font-size: 14px;
                font-weight: 600;
                color: var(--gray-700);
                margin-bottom: 8px;
                letter-spacing: 0.01em;
            }
            
            .form-input {
                width: 100%;
                padding: 16px 20px;
                border: 2px solid var(--gray-200);
                border-radius: var(--border-radius-md);
                font-size: 16px;
                font-weight: 400;
                transition: all 0.2s ease;
                background: var(--gray-50);
                font-family: inherit;
            }
            
            .form-input:focus {
                outline: none;
                border-color: var(--primary-orange);
                background: var(--white);
                box-shadow: 0 0 0 4px rgba(255, 107, 53, 0.1);
                transform: translateY(-1px);
            }
            
            .form-input::placeholder {
                color: var(--gray-400);
                font-weight: 400;
            }
            
            .btn {
                padding: 16px 24px;
                border-radius: var(--border-radius-md);
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s ease;
                border: none;
                font-family: inherit;
                position: relative;
                overflow: hidden;
            }
            
            .btn-primary {
                background: var(--gradient-primary);
                color: var(--white);
                box-shadow: var(--shadow-md);
            }
            
            .btn-primary:hover {
                transform: translateY(-2px);
                box-shadow: var(--shadow-lg);
            }
            
            .btn-primary:active {
                transform: translateY(0);
            }
            
            .btn-secondary {
                background: var(--gray-100);
                color: var(--gray-700);
                border: 2px solid var(--gray-200);
            }
            
            .btn-secondary:hover {
                background: var(--white);
                border-color: var(--primary-orange);
                color: var(--primary-orange);
                transform: translateY(-1px);
                box-shadow: var(--shadow-sm);
            }
            
            .divider {
                display: flex;
                align-items: center;
                margin: 32px 0;
                color: var(--gray-400);
                font-size: 14px;
                font-weight: 500;
            }
            
            .divider::before,
            .divider::after {
                content: '';
                flex: 1;
                height: 1px;
                background: var(--gray-200);
            }
            
            .divider span {
                margin: 0 20px;
            }
            
            .features-section {
                margin-top: 40px;
                padding-top: 32px;
                border-top: 1px solid var(--gray-200);
            }
            
            .features-title {
                font-size: 18px;
                font-weight: 700;
                color: var(--gray-800);
                margin-bottom: 20px;
                text-align: center;
            }
            
            .features-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 16px;
            }
            
            .feature-item {
                display: flex;
                align-items: center;
                font-size: 14px;
                font-weight: 500;
                color: var(--gray-600);
                padding: 12px;
                background: var(--secondary-orange);
                border-radius: var(--border-radius-sm);
                transition: all 0.2s ease;
            }
            
            .feature-item:hover {
                transform: translateY(-2px);
                box-shadow: var(--shadow-sm);
            }
            
            .feature-icon {
                width: 24px;
                height: 24px;
                background: var(--primary-orange);
                border-radius: 6px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 10px;
                font-size: 12px;
                color: var(--white);
                font-weight: 700;
            }
            
            .loading-spinner {
                display: none;
                width: 24px;
                height: 24px;
                border: 3px solid rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                border-top-color: var(--white);
                animation: spin 1s ease-in-out infinite;
                margin-right: 12px;
            }
            
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
            
            .success-animation {
                opacity: 0;
                transform: scale(0.8);
                animation: successPop 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
            }
            
            @keyframes successPop {
                to {
                    opacity: 1;
                    transform: scale(1);
                }
            }
            
            @media (max-width: 520px) {
                .auth-container {
                    padding: 16px;
                }
                
                .auth-card {
                    padding: 32px 24px;
                }
                
                .brand-name {
                    font-size: 28px;
                }
                
                .features-grid {
                    grid-template-columns: 1fr;
                }
                
                .logo {
                    width: 72px;
                    height: 72px;
                }
                
                .logo-text {
                    font-size: 32px;
                }
            }
            
            /* Custom scrollbar */
            ::-webkit-scrollbar {
                width: 6px;
            }
            
            ::-webkit-scrollbar-track {
                background: var(--gray-100);
            }
            
            ::-webkit-scrollbar-thumb {
                background: var(--primary-orange);
                border-radius: 3px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: var(--primary-orange-hover);
            }
        </style>
    </head>
    <body>
        <div class="auth-container">
            <div class="floating-shapes">
                <div class="floating-shape"></div>
                <div class="floating-shape"></div>
                <div class="floating-shape"></div>
            </div>
            
            <div class="auth-card">
                <div class="brand-section">
                    <div class="logo-container">
                        <div class="logo">
                            <div class="logo-text">Z</div>
                        </div>
                    </div>
                    <h1 class="brand-name">Zoneium</h1>
                    <p class="brand-tagline">Reliable • Private • Beautiful</p>
                </div>
                
                <form class="auth-form" onsubmit="handleAuth(event)">
                    <div class="form-group">
                        <label class="form-label" for="phone">Phone Number</label>
                        <input 
                            type="tel" 
                            id="phone" 
                            name="phone" 
                            class="form-input"
                            placeholder="+1 (555) 123-4567" 
                            required
                        >
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
                        >
                    </div>
                    
                    <button type="submit" class="btn btn-primary" id="signin-btn">
                        <div class="loading-spinner"></div>
                        <span>Sign In to Zoneium</span>
                    </button>
                </form>
                
                <div class="divider">
                    <span>or</span>
                </div>
                
                <button class="btn btn-secondary" onclick="showRegister()">
                    Create New Account
                </button>
                
                <div class="features-section">
                    <h3 class="features-title">Why Choose Zoneium?</h3>
                    <div class="features-grid">
                        <div class="feature-item">
                            <div class="feature-icon">✓</div>
                            <span>No Fees</span>
                        </div>
                        <div class="feature-item">
                            <div class="feature-icon">🎵</div>
                            <span>Voice Messages</span>
                        </div>
                        <div class="feature-item">
                            <div class="feature-icon">📎</div>
                            <span>File Sharing</span>
                        </div>
                        <div class="feature-item">
                            <div class="feature-icon">👥</div>
                            <span>Group Chats</span>
                        </div>
                        <div class="feature-item">
                            <div class="feature-icon">🌍</div>
                            <span>Global Reach</span>
                        </div>
                        <div class="feature-item">
                            <div class="feature-icon">🔒</div>
                            <span>End-to-End Encryption</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            async function handleAuth(event) {
                event.preventDefault();
                
                const btn = document.getElementById('signin-btn');
                const spinner = btn.querySelector('.loading-spinner');
                const span = btn.querySelector('span');
                
                // Show loading state
                btn.disabled = true;
                spinner.style.display = 'block';
                span.textContent = 'Signing In...';
                
                const phone = document.getElementById('phone').value;
                const password = document.getElementById('password').value;
                
                // Simulate authentication delay
                await new Promise(resolve => setTimeout(resolve, 1500));
                
                if (phone && password) {
                    localStorage.setItem('zoneium_user', JSON.stringify({
                        phone: phone,
                        loginTime: new Date().toISOString(),
                        premium: true
                    }));
                    
                    // Success state
                    span.textContent = 'Welcome to Zoneium!';
                    btn.classList.add('success-animation');
                    
                    setTimeout(() => {
                        window.location.href = '/messenger';
                    }, 800);
                } else {
                    // Error state
                    btn.disabled = false;
                    spinner.style.display = 'none';
                    span.textContent = 'Sign In to Zoneium';
                    
                    // Shake animation
                    btn.style.animation = 'shake 0.5s ease-in-out';
                    setTimeout(() => {
                        btn.style.animation = '';
                    }, 500);
                }
            }
            
            function showRegister() {
                window.location.href = '/register';
            }
            
            // Add shake animation
            const style = document.createElement('style');
            style.textContent = `
                @keyframes shake {
                    0%, 100% { transform: translateX(0); }
                    10%, 30%, 50%, 70%, 90% { transform: translateX(-8px); }
                    20%, 40%, 60%, 80% { transform: translateX(8px); }
                }
            `;
            document.head.appendChild(style);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/messenger")
def messenger():
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Zoneium Messenger - Premium Experience</title>
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
                --white: #FFFFFF;
                --gray-50: #FAFBFC;
                --gray-100: #F4F6F8;
                --gray-200: #E8EBED;
                --gray-300: #D2D8DD;
                --gray-400: #9DA4AE;
                --gray-500: #6C737F;
                --gray-600: #4D5562;
                --gray-700: #394150;
                --gray-800: #212936;
                --gray-900: #121926;
                --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.02);
                --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
                --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.12);
                --shadow-xl: 0 12px 48px rgba(0, 0, 0, 0.15);
                --border-radius-sm: 8px;
                --border-radius-md: 12px;
                --border-radius-lg: 16px;
                --border-radius-xl: 24px;
            }
            
            * { 
                margin: 0; 
                padding: 0; 
                box-sizing: border-box; 
            }
            
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: var(--gray-50);
                color: var(--gray-800);
                height: 100vh;
                overflow: hidden;
                -webkit-font-smoothing: antialiased;
                -moz-osx-font-smoothing: grayscale;
            }
            
            .messenger-layout {
                display: flex;
                height: 100vh;
                max-width: 1600px;
                margin: 0 auto;
                background: var(--white);
                box-shadow: var(--shadow-xl);
            }
            
            /* Sidebar Styles */
            .sidebar {
                width: 380px;
                background: var(--white);
                border-right: 1px solid var(--gray-200);
                display: flex;
                flex-direction: column;
                position: relative;
            }
            
            .sidebar-header {
                padding: 24px 28px;
                background: var(--gradient-primary);
                color: var(--white);
                display: flex;
                align-items: center;
                justify-content: space-between;
                box-shadow: var(--shadow-md);
            }
            
            .sidebar-header h1 {
                font-size: 22px;
                font-weight: 700;
                letter-spacing: -0.02em;
            }
            
            .header-actions {
                display: flex;
                gap: 12px;
            }
            
            .header-btn {
                width: 40px;
                height: 40px;
                border: none;
                background: rgba(255, 255, 255, 0.15);
                color: var(--white);
                border-radius: 50%;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 18px;
                transition: all 0.2s ease;
                backdrop-filter: blur(10px);
            }
            
            .header-btn:hover {
                background: rgba(255, 255, 255, 0.25);
                transform: scale(1.05);
            }
            
            .search-section {
                padding: 20px 28px;
                background: var(--gray-50);
                border-bottom: 1px solid var(--gray-200);
            }
            
            .search-container {
                position: relative;
            }
            
            .search-input {
                width: 100%;
                padding: 14px 20px 14px 48px;
                border: 2px solid transparent;
                border-radius: 25px;
                font-size: 15px;
                background: var(--white);
                transition: all 0.2s ease;
                font-family: inherit;
                box-shadow: var(--shadow-sm);
            }
            
            .search-input:focus {
                outline: none;
                border-color: var(--primary-orange);
                box-shadow: 0 0 0 4px rgba(255, 107, 53, 0.1);
            }
            
            .search-icon {
                position: absolute;
                left: 16px;
                top: 50%;
                transform: translateY(-50%);
                color: var(--gray-400);
                font-size: 18px;
                pointer-events: none;
            }
            
            .contacts-list {
                flex: 1;
                overflow-y: auto;
                padding: 8px 0;
            }
            
            .contact-item {
                padding: 16px 28px;
                cursor: pointer;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                border-left: 4px solid transparent;
                position: relative;
            }
            
            .contact-item:hover {
                background: var(--gray-50);
                border-left-color: var(--primary-orange-light);
            }
            
            .contact-item.active {
                background: var(--secondary-orange);
                border-left-color: var(--primary-orange);
            }
            
            .contact-avatar {
                width: 56px;
                height: 56px;
                border-radius: 50%;
                background: var(--gradient-primary);
                display: flex;
                align-items: center;
                justify-content: center;
                color: var(--white);
                font-weight: 700;
                font-size: 20px;
                margin-right: 16px;
                box-shadow: var(--shadow-md);
                position: relative;
            }
            
            .avatar-status {
                position: absolute;
                bottom: 2px;
                right: 2px;
                width: 14px;
                height: 14px;
                background: #22C55E;
                border: 3px solid var(--white);
                border-radius: 50%;
            }
            
            .contact-info {
                flex: 1;
                min-width: 0;
            }
            
            .contact-name {
                font-weight: 600;
                font-size: 16px;
                color: var(--gray-800);
                margin-bottom: 4px;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            
            .contact-time {
                font-size: 12px;
                color: var(--gray-400);
                font-weight: 500;
            }
            
            .contact-preview {
                color: var(--gray-500);
                font-size: 14px;
                font-weight: 400;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                display: flex;
                align-items: center;
                gap: 6px;
            }
            
            .unread-badge {
                background: var(--primary-orange);
                color: var(--white);
                font-size: 11px;
                font-weight: 600;
                padding: 4px 8px;
                border-radius: 10px;
                min-width: 20px;
                text-align: center;
                margin-left: auto;
            }
            
            /* Main Chat Area */
            .chat-main {
                flex: 1;
                display: flex;
                flex-direction: column;
                background: var(--white);
            }
            
            .chat-header {
                padding: 20px 32px;
                background: var(--white);
                border-bottom: 1px solid var(--gray-200);
                display: flex;
                align-items: center;
                justify-content: space-between;
                box-shadow: var(--shadow-sm);
            }
            
            .chat-user-info {
                display: flex;
                align-items: center;
            }
            
            .chat-avatar {
                width: 48px;
                height: 48px;
                border-radius: 50%;
                background: var(--gradient-primary);
                display: flex;
                align-items: center;
                justify-content: center;
                color: var(--white);
                font-weight: 700;
                font-size: 18px;
                margin-right: 16px;
                box-shadow: var(--shadow-md);
            }
            
            .chat-user-details h3 {
                font-size: 18px;
                font-weight: 600;
                color: var(--gray-800);
                margin-bottom: 4px;
            }
            
            .chat-user-status {
                font-size: 14px;
                color: var(--primary-orange);
                font-weight: 500;
                display: flex;
                align-items: center;
            }
            
            .status-indicator {
                width: 8px;
                height: 8px;
                background: #22C55E;
                border-radius: 50%;
                margin-right: 8px;
                animation: pulse 2s infinite;
            }
            
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.5; }
                100% { opacity: 1; }
            }
            
            .chat-actions {
                display: flex;
                gap: 8px;
            }
            
            .chat-action-btn {
                width: 44px;
                height: 44px;
                border: none;
                background: var(--gray-100);
                color: var(--gray-600);
                border-radius: 50%;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 18px;
                transition: all 0.2s ease;
            }
            
            .chat-action-btn:hover {
                background: var(--primary-orange);
                color: var(--white);
                transform: scale(1.05);
            }
            
            .messages-container {
                flex: 1;
                overflow-y: auto;
                padding: 32px;
                background: linear-gradient(to bottom, var(--gray-50), var(--white));
                display: flex;
                flex-direction: column;
                gap: 16px;
            }
            
            .welcome-screen {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100%;
                text-align: center;
                color: var(--gray-500);
                padding: 40px;
            }
            
            .welcome-logo {
                width: 120px;
                height: 120px;
                background: var(--gradient-primary);
                border-radius: 30px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: var(--white);
                font-size: 48px;
                font-weight: 800;
                margin-bottom: 32px;
                box-shadow: var(--shadow-lg);
                animation: float 6s ease-in-out infinite;
            }
            
            @keyframes float {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-10px); }
            }
            
            .welcome-title {
                font-size: 28px;
                font-weight: 700;
                color: var(--gray-800);
                margin-bottom: 16px;
            }
            
            .welcome-subtitle {
                font-size: 16px;
                margin-bottom: 40px;
                max-width: 400px;
                line-height: 1.5;
            }
            
            .welcome-features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 24px;
                max-width: 600px;
                width: 100%;
            }
            
            .welcome-feature {
                padding: 24px;
                background: var(--white);
                border-radius: var(--border-radius-lg);
                box-shadow: var(--shadow-md);
                transition: all 0.2s ease;
            }
            
            .welcome-feature:hover {
                transform: translateY(-4px);
                box-shadow: var(--shadow-lg);
            }
            
            .feature-icon-large {
                font-size: 32px;
                margin-bottom: 16px;
            }
            
            .feature-title {
                font-size: 16px;
                font-weight: 600;
                color: var(--gray-800);
                margin-bottom: 8px;
            }
            
            .feature-description {
                font-size: 14px;
                color: var(--gray-500);
                line-height: 1.4;
            }
            
            .message {
                max-width: 75%;
                padding: 16px 20px;
                border-radius: 20px;
                font-size: 15px;
                line-height: 1.4;
                word-wrap: break-word;
                position: relative;
                margin-bottom: 4px;
                animation: messageSlide 0.3s ease-out;
            }
            
            @keyframes messageSlide {
                from {
                    opacity: 0;
                    transform: translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .message.sent {
                background: var(--gradient-primary);
                color: var(--white);
                align-self: flex-end;
                border-bottom-right-radius: 6px;
                box-shadow: var(--shadow-md);
            }
            
            .message.received {
                background: var(--white);
                color: var(--gray-800);
                align-self: flex-start;
                border-bottom-left-radius: 6px;
                border: 1px solid var(--gray-200);
                box-shadow: var(--shadow-sm);
            }
            
            .message-time {
                font-size: 11px;
                opacity: 0.7;
                margin-top: 6px;
                text-align: right;
            }
            
            .message.received .message-time {
                text-align: left;
                color: var(--gray-400);
            }
            
            .message-input-area {
                padding: 24px 32px;
                background: var(--white);
                border-top: 1px solid var(--gray-200);
                display: flex;
                align-items: center;
                gap: 16px;
                box-shadow: var(--shadow-sm);
            }
            
            .attachment-btn, .voice-btn {
                width: 48px;
                height: 48px;
                border: none;
                background: var(--gray-100);
                color: var(--gray-600);
                border-radius: 50%;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 20px;
                transition: all 0.2s ease;
            }
            
            .attachment-btn:hover, .voice-btn:hover {
                background: var(--secondary-orange);
                color: var(--primary-orange);
                transform: scale(1.05);
            }
            
            .message-input {
                flex: 1;
                padding: 16px 24px;
                border: 2px solid var(--gray-200);
                border-radius: 25px;
                font-size: 15px;
                background: var(--gray-50);
                transition: all 0.2s ease;
                font-family: inherit;
                resize: none;
                max-height: 120px;
                min-height: 48px;
            }
            
            .message-input:focus {
                outline: none;
                border-color: var(--primary-orange);
                background: var(--white);
                box-shadow: 0 0 0 4px rgba(255, 107, 53, 0.1);
            }
            
            .send-btn {
                width: 48px;
                height: 48px;
                background: var(--gradient-primary);
                border: none;
                border-radius: 50%;
                color: var(--white);
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 20px;
                transition: all 0.2s ease;
                box-shadow: var(--shadow-md);
            }
            
            .send-btn:hover {
                transform: scale(1.05);
                box-shadow: var(--shadow-lg);
            }
            
            .send-btn:active {
                transform: scale(0.95);
            }
            
            /* Responsive Design */
            @media (max-width: 1024px) {
                .sidebar {
                    width: 320px;
                }
            }
            
            @media (max-width: 768px) {
                .messenger-layout {
                    flex-direction: column;
                }
                
                .sidebar {
                    width: 100%;
                    height: 100vh;
                    position: fixed;
                    z-index: 1000;
                    transform: translateX(-100%);
                    transition: transform 0.3s ease;
                }
                
                .sidebar.active {
                    transform: translateX(0);
                }
                
                .chat-main {
                    width: 100%;
                    height: 100vh;
                }
                
                .mobile-nav {
                    display: flex;
                    position: fixed;
                    bottom: 0;
                    left: 0;
                    right: 0;
                    background: var(--white);
                    padding: 16px;
                    border-top: 1px solid var(--gray-200);
                    z-index: 100;
                }
            }
            
            /* Custom Scrollbar */
            ::-webkit-scrollbar {
                width: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: var(--gray-100);
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: var(--primary-orange);
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: var(--primary-orange-hover);
            }
        </style>
    </head>
    <body>
        <div class="messenger-layout">
            <!-- Sidebar -->
            <div class="sidebar">
                <div class="sidebar-header">
                    <h1>Zoneium</h1>
                    <div class="header-actions">
                        <button class="header-btn" title="New Chat">💬</button>
                        <button class="header-btn" title="Settings">⚙️</button>
                    </div>
                </div>
                
                <div class="search-section">
                    <div class="search-container">
                        <div class="search-icon">🔍</div>
                        <input 
                            type="text" 
                            class="search-input" 
                            placeholder="Search conversations..."
                            id="search-input"
                        >
                    </div>
                </div>
                
                <div class="contacts-list">
                    <div class="contact-item active" onclick="openChat('John Doe', 'J', 'Hey! Ready for the meeting?')">
                        <div class="contact-avatar">
                            J
                            <div class="avatar-status"></div>
                        </div>
                        <div class="contact-info">
                            <div class="contact-name">
                                <span>John Doe</span>
                                <span class="contact-time">2m</span>
                            </div>
                            <div class="contact-preview">
                                <span>✓✓</span>
                                <span>Hey! Ready for the meeting?</span>
                                <div class="unread-badge">3</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="contact-item" onclick="openChat('Maria Garcia', 'M', '📎 Design_Final.pdf')">
                        <div class="contact-avatar">M</div>
                        <div class="contact-info">
                            <div class="contact-name">
                                <span>Maria Garcia</span>
                                <span class="contact-time">15m</span>
                            </div>
                            <div class="contact-preview">
                                <span>📎</span>
                                <span>Design_Final.pdf</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="contact-item" onclick="openChat('Family Group', 'F', 'Mom: Don\\'t forget dinner tonight!')">
                        <div class="contact-avatar">F</div>
                        <div class="contact-info">
                            <div class="contact-name">
                                <span>Family Group</span>
                                <span class="contact-time">1h</span>
                            </div>
                            <div class="contact-preview">
                                <span>👥</span>
                                <span>Mom: Don't forget dinner tonight!</span>
                                <div class="unread-badge">1</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="contact-item" onclick="openChat('Tech Team', 'T', '🎤 Voice message')">
                        <div class="contact-avatar">T</div>
                        <div class="contact-info">
                            <div class="contact-name">
                                <span>Tech Team</span>
                                <span class="contact-time">3h</span>
                            </div>
                            <div class="contact-preview">
                                <span>🎤</span>
                                <span>Voice message (0:42)</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="contact-item" onclick="openChat('Sarah Johnson', 'S', 'Perfect! Thanks for the update')">
                        <div class="contact-avatar">S</div>
                        <div class="contact-info">
                            <div class="contact-name">
                                <span>Sarah Johnson</span>
                                <span class="contact-time">Yesterday</span>
                            </div>
                            <div class="contact-preview">
                                <span>Perfect! Thanks for the update</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="contact-item" onclick="openChat('Alex Wilson', 'A', '📷 Photo')">
                        <div class="contact-avatar">A</div>
                        <div class="contact-info">
                            <div class="contact-name">
                                <span>Alex Wilson</span>
                                <span class="contact-time">2 days ago</span>
                            </div>
                            <div class="contact-preview">
                                <span>📷</span>
                                <span>Photo</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Main Chat Area -->
            <div class="chat-main">
                <div class="chat-header" id="chat-header" style="display: none;">
                    <div class="chat-user-info">
                        <div class="chat-avatar" id="chat-avatar">J</div>
                        <div class="chat-user-details">
                            <h3 id="chat-title">John Doe</h3>
                            <div class="chat-user-status">
                                <div class="status-indicator"></div>
                                <span>Online • Last seen now</span>
                            </div>
                        </div>
                    </div>
                    <div class="chat-actions">
                        <button class="chat-action-btn" title="Search">🔍</button>
                        <button class="chat-action-btn" title="Voice Call">📞</button>
                        <button class="chat-action-btn" title="Video Call">📹</button>
                        <button class="chat-action-btn" title="More">⋮</button>
                    </div>
                </div>
                
                <div class="messages-container" id="messages-container">
                    <div class="welcome-screen">
                        <div class="welcome-logo">Z</div>
                        <h2 class="welcome-title">Welcome to Zoneium</h2>
                        <p class="welcome-subtitle">
                            Experience premium messaging with beautiful design, 
                            powerful features, and complete privacy.
                        </p>
                        <div class="welcome-features">
                            <div class="welcome-feature">
                                <div class="feature-icon-large">🔒</div>
                                <div class="feature-title">End-to-End Encrypted</div>
                                <div class="feature-description">Your conversations are completely private and secure</div>
                            </div>
                            <div class="welcome-feature">
                                <div class="feature-icon-large">⚡</div>
                                <div class="feature-title">Lightning Fast</div>
                                <div class="feature-description">Messages delivered instantly across all devices</div>
                            </div>
                            <div class="welcome-feature">
                                <div class="feature-icon-large">🎨</div>
                                <div class="feature-title">Beautiful Design</div>
                                <div class="feature-description">Carefully crafted interface for the best experience</div>
                            </div>
                            <div class="welcome-feature">
                                <div class="feature-icon-large">🌍</div>
                                <div class="feature-title">Global Network</div>
                                <div class="feature-description">Connect with anyone, anywhere in the world</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="message-input-area" id="input-area" style="display: none;">
                    <button class="attachment-btn" title="Attach files">📎</button>
                    <textarea 
                        class="message-input" 
                        id="message-input" 
                        placeholder="Type your message here..."
                        rows="1"
                    ></textarea>
                    <button class="voice-btn" title="Voice message">🎤</button>
                    <button class="send-btn" onclick="sendMessage()" title="Send message">➤</button>
                </div>
            </div>
        </div>

        <script>
            let currentChat = null;
            let messages = {
                'John Doe': [
                    { type: 'received', text: 'Hey! How are you doing today?', time: '10:30 AM' },
                    { type: 'sent', text: 'Great! Thanks for asking. Working on some exciting projects.', time: '10:32 AM' },
                    { type: 'received', text: 'That sounds amazing! Ready for the meeting?', time: '10:33 AM' },
                    { type: 'sent', text: 'Absolutely! Looking forward to it 🚀', time: '10:35 AM' }
                ],
                'Maria Garcia': [
                    { type: 'received', text: 'Here's the final design document', time: '9:45 AM' },
                    { type: 'received', text: '📎 Design_Final.pdf (2.5 MB)', time: '9:45 AM' },
                    { type: 'sent', text: 'Perfect! I'll review it right away', time: '9:50 AM' },
                    { type: 'received', text: 'Let me know if you need any changes', time: '9:51 AM' }
                ],
                'Family Group': [
                    { type: 'received', text: 'Mom: Don't forget dinner tonight at 7 PM', time: '8:20 AM' },
                    { type: 'received', text: 'Dad: I'll bring the dessert! 🍰', time: '8:22 AM' },
                    { type: 'sent', text: 'Looking forward to it! See you all there', time: '8:25 AM' },
                    { type: 'received', text: 'Sister: Can I bring a friend?', time: '8:30 AM' }
                ],
                'Tech Team': [
                    { type: 'received', text: '🎤 Voice message (0:42)', time: '7:15 AM' },
                    { type: 'sent', text: 'Got it! I'll review the code changes', time: '7:20 AM' },
                    { type: 'received', text: 'Thanks! The deadline is tomorrow', time: '7:22 AM' },
                    { type: 'sent', text: 'No problem, I'll have it ready', time: '7:25 AM' }
                ]
            };
            
            function openChat(name, avatar, preview) {
                // Update active state
                document.querySelectorAll('.contact-item').forEach(item => {
                    item.classList.remove('active');
                });
                event.currentTarget.classList.add('active');
                
                currentChat = name;
                document.getElementById('chat-title').textContent = name;
                document.getElementById('chat-avatar').textContent = avatar;
                document.getElementById('chat-header').style.display = 'flex';
                document.getElementById('input-area').style.display = 'flex';
                
                // Load messages
                const container = document.getElementById('messages-container');
                container.innerHTML = '';
                
                if (messages[name]) {
                    messages[name].forEach(msg => {
                        const messageDiv = document.createElement('div');
                        messageDiv.className = `message ${msg.type}`;
                        messageDiv.innerHTML = `
                            <div>${msg.text}</div>
                            <div class="message-time">${msg.time}</div>
                        `;
                        container.appendChild(messageDiv);
                    });
                }
                
                container.scrollTop = container.scrollHeight;
            }
            
            function sendMessage() {
                const input = document.getElementById('message-input');
                const text = input.value.trim();
                
                if (text && currentChat) {
                    if (!messages[currentChat]) {
                        messages[currentChat] = [];
                    }
                    
                    const now = new Date();
                    const time = now.toLocaleTimeString('en-US', {
                        hour: 'numeric',
                        minute: '2-digit',
                        hour12: true
                    });
                    
                    messages[currentChat].push({ type: 'sent', text: text, time: time });
                    
                    const container = document.getElementById('messages-container');
                    const messageDiv = document.createElement('div');
                    messageDiv.className = 'message sent';
                    messageDiv.innerHTML = `
                        <div>${text}</div>
                        <div class="message-time">${time}</div>
                    `;
                    container.appendChild(messageDiv);
                    
                    input.value = '';
                    container.scrollTop = container.scrollHeight;
                    
                    // Auto-resize textarea
                    input.style.height = 'auto';
                }
            }
            
            // Auto-resize textarea
            document.getElementById('message-input').addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = Math.min(this.scrollHeight, 120) + 'px';
            });
            
            // Enter to send message
            document.getElementById('message-input').addEventListener('keypress', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                }
            });
            
            // Search functionality
            document.getElementById('search-input').addEventListener('input', function(e) {
                const query = e.target.value.toLowerCase();
                const contacts = document.querySelectorAll('.contact-item');
                
                contacts.forEach(contact => {
                    const name = contact.querySelector('.contact-name span').textContent.toLowerCase();
                    if (name.includes(query)) {
                        contact.style.display = 'flex';
                    } else {
                        contact.style.display = 'none';
                    }
                });
            });
        </script>
    </body>
    </html>
    """)

@app.get("/register")
def register():
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Create Account - Zoneium</title>
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
                --white: #FFFFFF;
                --gray-50: #FAFBFC;
                --gray-100: #F4F6F8;
                --gray-200: #E8EBED;
                --gray-300: #D2D8DD;
                --gray-400: #9DA4AE;
                --gray-500: #6C737F;
                --gray-600: #4D5562;
                --gray-700: #394150;
                --gray-800: #212936;
                --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.02);
                --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
                --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.12);
                --shadow-xl: 0 12px 48px rgba(0, 0, 0, 0.15);
                --border-radius-sm: 8px;
                --border-radius-md: 12px;
                --border-radius-lg: 16px;
                --border-radius-xl: 24px;
            }
            
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: var(--gradient-primary);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 24px;
                -webkit-font-smoothing: antialiased;
                -moz-osx-font-smoothing: grayscale;
            }
            
            .register-container {
                background: var(--white);
                border-radius: var(--border-radius-xl);
                padding: 40px;
                box-shadow: var(--shadow-xl);
                max-width: 480px;
                width: 100%;
                position: relative;
            }
            
            .back-btn {
                position: absolute;
                top: 24px;
                left: 24px;
                width: 40px;
                height: 40px;
                border: none;
                background: var(--gray-100);
                border-radius: 50%;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 18px;
                color: var(--gray-600);
                transition: all 0.2s ease;
            }
            
            .back-btn:hover {
                background: var(--secondary-orange);
                color: var(--primary-orange);
                transform: scale(1.05);
            }
            
            .brand-section {
                text-align: center;
                margin-bottom: 32px;
                margin-top: 16px;
            }
            
            .logo {
                width: 72px;
                height: 72px;
                background: var(--gradient-primary);
                border-radius: 18px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 20px;
                position: relative;
                box-shadow: var(--shadow-lg);
            }
            
            .logo::before {
                content: '';
                position: absolute;
                bottom: -6px;
                right: -6px;
                width: 20px;
                height: 20px;
                background: var(--primary-orange);
                border-radius: 4px 4px 0 4px;
                transform: rotate(45deg);
            }
            
            .logo-text {
                color: var(--white);
                font-size: 28px;
                font-weight: 800;
                z-index: 2;
                position: relative;
            }
            
            h1 {
                font-size: 28px;
                color: var(--gray-800);
                margin-bottom: 8px;
                font-weight: 700;
                letter-spacing: -0.02em;
            }
            
            .subtitle {
                color: var(--gray-500);
                font-size: 16px;
                font-weight: 400;
            }
            
            .register-form {
                display: flex;
                flex-direction: column;
                gap: 20px;
            }
            
            .form-row {
                display: flex;
                gap: 16px;
            }
            
            .form-group {
                flex: 1;
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
                padding: 14px 16px;
                border: 2px solid var(--gray-200);
                border-radius: var(--border-radius-md);
                font-size: 16px;
                background: var(--gray-50);
                transition: all 0.2s ease;
                font-family: inherit;
            }
            
            .form-input:focus {
                outline: none;
                border-color: var(--primary-orange);
                background: var(--white);
                box-shadow: 0 0 0 4px rgba(255, 107, 53, 0.1);
                transform: translateY(-1px);
            }
            
            .form-input::placeholder {
                color: var(--gray-400);
            }
            
            .btn-primary {
                width: 100%;
                background: var(--gradient-primary);
                color: var(--white);
                border: none;
                padding: 16px 24px;
                border-radius: var(--border-radius-md);
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s ease;
                box-shadow: var(--shadow-md);
                font-family: inherit;
            }
            
            .btn-primary:hover {
                transform: translateY(-2px);
                box-shadow: var(--shadow-lg);
            }
            
            .btn-primary:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }
            
            .login-link {
                text-align: center;
                margin-top: 24px;
                color: var(--gray-600);
                font-size: 14px;
            }
            
            .login-link a {
                color: var(--primary-orange);
                text-decoration: none;
                font-weight: 600;
            }
            
            .login-link a:hover {
                text-decoration: underline;
            }
            
            .password-strength {
                margin-top: 8px;
            }
            
            .strength-bar {
                width: 100%;
                height: 4px;
                background: var(--gray-200);
                border-radius: 2px;
                overflow: hidden;
                margin-bottom: 8px;
            }
            
            .strength-fill {
                height: 100%;
                transition: all 0.3s ease;
                border-radius: 2px;
            }
            
            .strength-text {
                font-size: 12px;
                font-weight: 500;
            }
            
            .strength-weak { background: #EF4444; color: #EF4444; }
            .strength-medium { background: #F59E0B; color: #F59E0B; }
            .strength-strong { background: #10B981; color: #10B981; }
            
            @media (max-width: 520px) {
                .register-container {
                    padding: 32px 24px;
                }
                
                .form-row {
                    flex-direction: column;
                    gap: 20px;
                }
                
                h1 {
                    font-size: 24px;
                }
            }
        </style>
    </head>
    <body>
        <div class="register-container">
            <button class="back-btn" onclick="window.location.href='/'">←</button>
            
            <div class="brand-section">
                <div class="logo">
                    <div class="logo-text">Z</div>
                </div>
                <h1>Create Account</h1>
                <p class="subtitle">Join the premium messaging experience</p>
            </div>
            
            <form class="register-form" onsubmit="handleRegister(event)">
                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label" for="first-name">First Name</label>
                        <input type="text" id="first-name" name="first-name" class="form-input" placeholder="John" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label" for="last-name">Last Name</label>
                        <input type="text" id="last-name" name="last-name" class="form-input" placeholder="Doe" required>
                    </div>
                </div>
                
                <div class="form-group">
                    <label class="form-label" for="email">Email Address</label>
                    <input type="email" id="email" name="email" class="form-input" placeholder="john@example.com" required>
                </div>
                
                <div class="form-group">
                    <label class="form-label" for="phone">Phone Number</label>
                    <input type="tel" id="phone" name="phone" class="form-input" placeholder="+1 (555) 123-4567" required>
                </div>
                
                <div class="form-group">
                    <label class="form-label" for="password">Password</label>
                    <input type="password" id="password" name="password" class="form-input" placeholder="Create a strong password" required>
                    <div class="password-strength">
                        <div class="strength-bar">
                            <div class="strength-fill" id="strength-fill"></div>
                        </div>
                        <div class="strength-text" id="strength-text">Password strength</div>
                    </div>
                </div>
                
                <div class="form-group">
                    <label class="form-label" for="confirm-password">Confirm Password</label>
                    <input type="password" id="confirm-password" name="confirm-password" class="form-input" placeholder="Confirm your password" required>
                </div>
                
                <button type="submit" class="btn-primary" id="register-btn">
                    Create Account
                </button>
            </form>
            
            <div class="login-link">
                Already have an account? <a href="/">Sign In</a>
            </div>
        </div>

        <script>
            function checkPasswordStrength(password) {
                const strengthFill = document.getElementById('strength-fill');
                const strengthText = document.getElementById('strength-text');
                
                let strength = 0;
                if (password.length >= 8) strength++;
                if (password.match(/[a-z]/)) strength++;
                if (password.match(/[A-Z]/)) strength++;
                if (password.match(/[0-9]/)) strength++;
                if (password.match(/[^a-zA-Z0-9]/)) strength++;
                
                strengthFill.style.width = (strength * 20) + '%';
                
                if (strength < 3) {
                    strengthFill.className = 'strength-fill strength-weak';
                    strengthText.textContent = 'Weak password';
                    strengthText.className = 'strength-text strength-weak';
                } else if (strength < 5) {
                    strengthFill.className = 'strength-fill strength-medium';
                    strengthText.textContent = 'Good password';
                    strengthText.className = 'strength-text strength-medium';
                } else {
                    strengthFill.className = 'strength-fill strength-strong';
                    strengthText.textContent = 'Strong password';
                    strengthText.className = 'strength-text strength-strong';
                }
            }
            
            document.getElementById('password').addEventListener('input', function(e) {
                checkPasswordStrength(e.target.value);
            });
            
            async function handleRegister(event) {
                event.preventDefault();
                
                const btn = document.getElementById('register-btn');
                const firstName = document.getElementById('first-name').value;
                const lastName = document.getElementById('last-name').value;
                const email = document.getElementById('email').value;
                const phone = document.getElementById('phone').value;
                const password = document.getElementById('password').value;
                const confirmPassword = document.getElementById('confirm-password').value;
                
                if (password !== confirmPassword) {
                    alert('Passwords do not match');
                    return;
                }
                
                btn.disabled = true;
                btn.textContent = 'Creating Account...';
                
                // Simulate registration delay
                await new Promise(resolve => setTimeout(resolve, 2000));
                
                if (firstName && lastName && email && phone && password) {
                    localStorage.setItem('zoneium_user', JSON.stringify({
                        name: `${firstName} ${lastName}`,
                        email: email,
                        phone: phone,
                        loginTime: new Date().toISOString(),
                        premium: true
                    }));
                    
                    btn.textContent = 'Account Created!';
                    btn.style.background = 'linear-gradient(135deg, #10B981, #059669)';
                    
                    setTimeout(() => {
                        window.location.href = '/messenger';
                    }, 1000);
                } else {
                    btn.disabled = false;
                    btn.textContent = 'Create Account';
                }
            }
        </script>
    </body>
    </html>
    """)

@app.get("/api/status")
def get_status():
    return {
        "status": "live",
        "app": "Zoneium Messenger Premium",
        "version": "2.0.0",
        "message": "Premium messaging experience - Reliable. Private. Beautiful.",
        "features": [
            "End-to-End Encryption", 
            "Premium Design", 
            "Voice Messages", 
            "File Sharing",
            "Group Chats",
            "Global Network",
            "Lightning Fast",
            "Beautiful UI"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
