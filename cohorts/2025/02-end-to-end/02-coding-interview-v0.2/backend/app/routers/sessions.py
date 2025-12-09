"""
Session management HTTP endpoints (REQ-001)
"""
from fastapi import APIRouter, HTTPException, status
from app.models.session import SessionCreate, SessionResponse
from app.services.session_store import session_store
from app.services.connection_manager import connection_manager

router = APIRouter(
    prefix="/api/sessions",
    tags=["sessions"]
)


@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(session_data: SessionCreate = SessionCreate()):
    """
    Create a new coding session
    
    Args:
        session_data: Session creation parameters (language, etc.)
        
    Returns:
        SessionResponse: The newly created session information
    """
    session = session_store.create_session(language=session_data.language)
    return session.to_response()


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str):
    """
    Get information about a specific session
    
    Args:
        session_id: The unique session identifier (UUID)
        
    Returns:
        SessionResponse: Session information
        
    Raises:
        HTTPException: 404 if session not found
    """
    session = session_store.get_session(session_id)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found"
        )
    
    # Get the actual active user count from the connection manager
    response = session.to_response()
    response.active_users = connection_manager.get_connection_count(session_id)
    
    return response
