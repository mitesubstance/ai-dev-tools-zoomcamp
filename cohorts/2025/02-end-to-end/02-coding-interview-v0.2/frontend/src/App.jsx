/**
 * Main App component for Collaborative Coding Interview Platform
 */
import { useState, useEffect, useCallback } from 'react';
import { CodeEditor } from './components/CodeEditor';
import { ConnectionStatus } from './components/ConnectionStatus';
import { OutputPanel } from './components/OutputPanel';
import { useWebSocket } from './hooks/useWebSocket';
import { createSession, getSession } from './services/api';
import './App.css';

function App() {
  const [sessionId, setSessionId] = useState(null);
  const [code, setCode] = useState('# Write your Python code here\n');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Get session ID from URL on mount
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const urlSessionId = params.get('session');
    
    if (urlSessionId) {
      setSessionId(urlSessionId);
      // Load session data
      getSession(urlSessionId)
        .then((data) => {
          console.log('Loaded session:', data);
        })
        .catch((err) => {
          setError('Failed to load session');
          console.error(err);
        });
    }
  }, []);

  // Handle WebSocket messages
  const handleMessage = useCallback((message) => {
    if (message.type === 'code_update') {
      setCode(message.data.code);
    } else if (message.type === 'session_state') {
      setCode(message.data.code);
    }
  }, []);

  // WebSocket connection
  const { connectionState, userCount, sendMessage } = useWebSocket(
    sessionId,
    handleMessage
  );

  // Handle code changes from the editor
  const handleCodeChange = useCallback((newCode) => {
    setCode(newCode);
    
    // Send update to other users
    if (sessionId) {
      sendMessage({
        type: 'code_update',
        data: {
          code: newCode,
          timestamp: Date.now(),
        },
      });
    }
  }, [sessionId, sendMessage]);

  // Create a new session
  const handleCreateSession = async () => {
    setLoading(true);
    setError(null);

    try {
      const session = await createSession('python');
      setSessionId(session.session_id);
      
      // Update URL
      const url = new URL(window.location);
      url.searchParams.set('session', session.session_id);
      window.history.pushState({}, '', url);
      
      console.log('Created session:', session.session_id);
    } catch (err) {
      setError('Failed to create session');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Copy session link to clipboard
  const handleCopyLink = () => {
    const link = `${window.location.origin}${window.location.pathname}?session=${sessionId}`;
    navigator.clipboard.writeText(link).then(() => {
      alert('Session link copied to clipboard!');
    });
  };

  // Render loading or error state
  if (!sessionId) {
    return (
      <div className="welcome-screen">
        <div className="welcome-content">
          <h1>🚀 Collaborative Coding Interview Platform</h1>
          <p>Create a session and share the link with others to collaborate in real-time</p>
          
          {error && <div className="error-message">{error}</div>}
          
          <button 
            onClick={handleCreateSession} 
            disabled={loading}
            className="create-button"
          >
            {loading ? 'Creating...' : 'Create New Session'}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Collaborative Coding Interview</h1>
        <div className="header-actions">
          <button onClick={handleCopyLink} className="copy-button">
            📋 Copy Session Link
          </button>
        </div>
      </header>

      <ConnectionStatus 
        connectionState={connectionState} 
        userCount={userCount} 
      />

      <main className="app-main">
        <div className="editor-container">
          <CodeEditor 
            code={code} 
            onChange={handleCodeChange} 
            readOnly={false}
          />
        </div>
        <div className="output-container">
          <OutputPanel code={code} />
        </div>
      </main>
    </div>
  );
}

export default App;
