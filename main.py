# Zoneium - Professional Messaging Platform - Render Deployment Ready
import os
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import socketio
from datetime import datetime, timedelta
import uvicorn
from pathlib import Path
import json
import uuid
import motor.motor_asyncio
from passlib.context import CryptContext
import jwt
from typing import Optional

# Security setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# JWT Configuration
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

# Initialize FastAPI
app = FastAPI(
    title="Zoneium Messaging Platform",
    description="Professional messaging app with real-time features for zozenium.top",
    version="3.0.0"
)

# CORS configuration for zozenium.top
CORS_ORIGINS = os.environ.get(
    "CORS_ORIGINS", 
    "https://zozenium.top,https://www.zozenium.top,http://localhost:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = "zoneium_production"

class Database:
    client: Optional[motor.motor_asyncio.AsyncIOMotorClient] = None
    database = None

db = Database()

# Socket.IO setup
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=CORS_ORIGINS,
    logger=True
)

# Create Socket.IO ASGI app
socket_app = socketio.ASGIApp(sio, app)

# Utility functions
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = await db.database.users.find_one({"username": username})
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# Database operations
@app.on_event("startup")
async def startup_event():
    """Initialize database connection"""
    try:
        db.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
        db.database = db.client[DATABASE_NAME]
        
        # Test connection
        await db.client.admin.command('ping')
        print("✅ Database connected successfully")
        
        # Create indexes
        await db.database.users.create_index("username", unique=True)
        await db.database.users.create_index("email", unique=True)
        await db.database.messages.create_index([("chat_id", 1), ("timestamp", -1)])
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup database connection"""
    if db.client:
        db.client.close()

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check for Render monitoring"""
    try:
        # Test database connection
        db_status = "ok"
        if db.database:
            try:
                await db.client.admin.command('ping')
            except:
                db_status = "error"
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "3.0.0",
            "environment": os.environ.get("ENVIRONMENT", "development"),
            "database": db_status,
            "domain": "zozenium.top"
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

