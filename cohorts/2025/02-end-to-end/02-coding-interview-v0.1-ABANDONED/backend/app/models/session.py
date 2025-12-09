"""
Pydantic models for coding sessions and users.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class User(BaseModel):
    """Model representing a user in a coding session."""

    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., min_length=1, max_length=100)
    color: str = Field(default="#3B82F6")  # Default blue color

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "John Doe",
                "color": "#3B82F6",
            }
        }


class UserCreate(BaseModel):
    """Model for creating a new user."""

    name: str = Field(..., min_length=1, max_length=100)
    color: Optional[str] = Field(default="#3B82F6")


class Session(BaseModel):
    """Model representing a collaborative coding session."""

    id: UUID = Field(default_factory=uuid4)
    language: str = Field(default="python")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    users: List[User] = Field(default_factory=list)
    document: str = Field(default="# Write your code here\n")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "language": "python",
                "created_at": "2025-12-09T00:00:00Z",
                "users": [],
                "document": "# Write your code here\n",
            }
        }


class SessionCreate(BaseModel):
    """Model for creating a new session."""

    language: Optional[str] = Field(default="python")


class SessionResponse(BaseModel):
    """Response model for session creation."""

    id: UUID
    language: str
    created_at: datetime
    share_url: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "language": "python",
                "created_at": "2025-12-09T00:00:00Z",
                "share_url": "http://localhost:5173/session/123e4567-e89b-12d3-a456-426614174000",
            }
        }
