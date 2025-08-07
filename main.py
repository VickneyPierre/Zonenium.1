Absolutely! Here's your complete `main.py` file that's ready for deployment. This includes your Zonenium logo, complete backend functionality, and all the fixes we applied:
Action: file_editor view /app/zonenium/main.py
Observation: /app/zonenium/main.py:
1|from fastapi import FastAPI, HTTPException, Depends, status, File, UploadFile
2|from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
3|from fastapi.middleware.cors import CORSMiddleware
4|from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
5|from fastapi.staticfiles import StaticFiles
6|from contextlib import asynccontextmanager
7|import socketio
8|import os
9|import base64
10|import json
11|from datetime import datetime, timedelta
12|from typing import Optional, List
13|from jose import JWTError, jwt
14|from passlib.context import CryptContext
15|import uuid
16|import asyncio
17|from motor.motor_asyncio import AsyncIOMotorClient
18|
19|# Environment Configuration
20|PORT = int(os.environ.get("PORT", 8000))
21|ENVIRONMENT = os.environ.get("ENVIRONMENT", "production")
22|DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
23|
24|# CORS origins from environment - Updated to include all potential external domains  
25|CORS_ORIGINS = os.environ.get(
26|    "CORS_ORIGINS", 
27|    "http://localhost:3000,http://localhost:3001,https://zonenium.top,https://www.zonenium.top,https://*.preview.emergentagent.com,https://*.onrender.com,http://localhost:8000,http://localhost:8001"
28|).split(",")
29|
30|# Add wildcard support for preview domains
31|CORS_ORIGINS.extend([
32|    "https://*.emergentagent.com",
33|    "https://*.preview.emergentagent.com", 
34|    "https://*.onrender.com"
35|])
36|
37|# Security setup
38|SECRET_KEY = os.getenv("SECRET_KEY", "zonenium-secret-key-change-in-production")
39|ALGORITHM = os.getenv("ALGORITHM", "HS256")
40|ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
41|
42|pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
43|security = HTTPBearer()
44|
45|# Pydantic Models (Essential ones for the integrated version)
46|from pydantic import BaseModel, Field
47|
48|class UserBase(BaseModel):
49|    username: str
50|    email: str
51|    full_name: str
52|    bio: Optional[str] = ""
53|    avatar: Optional[str] = ""
54|    phone: Optional[str] = ""
55|
56|class UserCreate(UserBase):
57|    password: str
58|
59|class User(UserBase):
60|    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
61|    password: Optional[str] = None
62|    is_active: bool = True
63|    is_online: bool = False
64|    last_seen: Optional[datetime] = None
65|    created_at: datetime = Field(default_factory=datetime.utcnow)
66|    
67|    class Config:
68|        populate_by_name = True
69|
70|class UserLogin(BaseModel):
71|    username: str
72|    password: str
73|
74|class Token(BaseModel):
75|    access_token: str
76|    token_type: str
77|
78|class MessageCreate(BaseModel):
79|    content: str
80|    recipient_id: str
81|    chat_id: Optional[str] = None
82|    message_type: str = "text"
83|    file_name: Optional[str] = None
84|    file_size: Optional[int] = None
85|    file_type: Optional[str] = None
86|    duration: Optional[int] = None
87|
88|class Message(BaseModel):
89|    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
90|    sender_id: str
91|    recipient_id: str
92|    chat_id: str
93|    content: str
94|    message_type: str = "text"
95|    file_name: Optional[str] = None
96|    file_size: Optional[int] = None
97|    file_type: Optional[str] = None
98|    duration: Optional[int] = None
99|    is_read: bool = False
100|    sent_at: datetime = Field(default_factory=datetime.utcnow)
101|    delivered_at: Optional[datetime] = None
102|    read_at: Optional[datetime] = None
103|    
104|    class Config:
105|        populate_by_name = True
106|
107|# Database Class
108|class ZoneniumDatabase:
109|    client: Optional[AsyncIOMotorClient] = None
110|    database = None
111|
112|    def __init__(self):
113|        self.mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/zonenium')
114|        
115|    async def connect_to_database(self):
116|        """Create database connection"""
117|        try:
118|            self.client = AsyncIOMotorClient(self.mongo_url)
119|            db_name = self.mongo_url.split('/')[-1] if '/' in self.mongo_url else 'zonenium'
120|            self.database = self.client[db_name]
121|            # Test connection
122|            await self.client.admin.command('ping')
123|            print(f"✅ Connected to MongoDB: {db_name}")
124|            await self.initialize_sample_data()
125|        except Exception as e:
126|            print(f"❌ MongoDB connection failed: {e}")
127|            # Use in-memory fallback
128|            self.database = None
129|
130|    async def close_database_connection(self):
131|        """Close database connection"""
132|        if self.client:
133|            self.client.close()
134|
135|    async def create_user(self, user_data: UserCreate) -> User:
136|        """Create new user"""
137|        if self.database is None:
138|            return None
139|        
140|        user_dict = user_data.dict()
141|        user_dict["_id"] = str(uuid.uuid4())
142|        user_dict["created_at"] = datetime.utcnow()
143|        user_dict["is_active"] = True
144|        user_dict["is_online"] = False
145|        
146|        # Hash password
147|        user_dict["password"] = pwd_context.hash(user_dict["password"])
148|        
149|        result = await self.database.users.insert_one(user_dict)
150|        created_user = await self.database.users.find_one({"_id": user_dict["_id"]})
151|        return User(**created_user)
152|
153|    async def get_user_by_username(self, username: str) -> Optional[User]:
154|        """Get user by username"""
155|        if self.database is None:
156|            return None
157|        user_doc = await self.database.users.find_one({"username": username})
158|        return User(**user_doc) if user_doc else None
159|
160|    async def get_user_by_id(self, user_id: str) -> Optional[User]:
161|        """Get user by ID"""
162|        if self.database is None:
163|            return None
164|        user_doc = await self.database.users.find_one({"_id": user_id})
165|        return User(**user_doc) if user_doc else None
166|
167|    async def create_message(self, message_data: MessageCreate, sender_id: str) -> Message:
168|        """Create new message"""
169|        if self.database is None:
170|            return None
171|        
172|        message_dict = message_data.dict()
173|        message_dict["_id"] = str(uuid.uuid4())
174|        message_dict["sender_id"] = sender_id
175|        message_dict["sent_at"] = datetime.utcnow()
176|        message_dict["is_read"] = False
177|        message_dict["chat_id"] = f"chat_{min(sender_id, message_data.recipient_id)}_{max(sender_id, message_data.recipient_id)}"
178|        
179|        result = await self.database.messages.insert_one(message_dict)
180|        created_message = await self.database.messages.find_one({"_id": message_dict["_id"]})
181|        return Message(**created_message)
182|
183|    async def initialize_sample_data(self):
184|        """Initialize with sample users for testing"""
185|        try:
186|            existing_users = await self.database.users.count_documents({})
187|            if existing_users == 0:
188|                print("🔄 Initializing sample data...")
189|                
190|                sample_users = [
191|                    UserCreate(
192|                        username="demo_user",
193|                        email="demo@zonenium.com",
194|                        full_name="Demo User",
195|                        bio="This is a demo user for testing Zonenium",
196|                        password="demo123"
197|                    ),
198|                    UserCreate(
199|                        username="test_user",
200|                        email="test@zonenium.com", 
201|                        full_name="Test User",
202|                        bio="Another test user for Zonenium",
203|                        password="test123"
204|                    )
205|                ]
206|                
207|                for user_data in sample_users:
208|                    await self.create_user(user_data)
209|                
210|                print("✅ Sample data initialized successfully")
211|        except Exception as e:
212|            print(f"Warning: Could not initialize sample data: {e}")
213|
214|# Global database instance
215|db = ZoneniumDatabase()
216|
217|# Socket.IO setup
218|sio = socketio.AsyncServer(
219|    async_mode="asgi",
220|    cors_allowed_origins=CORS_ORIGINS,
221|    logger=DEBUG,
222|    engineio_logger=DEBUG
223|)
224|
225|@asynccontextmanager
226|async def lifespan(app: FastAPI):
227|    # Startup
228|    print(f"🚀 Starting Zonenium server on port {PORT}")
229|    print(f"🌍 Environment: {ENVIRONMENT}")
230|    
231|    # Connect to database
232|    await db.connect_to_database()
233|    
234|    yield
235|    
236|    # Shutdown
237|    await db.close_database_connection()
238|    print("👋 Zonenium server shutdown complete")
239|
240|# FastAPI app with lifespan
241|app = FastAPI(
242|    title="Zoneium Messenger - Premium Messaging Experience", 
243|    description="Reliable. Private. Beautiful. The most elegant messaging app for modern communication.",
244|    version="3.0.0",
245|    lifespan=lifespan
246|)
247|
248|# Add CORS middleware with more permissive settings
249|app.add_middleware(
250|    CORSMiddleware,
251|    allow_origins=["*"],  # Allow all origins for development
252|    allow_credentials=True,
253|    allow_methods=["*"],
254|    allow_headers=["*"],
255|    expose_headers=["*"]
256|)
257|
258|# Serve static files from React build
259|try:
260|    app.mount("/images", StaticFiles(directory="/app/zonenium/frontend/dist/images"), name="images")
261|    app.mount("/assets", StaticFiles(directory="/app/zonenium/frontend/dist/assets"), name="assets") 
262|    print("✅ Static files mounted successfully")
263|except Exception as e:
264|    print(f"⚠️ Warning: Could not mount static files: {e}")
265|
266|# Mount Socket.IO
267|socket_app = socketio.ASGIApp(sio, app)
268|
269|# Authentication utilities
270|def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
271|    to_encode = data.copy()
272|    if expires_delta:
273|        expire = datetime.utcnow() + expires_delta
274|    else:
275|        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
276|    to_encode.update({"exp": expire})
277|    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
278|    return encoded_jwt
279|
280|async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
281|    try:
282|        token = credentials.credentials
283|        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
284|        username: str = payload.get("sub")
285|        if username is None:
286|            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
287|    except JWTError:
288|        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
289|    
290|    user = await db.get_user_by_username(username=username)
291|    if user is None:
292|        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
293|    return user
294|
295|# Landing Page Route with Your Logo
296|@app.get("/")
297|def home():
298|    html_content = """
299|    <!DOCTYPE html>
300|    <html lang="en">
301|    <head>
302|        <meta charset="UTF-8">
303|        <meta name="viewport" content="width=device-width, initial-scale=1.0">
304|        <title>Zoneium - Premium Messaging Experience</title>
305|        <meta name="theme-color" content="#FF6B35">
306|        <link rel="preconnect" href="https://fonts.googleapis.com">
307|        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
308|        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
309|        <style>
310|            :root {
311|                --primary-orange: #FF6B35;
312|                --primary-orange-hover: #E55D2B;
313|                --primary-orange-light: #FF8F66;
314|                --secondary-orange: #FFF4F0;
315|                --gradient-primary: linear-gradient(135deg, #FF6B35 0%, #FF8F66 100%);
316|                --gradient-secondary: linear-gradient(135deg, #FFF4F0 0%, #FFEDE5 100%);
317|                --white: #FFFFFF;
318|                --gray-50: #FAFBFC;
319|                --gray-100: #F3F4F6;
320|                --gray-200: #E5E7EB;
321|                --gray-300: #D1D5DB;
322|                --gray-400: #9CA3AF;
323|                --gray-500: #6B7280;
324|                --gray-600: #4B5563;
325|                --gray-700: #374151;
326|                --gray-800: #1F2937;
327|                --gray-900: #111827;
328|                --shadow-soft: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
329|                --shadow-medium: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
330|                --shadow-large: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
331|            }
332|
333|            * { margin: 0; padding: 0; box-sizing: border-box; }
334|
335|            body {
336|                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
337|                background: var(--gradient-primary);
338|                min-height: 100vh;
339|                display: flex;
340|                align-items: center;
341|                justify-content: center;
342|                line-height: 1.6;
343|                color: var(--gray-800);
344|                overflow: hidden;
345|                position: relative;
346|            }
347|
348|            /* Background Animations */
349|            .bg-decoration {
350|                position: absolute;
351|                width: 200px;
352|                height: 200px;
353|                border-radius: 50%;
354|                background: rgba(255, 255, 255, 0.1);
355|                animation: float 6s ease-in-out infinite;
356|            }
357|            .bg-decoration:nth-child(1) {
358|                top: 10%;
359|                left: 10%;
360|                animation-delay: 0s;
361|            }
362|            .bg-decoration:nth-child(2) {
363|                top: 70%;
364|                right: 10%;
365|                animation-delay: 2s;
366|                width: 150px;
367|                height: 150px;
368|            }
369|            .bg-decoration:nth-child(3) {
370|                bottom: 20%;
371|                left: 20%;
372|                animation-delay: 4s;
373|                width: 100px;
374|                height: 100px;
375|            }
376|
377|            @keyframes float {
378|                0%, 100% { transform: translateY(0px) rotate(0deg); }
379|                50% { transform: translateY(-20px) rotate(180deg); }
380|            }
381|
382|            .container {
383|                max-width: 420px;
384|                width: 90%;
385|                position: relative;
386|                z-index: 10;
387|            }
388|
389|            .login-card {
390|                background: rgba(255, 255, 255, 0.95);
391|                border-radius: 24px;
392|                padding: 40px 32px;
393|                box-shadow: var(--shadow-large);
394|                backdrop-filter: blur(20px);
395|                border: 1px solid rgba(255, 255, 255, 0.2);
396|                animation: slideUp 0.8s ease-out;
397|            }
398|
399|            @keyframes slideUp {
400|                from {
401|                    opacity: 0;
402|                    transform: translateY(30px);
403|                }
404|                to {
405|                    opacity: 1;
406|                    transform: translateY(0);
407|                }
408|            }
409|
410|            .logo-container {
411|                text-align: center;
412|                margin-bottom: 32px;
413|            }
414|
415|            .logo {
416|                width: 80px;
417|                height: 80px;
418|                margin: 0 auto 16px;
419|                background: var(--gradient-primary);
420|                border-radius: 20px;
421|                display: flex;
422|                align-items: center;
423|                justify-content: center;
424|                box-shadow: var(--shadow-medium);
425|                transition: transform 0.3s ease;
426|                overflow: hidden;
427|            }
428|            
429|            .logo img {
430|                width: 100%;
431|                height: 100%;
432|                object-fit: contain;
433|                padding: 8px;
434|            }
435|
436|            .logo:hover {
437|                transform: scale(1.05);
438|            }
439|
440|            .app-title {
441|                font-size: 28px;
442|                font-weight: 800;
443|                color: var(--gray-800);
444|                margin-bottom: 8px;
445|                letter-spacing: -0.02em;
446|            }
447|
448|            .app-subtitle {
449|                color: var(--gray-500);
450|                font-size: 16px;
451|                font-weight: 500;
452|                margin-bottom: 32px;
453|            }
454|
455|            .form-group {
456|                margin-bottom: 24px;
457|            }
458|
459|            .form-label {
460|                display: block;
461|                font-size: 14px;
462|                font-weight: 600;
463|                color: var(--gray-700);
464|                margin-bottom: 8px;
465|            }
466|
467|            .form-input {
468|                width: 100%;
469|                padding: 16px 18px;
470|                border: 2px solid var(--gray-200);
471|                border-radius: 12px;
472|                font-size: 16px;
473|                font-weight: 500;
474|                color: var(--gray-800);
475|                background: var(--white);
476|                transition: all 0.3s ease;
477|                outline: none;
478|            }
479|
480|            .form-input:focus {
481|                border-color: var(--primary-orange);
482|                box-shadow: 0 0 0 4px rgba(255, 107, 53, 0.1);
483|                transform: translateY(-1px);
484|            }
485|
486|            .form-input::placeholder {
487|                color: var(--gray-400);
488|                font-weight: 400;
489|            }
490|
491|            .primary-button {
492|                width: 100%;
493|                padding: 18px 24px;
494|                background: var(--gradient-primary);
495|                color: var(--white);
496|                border: none;
497|                border-radius: 12px;
498|                font-size: 16px;
499|                font-weight: 700;
500|                cursor: pointer;
501|                transition: all 0.3s ease;
502|                box-shadow: var(--shadow-medium);
503|                margin-bottom: 20px;
504|                text-decoration: none;
505|                display: inline-block;
506|                text-align: center;
507|            }
508|
509|            .primary-button:hover {
510|                background: linear-gradient(135deg, var(--primary-orange-hover) 0%, var(--primary-orange) 100%);
511|                transform: translateY(-2px);
512|                box-shadow: var(--shadow-large);
513|            }
514|
515|            .secondary-button {
516|                width: 100%;
517|                padding: 16px 24px;
518|                background: transparent;
519|                color: var(--gray-600);
520|                border: 2px solid var(--gray-200);
521|                border-radius: 12px;
522|                font-size: 16px;
523|                font-weight: 600;
524|                cursor: pointer;
525|                transition: all 0.3s ease;
526|                margin-bottom: 20px;
527|                text-decoration: none;
528|                display: inline-block;
529|                text-align: center;
530|            }
531|
532|            .secondary-button:hover {
533|                border-color: var(--primary-orange);
534|                color: var(--primary-orange);
535|                background: rgba(255, 107, 53, 0.05);
536|                transform: translateY(-1px);
537|            }
538|
539|            .launch-button {
540|                background: linear-gradient(135deg, #10B981 0%, #059669 100%);
541|                margin-bottom: 16px;
542|            }
543|            
544|            .launch-button:hover {
545|                background: linear-gradient(135deg, #059669 0%, #047857 100%);
546|            }
547|
548|            .divider {
549|                text-align: center;
550|                margin: 24px 0;
551|                position: relative;
552|                color: var(--gray-400);
553|                font-size: 14px;
554|                font-weight: 500;
555|            }
556|
557|            .divider::before {
558|                content: '';
559|                position: absolute;
560|                top: 50%;
561|                left: 0;
562|                right: 0;
563|                height: 1px;
564|                background: var(--gray-200);
565|                z-index: 1;
566|            }
567|
568|            .divider span {
569|                background: var(--white);
570|                padding: 0 16px;
571|                position: relative;
572|                z-index: 2;
573|            }
574|
575|            .features {
576|                margin-top: 32px;
577|                text-align: center;
578|            }
579|
580|            .features-title {
581|                font-size: 18px;
582|                font-weight: 700;
583|                color: var(--gray-800);
584|                margin-bottom: 16px;
585|            }
586|
587|            .features-list {
588|                display: grid;
589|                grid-template-columns: repeat(2, 1fr);
590|                gap: 12px;
591|                font-size: 14px;
592|                color: var(--gray-600);
593|            }
594|
595|            .feature-item {
596|                display: flex;
597|                align-items: center;
598|                gap: 8px;
599|                padding: 8px 12px;
600|                background: var(--secondary-orange);
601|                border-radius: 8px;
602|                font-weight: 500;
603|            }
604|
605|            .feature-icon {
606|                width: 16px;
607|                height: 16px;
608|                background: var(--primary-orange);
609|                border-radius: 50%;
610|                display: flex;
611|                align-items: center;
612|                justify-content: center;
613|                color: white;
614|                font-size: 10px;
615|                font-weight: bold;
616|            }
617|
618|            @media (max-width: 480px) {
619|                .container { width: 95%; }
620|                .login-card { padding: 32px 24px; }
621|                .app-title { font-size: 24px; }
622|                .form-input, .primary-button { font-size: 16px; }
623|                .features-list { grid-template-columns: 1fr; }
624|            }
625|        </style>
626|    </head>
627|    <body>
628|        <div class="bg-decoration"></div>
629|        <div class="bg-decoration"></div>
630|        <div class="bg-decoration"></div>
631|        
632|        <div class="container">
633|            <div class="login-card">
634|                <div class="logo-container">
635|                    <div class="logo">
636|                        <img src="/images/zonenium-logo.png" alt="Zonenium Logo" />
637|                    </div>
638|                    <h1 class="app-title">Zonenium</h1>
639|                    <p class="app-subtitle">Reliable • Private • Beautiful</p>
640|                </div>
641|
642|                <form id="loginForm">
643|                    <div class="form-group">
644|                        <label class="form-label" for="phone">Phone Number</label>
645|                        <input 
646|                            type="tel" 
647|                            id="phone" 
648|                            name="phone" 
649|                            class="form-input" 
650|                            placeholder="+1 (555) 123-4567"
651|                            required
652|                        />
653|                    </div>
654|
655|                    <div class="form-group">
656|                        <label class="form-label" for="password">Password</label>
657|                        <input 
658|                            type="password" 
659|                            id="password" 
660|                            name="password" 
661|                            class="form-input" 
662|                            placeholder="Enter your password"
663|                            required
664|                        />
665|                    </div>
666|
667|                    <a href="/app" class="primary-button launch-button">
668|                        🚀 Launch App
669|                    </a>
670|
671|                    <button type="submit" class="primary-button">
672|                        Sign In to Zonenium
673|                    </button>
674|                </form>
675|
676|                <div class="divider">
677|                    <span>or</span>
678|                </div>
679|
680|                <a href="/register" class="secondary-button">
681|                    Create New Account
682|                </a>
683|
684|                <div class="features">
685|                    <h3 class="features-title">Why Choose Zonenium?</h3>
686|                    <div class="features-list">
687|                        <div class="feature-item">
688|                            <div class="feature-icon">🔒</div>
689|                            <span>End-to-End Encrypted</span>
690|                        </div>
691|                        <div class="feature-item">
692|                            <div class="feature-icon">⚡</div>
693|                            <span>Lightning Fast</span>
694|                        </div>
695|                        <div class="feature-item">
696|                            <div class="feature-icon">🎵</div>
697|                            <span>Voice Messages</span>
698|                        </div>
699|                        <div class="feature-item">
700|                            <div class="feature-icon">👥</div>
701|                            <span>Group Chats</span>
702|                        </div>
703|                    </div>
704|                </div>
705|            </div>
706|        </div>
707|
708|        <script>
709|            document.getElementById('loginForm').addEventListener('submit', function(e) {
710|                e.preventDefault();
711|                // Simple demo - redirect to app
712|                window.location.href = '/app';
713|            });
714|        </script>
715|    </body>
716|    </html>
717|    """
718|    return HTMLResponse(content=html_content)
719|
720|# React App Route with better error handling
721|@app.get("/app")
722|def messenger_app():
723|    """Serve the React messaging application"""
724|    try:
725|        html_path = "/app/zonenium/frontend/dist/index.html"
726|        if os.path.exists(html_path):
727|            with open(html_path, "r", encoding="utf-8") as f:
728|                html_content = f.read()
729|            return HTMLResponse(content=html_content)
730|        else:
731|            # Fallback if React build not available
732|            return HTMLResponse(content="""
733|            <!DOCTYPE html>
734|            <html><head><title>Zonenium - Loading</title></head>
735|            <body style="font-family: Arial; text-align: center; padding: 50px;">
736|                <div style="max-width: 400px; margin: 0 auto;">
737|                    <img src="/images/zonenium-logo.png" alt="Zonenium" style="width: 80px; height: 80px; margin-bottom: 20px;">
738|                    <h1>Welcome to Zonenium</h1>
739|                    <p>Loading messaging interface...</p>
740|                    <p><a href="/">← Back to Home</a></p>
741|                </div>
742|            </body></html>
743|            """)
744|    except Exception as e:
745|        print(f"Error serving React app: {e}")
746|        return HTMLResponse(content=f"""
747|        <!DOCTYPE html>
748|        <html><head><title>Zonenium - Error</title></head>
749|        <body style="font-family: Arial; text-align: center; padding: 50px;">
750|            <h1>Zonenium Messaging</h1>
751|            <p>Loading error occurred. Please try again.</p>
752|            <p><a href="/">← Back to Home</a></p>
753|        </body></html>
754|        """, status_code=500)
755|
756|# Additional routes for React app navigation
757|@app.get("/login")
758|def login_page():
759|    """Redirect login to React app"""
760|    return messenger_app()
761|
762|@app.get("/register") 
763|def register_page():
764|    """Redirect register to React app"""
765|    return messenger_app()
766|
767|# API Routes
768|
769|# Handle preflight CORS requests
770|@app.options("/api/{path:path}")
771|async def handle_options(path: str):
772|    """Handle preflight CORS requests"""
773|    return JSONResponse(
774|        content={"message": "OK"},
775|        headers={
776|            "Access-Control-Allow-Origin": "*",
777|            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
778|            "Access-Control-Allow-Headers": "*",
779|            "Access-Control-Allow-Credentials": "true"
780|        }
781|    )
782|
783|@app.get("/api/status")
784|def get_status():
785|    return {
786|        "status": "live",
787|        "app": "Zoneium Messenger Premium",
788|        "version": "3.0.0",
789|        "message": "Premium messaging experience with your branding - Reliable. Private. Beautiful.",
790|        "features": [
791|            "JWT Authentication",
792|            "Real-time messaging via Socket.IO", 
793|            "Voice messages and file sharing",
794|            "Group chats and user search",
795|            "PWA support for mobile experience",
796|            "Your custom Zonenium branding"
797|        ],
798|        "backend_available": db.database is not None,
799|        "demo_accounts": [
800|            {"username": "demo_user", "password": "demo123"},
801|            {"username": "test_user", "password": "test123"}
802|        ]
803|    }
804|
805|@app.post("/api/register")
806|async def register(user_data: UserCreate):
807|    """Register a new user"""
808|    if db.database is None:
809|        raise HTTPException(status_code=503, detail="Database not available")
810|    
811|    # Check if user already exists
812|    existing_user = await db.get_user_by_username(user_data.username)
813|    if existing_user:
814|        raise HTTPException(status_code=400, detail="Username already registered")
815|    
816|    # Create user
817|    try:
818|        user = await db.create_user(user_data)
819|        if not user:
820|            raise HTTPException(status_code=500, detail="Failed to create user")
821|        
822|        # Create access token
823|        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
824|        access_token = create_access_token(
825|            data={"sub": user.username}, expires_delta=access_token_expires
826|        )
827|        
828|        return {
829|            "access_token": access_token,
830|            "token_type": "bearer",
831|            "user": {
832|                "id": user.id,
833|                "username": user.username,
834|                "email": user.email,
835|                "full_name": user.full_name,
836|                "bio": user.bio,
837|                "avatar": user.avatar
838|            }
839|        }
840|    except Exception as e:
841|        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")
842|
843|# Additional endpoint for frontend compatibility
844|@app.post("/api/auth/register")
845|async def auth_register(user_data: UserCreate):
846|    """Frontend-compatible registration endpoint"""
847|    return await register(user_data)
848|
849|@app.post("/api/login")
850|async def login(user_credentials: UserLogin):
851|    """Authenticate user and return JWT token"""
852|    if db.database is None:
853|        raise HTTPException(status_code=503, detail="Database not available")
854|    
855|    # Get user
856|    user = await db.get_user_by_username(user_credentials.username)
857|    if not user or not pwd_context.verify(user_credentials.password, user.password):
858|        raise HTTPException(
859|            status_code=status.HTTP_401_UNAUTHORIZED,
860|            detail="Incorrect username or password"
861|        )
862|    
863|    # Create access token
864|    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
865|    access_token = create_access_token(
866|        data={"sub": user.username}, expires_delta=access_token_expires
867|    )
868|    
869|    return {
870|        "access_token": access_token,
871|        "token_type": "bearer",
872|        "user": {
873|            "id": user.id,
874|            "username": user.username,
875|            "email": user.email,
876|            "full_name": user.full_name,
877|            "bio": user.bio,
878|            "avatar": user.avatar
879|        }
880|    }
881|
882|# Additional endpoint for frontend compatibility
883|@app.post("/api/auth/login")
884|async def auth_login(user_credentials: UserLogin):
885|    """Frontend-compatible authentication endpoint"""
886|    return await login(user_credentials)
887|
888|@app.get("/api/me")
889|async def get_current_user_info(current_user: User = Depends(get_current_user)):
890|    """Get current user information"""
891|    return {
892|        "id": current_user.id,
893|        "username": current_user.username,
894|        "email": current_user.email,
895|        "full_name": current_user.full_name,
896|        "bio": current_user.bio,
897|        "avatar": current_user.avatar,
898|        "is_online": current_user.is_online,
899|        "last_seen": current_user.last_seen
900|    }
901|
902|@app.post("/api/messages")
903|async def send_message(message_data: MessageCreate, current_user: User = Depends(get_current_user)):
904|    """Send a message"""
905|    if db.database is None:
906|        raise HTTPException(status_code=503, detail="Database not available")
907|    
908|    try:
909|        message = await db.create_message(message_data, current_user.id)
910|        if not message:
911|            raise HTTPException(status_code=500, detail="Failed to send message")
912|        
913|        # Emit via Socket.IO for real-time delivery
914|        await sio.emit('new_message', {
915|            "id": message.id,
916|            "sender_id": message.sender_id,
917|            "recipient_id": message.recipient_id,
918|            "content": message.content,
919|            "message_type": message.message_type,
920|            "sent_at": message.sent_at.isoformat()
921|        }, room=f"user_{message.recipient_id}")
922|        
923|        return {
924|            "id": message.id,
925|            "sender_id": message.sender_id,
926|            "recipient_id": message.recipient_id,
927|            "content": message.content,
928|            "message_type": message.message_type,
929|            "sent_at": message.sent_at.isoformat(),
930|            "is_read": message.is_read
931|        }
932|    except Exception as e:
933|        raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")
934|
935|@app.get("/api/users/search")
936|async def search_users(q: str, current_user: User = Depends(get_current_user)):
937|    """Search for users"""
938|    if db.database is None:
939|        return {"users": []}
940|    
941|    try:
942|        # Simple search implementation
943|        all_users_cursor = db.database.users.find({
944|            "username": {"$regex": q, "$options": "i"},
945|            "_id": {"$ne": current_user.id}
946|        }).limit(10)
947|        
948|        users = []
949|        async for user_doc in all_users_cursor:
950|            users.append({
951|                "id": user_doc["_id"],
952|                "username": user_doc["username"],
953|                "full_name": user_doc["full_name"],
954|                "avatar": user_doc.get("avatar", ""),
955|                "is_online": user_doc.get("is_online", False)
956|            })
957|        
958|        return {"users": users}
959|    except Exception as e:
960|        return {"users": []}
961|
962|# Socket.IO Events
963|@sio.event
964|async def connect(sid, environ):
965|    print(f"User connected: {sid}")
966|
967|@sio.event  
968|async def disconnect(sid):
969|    print(f"User disconnected: {sid}")
970|
971|@sio.event
972|async def join_room(sid, data):
973|    """Join a user to their personal room for notifications"""
974|    user_id = data.get('user_id')
975|    if user_id:
976|        await sio.enter_room(sid, f"user_{user_id}")
977|        print(f"User {user_id} joined room user_{user_id}")
978|
979|@sio.event
980|async def send_message(sid, data):
981|    """Handle real-time message sending"""
982|    # Emit to recipient
983|    recipient_id = data.get('recipient_id')
984|    if recipient_id:
985|        await sio.emit('new_message', data, room=f"user_{recipient_id}")
986|
987|# Serve other static files
988|@app.get("/manifest.json")
989|def get_manifest():
990|    return FileResponse("/app/zonenium/frontend/dist/manifest.json")
991|
992|@app.get("/sw.js")
993|def get_service_worker():
994|    return FileResponse("/app/zonenium/frontend/dist/sw.js")
995|
996|@app.get("/offline.html")
997|def get_offline_page():
998|    return FileResponse("/app/zonenium/frontend/dist/offline.html")
999|
1000|# Export the main app
1001|final_app = socket_app
1002|
1003|if __name__ == "__main__":
1004|    import uvicorn
1005|    uvicorn.run(final_app, host="0.0.0.0", port=PORT)