# Authentication endpoints
@app.post("/api/register")
async def register(request: Request):
    """User registration"""
    try:
        data = await request.json()
        username = data.get("username")
        email = data.get("email") 
        password = data.get("password")
        full_name = data.get("full_name", "")
        
        if not username or not email or not password:
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        # Check if user exists
        existing_user = await db.database.users.find_one({
            "$or": [{"username": username}, {"email": email}]
        })
        
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        
        # Create new user
        user_id = str(uuid.uuid4())
        hashed_password = hash_password(password)
        
        user_doc = {
            "user_id": user_id,
            "username": username,
            "email": email,
            "full_name": full_name,
            "password_hash": hashed_password,
            "created_at": datetime.utcnow(),
            "is_online": False,
            "status": "Hey there! I am using Zoneium.",
            "avatar_url": ""
        }
        
        await db.database.users.insert_one(user_doc)
        
        # Create access token
        token = create_access_token(data={"sub": username})
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "user_id": user_id,
                "username": username,
                "full_name": full_name,
                "email": email,
                "avatar_url": "",
                "status": user_doc["status"]
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/login")
async def login(request: Request):
    """User login"""
    try:
        data = await request.json()
        username = data.get("username")
        password = data.get("password")
        
        if not username or not password:
            raise HTTPException(status_code=400, detail="Username and password required")
        
        # Find user
        user = await db.database.users.find_one({"username": username})
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Verify password
        if not verify_password(password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Update online status
        await db.database.users.update_one(
            {"user_id": user["user_id"]},
            {"$set": {"is_online": True, "last_seen": datetime.utcnow()}}
        )
        
        # Create access token
        token = create_access_token(data={"sub": username})
        
        return {
            "access_token": token,
            "token_type": "bearer", 
            "user": {
                "user_id": user["user_id"],
                "username": user["username"],
                "full_name": user.get("full_name", ""),
                "email": user["email"],
                "avatar_url": user.get("avatar_url", ""),
                "status": user.get("status", "")
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Basic messaging endpoints
@app.get("/api/chats")
async def get_user_chats(current_user: dict = Depends(get_current_user)):
    """Get user's chats"""
    try:
        chats_cursor = db.database.chats.find({
            "participants": {"$in": [current_user["user_id"]]}
        }).sort("last_message_time", -1).limit(50)
        
        chats = []
        async for chat in chats_cursor:
            chat["_id"] = str(chat["_id"])
            chats.append(chat)
        
        return {"chats": chats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/messages/{chat_id}")
async def get_messages(chat_id: str, current_user: dict = Depends(get_current_user)):
    """Get messages for a chat"""
    try:
        messages_cursor = db.database.messages.find({
            "chat_id": chat_id
        }).sort("timestamp", -1).limit(50)
        
        messages = []
        async for message in messages_cursor:
            message["_id"] = str(message["_id"])
            messages.append(message)
        
        messages.reverse()  # Reverse to get chronological order
        return {"messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/users/search")
async def search_users(query: str, current_user: dict = Depends(get_current_user)):
    """Search for users"""
    try:
        if len(query) < 2:
            return {"users": []}
        
        users_cursor = db.database.users.find({
            "$or": [
                {"username": {"$regex": query, "$options": "i"}},
                {"full_name": {"$regex": query, "$options": "i"}}
            ],
            "user_id": {"$ne": current_user["user_id"]}
        }).limit(10)
        
        users = []
        async for user in users_cursor:
            users.append({
                "user_id": user["user_id"],
                "username": user["username"],
                "full_name": user.get("full_name", ""),
                "avatar_url": user.get("avatar_url", ""),
                "is_online": user.get("is_online", False)
            })
        
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Frontend serving
@app.get("/")
async def serve_frontend():
    """Serve React frontend"""
    frontend_path = Path("frontend/dist/index.html")
    if frontend_path.exists():
        return FileResponse(frontend_path)
    else:
        return {
            "message": "🚀 Zoneium API is running!", 
            "version": "3.0.0",
            "domain": "zozenium.top",
            "status": "healthy"
        }

# Socket.IO events
@sio.event
async def connect(sid, environ):
    """Handle client connection"""
    print(f"Client {sid} connected")

@sio.event
async def disconnect(sid):
    """Handle client disconnection""" 
    print(f"Client {sid} disconnected")

@sio.event
async def join_chat(sid, data):
    """Join a chat room"""
    try:
        chat_id = data.get("chat_id")
        if chat_id:
            await sio.enter_room(sid, chat_id)
            print(f"Client {sid} joined chat {chat_id}")
    except Exception as e:
        print(f"Error joining chat: {e}")

@sio.event
async def send_message(sid, data):
    """Handle message sending"""
    try:
        message_id = str(uuid.uuid4())
        chat_id = data.get("chat_id")
        sender_id = data.get("sender_id") 
        content = data.get("content")
        
        if not all([chat_id, sender_id, content]):
            await sio.emit("error", {"message": "Missing required fields"}, room=sid)
            return
        
        message = {
            "message_id": message_id,
            "chat_id": chat_id,
            "sender_id": sender_id,
            "content": content,
            "timestamp": datetime.utcnow(),
            "message_type": "text"
        }
        
        # Save to database
        await db.database.messages.insert_one(message)
        
        # Update chat's last message time
        await db.database.chats.update_one(
            {"chat_id": chat_id},
            {"$set": {"last_message_time": datetime.utcnow()}}
        )
        
        # Convert datetime for JSON serialization
        message["timestamp"] = message["timestamp"].isoformat()
        
        # Emit to chat room
        await sio.emit("new_message", message, room=chat_id)
        
    except Exception as e:
        await sio.emit("error", {"message": str(e)}, room=sid)

# Run the application
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(socket_app, host="0.0.0.0", port=port)
