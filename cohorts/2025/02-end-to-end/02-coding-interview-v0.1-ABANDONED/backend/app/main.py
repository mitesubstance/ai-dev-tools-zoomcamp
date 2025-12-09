"""
FastAPI application for Collaborative Coding Interview Platform.

This module initializes the FastAPI app with CORS middleware and basic endpoints.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(
    title="Collaborative Coding Interview Platform API",
    description="REST API for managing coding interview sessions with real-time collaboration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
# TODO: Update origins for production deployment
origins = [
    "http://localhost:5173",  # Vite default dev server
    "http://localhost:3000",  # Alternative frontend port
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Status indicating the API is healthy
    """
    return {"status": "ok"}


@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        dict: API name and documentation links
    """
    return {
        "name": "Collaborative Coding Interview Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


# Future routes will be imported here
# from app.routes import sessions, websocket
# app.include_router(sessions.router)
# app.include_router(websocket.router)
