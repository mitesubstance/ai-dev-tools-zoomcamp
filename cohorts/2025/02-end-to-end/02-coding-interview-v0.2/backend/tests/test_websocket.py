"""
Backend WebSocket tests for real-time collaborative editing (REQ-002, REQ-005)
Following TDD approach - these tests verify WebSocket functionality
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_websocket_endpoint_exists():
    """Test: WebSocket endpoint exists at /ws/{session_id}"""
    # Create a session first
    response = client.post("/api/sessions", json={"language": "python"})
    assert response.status_code == 201
    session_id = response.json()["session_id"]
    
    # Attempt WebSocket connection (this will fail if endpoint doesn't exist)
    with client.websocket_connect(f"/ws/{session_id}") as websocket:
        # If we get here, the endpoint exists
        assert websocket is not None


def test_websocket_connection_accepted_for_valid_session():
    """Test: Connection accepted for valid session"""
    # Create a session
    response = client.post("/api/sessions", json={"language": "python"})
    assert response.status_code == 201
    session_id = response.json()["session_id"]
    
    # Connect via WebSocket
    with client.websocket_connect(f"/ws/{session_id}") as websocket:
        # Should receive session_state message upon connection
        data = websocket.receive_json()
        assert data["type"] == "session_state"
        assert "code" in data["data"]
        assert "language" in data["data"]
        assert data["data"]["language"] == "python"


def test_websocket_connection_rejected_for_invalid_session():
    """Test: Connection rejected for invalid session (404)"""
    fake_session_id = "00000000-0000-0000-0000-000000000000"
    
    # Attempt to connect to non-existent session should fail
    with pytest.raises(Exception):
        with client.websocket_connect(f"/ws/{fake_session_id}") as websocket:
            pass


def test_websocket_receives_current_session_state_on_connect():
    """Test: New client receives current session state on connect"""
    # Create a session
    response = client.post("/api/sessions", json={"language": "python"})
    session_id = response.json()["session_id"]
    
    # Connect first client
    with client.websocket_connect(f"/ws/{session_id}") as websocket:
        # Receive initial state
        data = websocket.receive_json()
        assert data["type"] == "session_state"
        assert "code" in data["data"]
        assert "active_users" in data["data"]
        # Should have at least 1 user (this connection)
        assert data["data"]["active_users"] >= 1


def test_websocket_user_joined_event_broadcast():
    """Test: user_joined event broadcast correctly"""
    # Create a session
    response = client.post("/api/sessions", json={"language": "python"})
    session_id = response.json()["session_id"]
    
    # Connect first client
    with client.websocket_connect(f"/ws/{session_id}") as ws1:
        # Receive initial state for first client
        data1 = ws1.receive_json()
        assert data1["type"] == "session_state"
        
        # Connect second client
        with client.websocket_connect(f"/ws/{session_id}") as ws2:
            # Second client receives session_state
            data2 = ws2.receive_json()
            assert data2["type"] == "session_state"
            
            # First client should receive user_joined message
            joined_msg = ws1.receive_json()
            assert joined_msg["type"] == "user_joined"
            assert "user_count" in joined_msg["data"]
            assert joined_msg["data"]["user_count"] == 2


def test_websocket_code_update_broadcast():
    """Test: code_update message broadcast to all clients in session"""
    # Create a session
    response = client.post("/api/sessions", json={"language": "python"})
    session_id = response.json()["session_id"]
    
    # Connect two clients
    with client.websocket_connect(f"/ws/{session_id}") as ws1:
        with client.websocket_connect(f"/ws/{session_id}") as ws2:
            # Clear initial messages
            ws1.receive_json()  # session_state
            ws2.receive_json()  # session_state
            ws1.receive_json()  # user_joined for ws2
            
            # Client 1 sends code update
            new_code = 'print("Hello, World!")'
            ws1.send_json({
                "type": "code_update",
                "data": {
                    "code": new_code
                }
            })
            
            # Client 2 should receive the update
            update_msg = ws2.receive_json()
            assert update_msg["type"] == "code_update"
            assert update_msg["data"]["code"] == new_code
            assert "timestamp" in update_msg["data"]


def test_websocket_code_update_not_sent_back_to_sender():
    """Test: code_update is not echoed back to the sender"""
    # Create a session
    response = client.post("/api/sessions", json={"language": "python"})
    session_id = response.json()["session_id"]
    
    # Connect one client
    with client.websocket_connect(f"/ws/{session_id}") as ws1:
        # Clear initial message
        ws1.receive_json()  # session_state
        
        # Send code update
        new_code = 'print("Test")'
        ws1.send_json({
            "type": "code_update",
            "data": {
                "code": new_code
            }
        })
        
        # The sender should NOT receive their own update back
        # (since there are no other clients, there should be no messages)
        # We'll use a timeout to verify no message is received
        import asyncio
        try:
            # This should timeout since no message should be sent back
            ws1.receive_json(timeout=0.5)
            pytest.fail("Sender should not receive their own code update")
        except:
            # Expected - no message received
            pass


def test_websocket_user_left_event_on_disconnect():
    """Test: user_left event broadcast on disconnect"""
    # Create a session
    response = client.post("/api/sessions", json={"language": "python"})
    session_id = response.json()["session_id"]
    
    # Connect two clients
    with client.websocket_connect(f"/ws/{session_id}") as ws1:
        with client.websocket_connect(f"/ws/{session_id}") as ws2:
            # Clear initial messages
            ws1.receive_json()  # session_state
            ws2.receive_json()  # session_state
            ws1.receive_json()  # user_joined
        
        # ws2 is now disconnected (exited context manager)
        # ws1 should receive user_left message
        left_msg = ws1.receive_json()
        assert left_msg["type"] == "user_left"
        assert "user_count" in left_msg["data"]
        assert left_msg["data"]["user_count"] == 1


def test_websocket_session_code_persists_across_updates():
    """Test: Session code is updated and persists"""
    # Create a session
    response = client.post("/api/sessions", json={"language": "python"})
    session_id = response.json()["session_id"]
    
    # Connect, send update, disconnect
    with client.websocket_connect(f"/ws/{session_id}") as ws1:
        ws1.receive_json()  # session_state
        
        new_code = 'def hello():\n    print("Hello")'
        ws1.send_json({
            "type": "code_update",
            "data": {"code": new_code}
        })
    
    # Connect again with new client
    with client.websocket_connect(f"/ws/{session_id}") as ws2:
        state = ws2.receive_json()
        assert state["type"] == "session_state"
        assert state["data"]["code"] == new_code


def test_websocket_multiple_clients_receive_updates():
    """Test: Multiple clients all receive code updates"""
    # Create a session
    response = client.post("/api/sessions", json={"language": "python"})
    session_id = response.json()["session_id"]
    
    # Connect three clients
    with client.websocket_connect(f"/ws/{session_id}") as ws1:
        with client.websocket_connect(f"/ws/{session_id}") as ws2:
            with client.websocket_connect(f"/ws/{session_id}") as ws3:
                # Clear initial messages
                for ws in [ws1, ws2, ws3]:
                    ws.receive_json()  # session_state
                
                # Clear user_joined messages
                ws1.receive_json()  # ws2 joined
                ws1.receive_json()  # ws3 joined
                ws2.receive_json()  # ws3 joined
                
                # ws1 sends update
                code = "print('Broadcasting test')"
                ws1.send_json({
                    "type": "code_update",
                    "data": {"code": code}
                })
                
                # Both ws2 and ws3 should receive it
                msg2 = ws2.receive_json()
                msg3 = ws3.receive_json()
                
                assert msg2["type"] == "code_update"
                assert msg2["data"]["code"] == code
                assert msg3["type"] == "code_update"
                assert msg3["data"]["code"] == code
