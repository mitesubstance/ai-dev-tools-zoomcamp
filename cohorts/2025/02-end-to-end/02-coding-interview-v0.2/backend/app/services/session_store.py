"""
In-memory session storage service
"""
import uuid
from typing import Dict, Optional
from datetime import datetime
from app.models.session import SessionData


class SessionStore:
    """
    In-memory storage for coding sessions
    
    This is a simple implementation using a dictionary.
    In production, consider using Redis or a database.
    """
    
    def __init__(self):
        self._sessions: Dict[str, SessionData] = {}
    
    def create_session(self, language: str = "python") -> SessionData:
        """
        Create a new session with a unique UUID
        
        Args:
            language: Programming language for the session (default: "python")
            
        Returns:
            SessionData: The newly created session
        """
        session_id = str(uuid.uuid4())
        session = SessionData(session_id=session_id, language=language)
        self._sessions[session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[SessionData]:
        """
        Retrieve a session by ID
        
        Args:
            session_id: The unique session identifier
            
        Returns:
            SessionData if found, None otherwise
        """
        return self._sessions.get(session_id)
    
    def update_session_code(self, session_id: str, code: str) -> bool:
        """
        Update the code content of a session
        
        Args:
            session_id: The unique session identifier
            code: The new code content
            
        Returns:
            True if successful, False if session not found
        """
        session = self.get_session(session_id)
        if session:
            session.code = code
            session.last_activity = datetime.now()
            return True
        return False
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session
        
        Args:
            session_id: The unique session identifier
            
        Returns:
            True if deleted, False if not found
        """
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False
    
    def session_exists(self, session_id: str) -> bool:
        """
        Check if a session exists
        
        Args:
            session_id: The unique session identifier
            
        Returns:
            True if session exists, False otherwise
        """
        return session_id in self._sessions
    
    def get_session_count(self) -> int:
        """Get the total number of active sessions"""
        return len(self._sessions)


# Global singleton instance
session_store = SessionStore()
