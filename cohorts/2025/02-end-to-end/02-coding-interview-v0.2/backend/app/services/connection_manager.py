"""
WebSocket connection manager for real-time communication (REQ-005)
"""
import json
from typing import Dict, Set
from fastapi import WebSocket
from datetime import datetime


class ConnectionManager:
    """
    Manages WebSocket connections for real-time collaboration
    
    Handles connection tracking and message broadcasting per session
    """
    
    def __init__(self):
        # Map of session_id -> set of active WebSocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        """
        Accept a new WebSocket connection and add it to the session
        
        Args:
            websocket: The WebSocket connection
            session_id: The session to join
        """
        await websocket.accept()
        
        if session_id not in self.active_connections:
            self.active_connections[session_id] = set()
        
        self.active_connections[session_id].add(websocket)
    
    def disconnect(self, websocket: WebSocket, session_id: str):
        """
        Remove a WebSocket connection from the session
        
        Args:
            websocket: The WebSocket connection to remove
            session_id: The session to leave
        """
        if session_id in self.active_connections:
            self.active_connections[session_id].discard(websocket)
            
            # Clean up empty session connection sets
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """
        Send a message to a specific WebSocket connection
        
        Args:
            message: The message dict to send (will be JSON-encoded)
            websocket: The target WebSocket connection
        """
        await websocket.send_text(json.dumps(message))
    
    async def broadcast_to_session(self, message: dict, session_id: str, exclude: WebSocket = None):
        """
        Broadcast a message to all connections in a session
        
        Args:
            message: The message dict to broadcast (will be JSON-encoded)
            session_id: The session to broadcast to
            exclude: Optional WebSocket to exclude from broadcast (e.g., the sender)
        """
        if session_id not in self.active_connections:
            return
        
        message_json = json.dumps(message)
        
        # Create a copy of the set to avoid modification during iteration
        connections = self.active_connections[session_id].copy()
        
        for connection in connections:
            if connection != exclude:
                try:
                    await connection.send_text(message_json)
                except Exception:
                    # Connection might be closed, will be cleaned up on disconnect
                    pass
    
    def get_connection_count(self, session_id: str) -> int:
        """
        Get the number of active connections for a session
        
        Args:
            session_id: The session to check
            
        Returns:
            Number of active connections
        """
        if session_id in self.active_connections:
            return len(self.active_connections[session_id])
        return 0


# Global singleton instance
connection_manager = ConnectionManager()
