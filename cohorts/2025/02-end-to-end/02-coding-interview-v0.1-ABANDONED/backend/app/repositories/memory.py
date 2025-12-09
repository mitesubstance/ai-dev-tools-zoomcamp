"""
In-memory implementation of session repository.
"""

from typing import Dict, Optional
from uuid import UUID

from app.models.session import Session, User
from .base import SessionRepository


class InMemorySessionRepository(SessionRepository):
    """In-memory implementation of session storage."""

    def __init__(self):
        self._sessions: Dict[UUID, Session] = {}

    async def create(self, session: Session) -> Session:
        """Create a new session."""
        self._sessions[session.id] = session
        return session

    async def get(self, session_id: UUID) -> Optional[Session]:
        """Get a session by ID."""
        return self._sessions.get(session_id)

    async def delete(self, session_id: UUID) -> bool:
        """Delete a session."""
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False

    async def add_user(self, session_id: UUID, user: User) -> Optional[Session]:
        """Add a user to a session."""
        session = self._sessions.get(session_id)
        if session:
            # Check if user already exists
            if not any(u.id == user.id for u in session.users):
                session.users.append(user)
        return session

    async def remove_user(self, session_id: UUID, user_id: UUID) -> Optional[Session]:
        """Remove a user from a session."""
        session = self._sessions.get(session_id)
        if session:
            session.users = [u for u in session.users if u.id != user_id]
        return session

    async def update_document(self, session_id: UUID, document: str) -> Optional[Session]:
        """Update the document content of a session."""
        session = self._sessions.get(session_id)
        if session:
            session.document = document
        return session
