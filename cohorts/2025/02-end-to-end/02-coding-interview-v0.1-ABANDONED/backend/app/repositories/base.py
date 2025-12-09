"""
Abstract base repository for session storage.
"""

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from app.models.session import Session, User


class SessionRepository(ABC):
    """Abstract base class for session storage."""

    @abstractmethod
    async def create(self, session: Session) -> Session:
        """Create a new session."""
        pass

    @abstractmethod
    async def get(self, session_id: UUID) -> Optional[Session]:
        """Get a session by ID."""
        pass

    @abstractmethod
    async def delete(self, session_id: UUID) -> bool:
        """Delete a session."""
        pass

    @abstractmethod
    async def add_user(self, session_id: UUID, user: User) -> Optional[Session]:
        """Add a user to a session."""
        pass

    @abstractmethod
    async def remove_user(self, session_id: UUID, user_id: UUID) -> Optional[Session]:
        """Remove a user from a session."""
        pass

    @abstractmethod
    async def update_document(self, session_id: UUID, document: str) -> Optional[Session]:
        """Update the document content of a session."""
        pass
