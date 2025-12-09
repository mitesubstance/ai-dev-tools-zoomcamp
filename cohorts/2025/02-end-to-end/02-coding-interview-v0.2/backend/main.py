"""
FastAPI Backend for Real-Time Collaborative Coding Interview Platform
Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from app.routers import sessions, websocket

# Create FastAPI application
app = FastAPI(
    title="Coding Interview Platform API",
    description="Real-time collaborative coding interview platform",
    version="0.2.0"
)

# Configure CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(sessions.router)
app.include_router(websocket.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Coding Interview Platform API",
        "version": "0.2.0",
        "status": "running"
    }


@app.get("/api/health")
async def health_check():
    """
    Health check endpoint
    Returns server status and timestamp
    """
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "service": "coding-interview-backend"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
