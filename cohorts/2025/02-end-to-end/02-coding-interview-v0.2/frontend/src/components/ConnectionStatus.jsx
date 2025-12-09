/**
 * ConnectionStatus component
 * Displays WebSocket connection status and active user count
 */
import { ConnectionState } from '../hooks/useWebSocket';

/**
 * ConnectionStatus component
 * @param {Object} props
 * @param {string} props.connectionState - Current connection state
 * @param {number} props.userCount - Number of active users
 */
export function ConnectionStatus({ connectionState, userCount }) {
  const getStatusColor = () => {
    switch (connectionState) {
      case ConnectionState.CONNECTED:
        return '#4CAF50';
      case ConnectionState.CONNECTING:
        return '#FFA726';
      case ConnectionState.ERROR:
        return '#F44336';
      case ConnectionState.DISCONNECTED:
      default:
        return '#9E9E9E';
    }
  };

  const getStatusText = () => {
    switch (connectionState) {
      case ConnectionState.CONNECTED:
        return 'Connected';
      case ConnectionState.CONNECTING:
        return 'Connecting...';
      case ConnectionState.ERROR:
        return 'Connection Error';
      case ConnectionState.DISCONNECTED:
      default:
        return 'Disconnected';
    }
  };

  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: '16px',
        padding: '8px 16px',
        backgroundColor: '#1e1e1e',
        color: '#fff',
        fontSize: '14px',
        borderBottom: '1px solid #333',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <div
          style={{
            width: '8px',
            height: '8px',
            borderRadius: '50%',
            backgroundColor: getStatusColor(),
          }}
        />
        <span>{getStatusText()}</span>
      </div>
      
      {connectionState === ConnectionState.CONNECTED && (
        <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
          <span>👥</span>
          <span>{userCount} {userCount === 1 ? 'user' : 'users'} online</span>
        </div>
      )}
    </div>
  );
}
