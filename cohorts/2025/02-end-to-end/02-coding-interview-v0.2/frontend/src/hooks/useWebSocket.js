/**
 * WebSocket hook for real-time collaborative editing
 */
import { useEffect, useRef, useState, useCallback } from 'react';

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000';

/**
 * WebSocket connection states
 */
export const ConnectionState = {
  CONNECTING: 'connecting',
  CONNECTED: 'connected',
  DISCONNECTED: 'disconnected',
  ERROR: 'error',
};

/**
 * Custom hook for managing WebSocket connections
 * @param {string} sessionId - The session ID to connect to
 * @param {Function} onMessage - Callback for incoming messages
 * @returns {Object} WebSocket connection state and methods
 */
export function useWebSocket(sessionId, onMessage) {
  const [connectionState, setConnectionState] = useState(ConnectionState.DISCONNECTED);
  const [userCount, setUserCount] = useState(0);
  const wsRef = useRef(null);
  const onMessageRef = useRef(onMessage);
  const shouldReconnect = useRef(true);

  // Keep onMessage ref up to date
  useEffect(() => {
    onMessageRef.current = onMessage;
  }, [onMessage]);

  /**
   * Send a message through the WebSocket connection
   */
  const sendMessage = useCallback((message) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    } else {
      console.warn('WebSocket is not connected');
    }
  }, []);

  /**
   * Disconnect from WebSocket server
   */
  const disconnect = useCallback(() => {
    shouldReconnect.current = false;
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
    setConnectionState(ConnectionState.DISCONNECTED);
  }, []);

  // Main connection effect
  useEffect(() => {
    if (!sessionId) return;

    let reconnectAttempts = 0;
    const maxReconnectAttempts = 5;
    let reconnectTimeout = null;
    shouldReconnect.current = true;

    function connect() {
      if (!shouldReconnect.current) return;

      setConnectionState(ConnectionState.CONNECTING);

      try {
        const ws = new WebSocket(`${WS_URL}/ws/${sessionId}`);
        wsRef.current = ws;

        ws.onopen = () => {
          console.log('WebSocket connected');
          setConnectionState(ConnectionState.CONNECTED);
          reconnectAttempts = 0;
        };

        ws.onmessage = (event) => {
          try {
            const message = JSON.parse(event.data);
            
            // Handle user count updates
            if (message.type === 'user_joined' || message.type === 'user_left') {
              setUserCount(message.data.user_count);
            }
            
            // Handle session state on initial connection
            if (message.type === 'session_state') {
              setUserCount(message.data.active_users);
            }

            // Pass message to parent component
            if (onMessageRef.current) {
              onMessageRef.current(message);
            }
          } catch (error) {
            console.error('Error parsing WebSocket message:', error);
          }
        };

        ws.onerror = (error) => {
          console.error('WebSocket error:', error);
          setConnectionState(ConnectionState.ERROR);
        };

        ws.onclose = () => {
          console.log('WebSocket disconnected');
          setConnectionState(ConnectionState.DISCONNECTED);
          wsRef.current = null;

          // Attempt to reconnect with exponential backoff
          if (shouldReconnect.current && reconnectAttempts < maxReconnectAttempts) {
            const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), 10000);
            reconnectAttempts += 1;
            
            console.log(`Reconnecting in ${delay}ms (attempt ${reconnectAttempts})`);
            
            reconnectTimeout = setTimeout(() => {
              connect();
            }, delay);
          }
        };
      } catch (error) {
        console.error('Failed to create WebSocket connection:', error);
        setConnectionState(ConnectionState.ERROR);
      }
    }

    connect();
    
    return () => {
      shouldReconnect.current = false;
      if (reconnectTimeout) {
        clearTimeout(reconnectTimeout);
      }
      if (wsRef.current) {
        wsRef.current.close();
        wsRef.current = null;
      }
    };
  }, [sessionId]);

  return {
    connectionState,
    userCount,
    sendMessage,
    disconnect,
  };
}
