"""
FastAPI Backend for Real-Time Collaborative Coding Interview Platform
Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import datetime
from pathlib import Path
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


# Serve frontend static files in production (when running in Docker)
frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    # Mount static assets (JS, CSS, images, etc.)
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")
    
    # Serve index.html for root and any unmatched routes (SPA routing)
    @app.get("/")
    async def serve_frontend():
        """Serve the frontend application"""
        return FileResponse(str(frontend_dist / "index.html"))
    
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """
        Catch-all route for SPA - serves index.html for any route not matched by API
        This allows React Router to handle routing on the client side
        """
        # If path starts with /api or /ws, don't intercept (let 404 happen)
        if full_path.startswith("api/") or full_path.startswith("ws/"):
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="API endpoint not found")
        
        # Check if file exists in dist (e.g., favicon, robots.txt)
        file_path = frontend_dist / full_path
        if file_path.is_file():
            return FileResponse(str(file_path))
        
        # Otherwise, serve index.html for SPA routing
        return FileResponse(str(frontend_dist / "index.html"))
else:
    # Development mode - API only
    @app.get("/")
    async def root():
        """Root endpoint - Development mode"""
        return {
            "message": "Coding Interview Platform API",
            "version": "0.2.0",
            "status": "running",
            "mode": "development"
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
