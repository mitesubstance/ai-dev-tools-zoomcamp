"""
Session data models
"""
from datetime import datetime
from typing import Set, Optional
from pydantic import BaseModel, Field
from fastapi import WebSocket


class SessionCreate(BaseModel):
    """Request model for creating a new session"""
    language: str = Field(default="python", description="Programming language for the session")


class SessionResponse(BaseModel):
    """Response model for session information"""
    session_id: str = Field(description="Unique session identifier (UUID)")
    language: str = Field(description="Programming language")
    created_at: str = Field(description="ISO format timestamp of session creation")
    active_users: int = Field(default=0, description="Number of currently connected users")


class SessionData:
    """Internal session data structure (not for API responses)"""
    def __init__(self, session_id: str, language: str = "python"):
        self.session_id = session_id
        self.code = "# Write your Python code here\n"
        self.language = language
        self.connections: Set[WebSocket] = set()
        self.created_at = datetime.now()
        self.last_activity = datetime.now()

    def to_response(self) -> SessionResponse:
        """Convert to API response model"""
        return SessionResponse(
            session_id=self.session_id,
            language=self.language,
            created_at=self.created_at.isoformat(),
            active_users=len(self.connections)
        )
