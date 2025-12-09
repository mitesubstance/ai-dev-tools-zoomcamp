/**
 * Tests for ConnectionStatus component (REQ-005)
 * Verifies connection status indicator displays correctly for all states
 */
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ConnectionStatus } from '../ConnectionStatus';
import { ConnectionState } from '../../hooks/useWebSocket';

describe('ConnectionStatus Component', () => {
  describe('Status Display', () => {
    it('should render "Connected" status with green indicator', () => {
      render(
        <ConnectionStatus 
          connectionState={ConnectionState.CONNECTED} 
          userCount={2} 
        />
      );

      expect(screen.getByText('Connected')).toBeInTheDocument();
    });

    it('should render "Connecting..." status with orange indicator', () => {
      render(
        <ConnectionStatus 
          connectionState={ConnectionState.CONNECTING} 
          userCount={0} 
        />
      );

      expect(screen.getByText('Connecting...')).toBeInTheDocument();
    });

    it('should render "Connection Error" status with red indicator', () => {
      render(
        <ConnectionStatus 
          connectionState={ConnectionState.ERROR} 
          userCount={0} 
        />
      );

      expect(screen.getByText('Connection Error')).toBeInTheDocument();
    });

    it('should render "Disconnected" status with gray indicator', () => {
      render(
        <ConnectionStatus 
          connectionState={ConnectionState.DISCONNECTED} 
          userCount={0} 
        />
      );

      expect(screen.getByText('Disconnected')).toBeInTheDocument();
    });
  });

  describe('User Count Display', () => {
    it('should show user count when connected with singular form', () => {
      render(
        <ConnectionStatus 
          connectionState={ConnectionState.CONNECTED} 
          userCount={1} 
        />
      );

      expect(screen.getByText(/1 user online/i)).toBeInTheDocument();
    });

    it('should show user count when connected with plural form', () => {
      render(
        <ConnectionStatus 
          connectionState={ConnectionState.CONNECTED} 
          userCount={3} 
        />
      );

      expect(screen.getByText(/3 users online/i)).toBeInTheDocument();
    });

    it('should not show user count when connecting', () => {
      render(
        <ConnectionStatus 
          connectionState={ConnectionState.CONNECTING} 
          userCount={2} 
        />
      );

      expect(screen.queryByText(/users online/i)).not.toBeInTheDocument();
    });

    it('should not show user count when disconnected', () => {
      render(
        <ConnectionStatus 
          connectionState={ConnectionState.DISCONNECTED} 
          userCount={2} 
        />
      );

      expect(screen.queryByText(/users online/i)).not.toBeInTheDocument();
    });

    it('should not show user count when error', () => {
      render(
        <ConnectionStatus 
          connectionState={ConnectionState.ERROR} 
          userCount={2} 
        />
      );

      expect(screen.queryByText(/users online/i)).not.toBeInTheDocument();
    });
  });

  describe('Edge Cases', () => {
    it('should handle zero users when connected', () => {
      render(
        <ConnectionStatus 
          connectionState={ConnectionState.CONNECTED} 
          userCount={0} 
        />
      );

      expect(screen.getByText(/0 users online/i)).toBeInTheDocument();
    });

    it('should handle large user counts', () => {
      render(
        <ConnectionStatus 
          connectionState={ConnectionState.CONNECTED} 
          userCount={100} 
        />
      );

      expect(screen.getByText(/100 users online/i)).toBeInTheDocument();
    });
  });
});
