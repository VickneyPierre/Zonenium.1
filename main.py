from fastapi import FastAPI
import os

app = FastAPI(title="Zonenium", description="WhatsApp-like messaging app")

@app.get("/")
def read_root():
    return {
        "app": "Zonenium",
        "message": "🎉 Zonenium is live!",
        "domain": "zonenium.top",
        "status": "success"
    }

@app.get("/api/status")
def health_check():
    return {"status": "healthy", "app": "zonenium"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
