"""
WebSocket endpoint for real-time collaborative editing (REQ-002, REQ-005)
"""
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from fastapi.responses import JSONResponse
from app.services.connection_manager import connection_manager
from app.services.session_store import session_store
from datetime import datetime

router = APIRouter()


@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for real-time collaborative editing
    
    Args:
        websocket: The WebSocket connection
        session_id: The session to join
        
    Message Types:
        - code_update: Broadcast code changes to all users
        - user_joined: Notify when a user joins
        - user_left: Notify when a user leaves
        - session_state: Send current session state to new user
    """
    # Verify session exists
    session = session_store.get_session(session_id)
    if not session:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    # Connect the WebSocket
    await connection_manager.connect(websocket, session_id)
    
    # Add connection to session's connection set
    session.connections.add(websocket)
    
    try:
        # Send current session state to the newly connected user
        await connection_manager.send_personal_message(
            {
                "type": "session_state",
                "data": {
                    "code": session.code,
                    "language": session.language,
                    "active_users": connection_manager.get_connection_count(session_id)
                }
            },
            websocket
        )
        
        # Notify others that a user joined
        await connection_manager.broadcast_to_session(
            {
                "type": "user_joined",
                "data": {
                    "user_count": connection_manager.get_connection_count(session_id)
                }
            },
            session_id,
            exclude=websocket
        )
        
        # Listen for messages
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            message_type = message.get("type")
            message_data = message.get("data", {})
            
            if message_type == "code_update":
                # Update session code
                code = message_data.get("code", "")
                session_store.update_session_code(session_id, code)
                
                # Broadcast to all other users in the session
                await connection_manager.broadcast_to_session(
                    {
                        "type": "code_update",
                        "data": {
                            "code": code,
                            "timestamp": datetime.now().isoformat()
                        }
                    },
                    session_id,
                    exclude=websocket
                )
            
    except WebSocketDisconnect:
        # Handle disconnection
        connection_manager.disconnect(websocket, session_id)
        
        # Remove connection from session's connection set
        session.connections.discard(websocket)
        
        # Notify others that a user left
        await connection_manager.broadcast_to_session(
            {
                "type": "user_left",
                "data": {
                    "user_count": connection_manager.get_connection_count(session_id)
                }
            },
            session_id
        )
    
    except Exception as e:
        # Handle other errors
        connection_manager.disconnect(websocket, session_id)
        
        # Remove connection from session's connection set
        session.connections.discard(websocket)
        
        # Optionally log the error
        print(f"WebSocket error in session {session_id}: {str(e)}")
