
from fastapi import FastAPI
from datetime import datetime, timezone
import socket

app = FastAPI(title="Infrastructure Lab API")

@app.get("/")
def home():
    return {
        "message": "Infrastructure Lab API is running",
        "server": socket.gethostname(),
        "status": "online"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
