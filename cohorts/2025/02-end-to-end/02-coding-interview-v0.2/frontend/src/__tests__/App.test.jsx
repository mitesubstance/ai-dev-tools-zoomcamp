/**
 * Frontend tests for App component (REQ-001)
 * Tests verify session management UI and basic functionality
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import App from '../App'
import * as api from '../services/api'

// Mock the API service
vi.mock('../services/api', () => ({
  createSession: vi.fn(),
  getSession: vi.fn(),
}))

// Mock the useWebSocket hook
vi.mock('../hooks/useWebSocket', () => ({
  useWebSocket: vi.fn(() => ({
    connectionState: 'disconnected',
    userCount: 0,
    sendMessage: vi.fn(),
  })),
}))

// Mock the CodeEditor component
vi.mock('../components/CodeEditor', () => ({
  CodeEditor: ({ code, onChange }) => (
    <div data-testid="code-editor">
      <textarea
        value={code}
        onChange={(e) => onChange(e.target.value)}
        data-testid="code-textarea"
      />
    </div>
  ),
}))

// Mock the ConnectionStatus component
vi.mock('../components/ConnectionStatus', () => ({
  ConnectionStatus: ({ connectionState, userCount }) => (
    <div data-testid="connection-status">
      {connectionState} - {userCount} users
    </div>
  ),
}))

describe('App Component - Welcome Screen (No Session)', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    // Reset window.location
    delete window.location
    window.location = { origin: 'http://localhost:5173', pathname: '/', search: '' }
  })

  it('renders welcome screen when no session exists', () => {
    render(<App />)
    
    expect(screen.getByText(/Collaborative Coding Interview Platform/i)).toBeInTheDocument()
    expect(screen.getByText(/Create a session and share the link/i)).toBeInTheDocument()
  })

  it('renders Create New Session button', () => {
    render(<App />)
    
    const button = screen.getByRole('button', { name: /Create New Session/i })
    expect(button).toBeInTheDocument()
    expect(button).not.toBeDisabled()
  })

  it('clicking create button calls API and displays session', async () => {
    const mockSession = {
      session_id: '123e4567-e89b-12d3-a456-426614174000',
      language: 'python',
      created_at: '2025-12-09T05:00:00Z',
      active_users: 0,
    }
    
    api.createSession.mockResolvedValue(mockSession)
    
    render(<App />)
    
    const button = screen.getByRole('button', { name: /Create New Session/i })
    fireEvent.click(button)
    
    // Wait for API call
    await waitFor(() => {
      expect(api.createSession).toHaveBeenCalledWith('python')
    })
    
    // After session creation, the main app should render
    await waitFor(() => {
      expect(screen.getByText(/Collaborative Coding Interview/i)).toBeInTheDocument()
    })
  })

  it('displays loading state while creating session', async () => {
    api.createSession.mockImplementation(() => new Promise(() => {})) // Never resolves
    
    render(<App />)
    
    const button = screen.getByRole('button', { name: /Create New Session/i })
    fireEvent.click(button)
    
    // Should show loading text
    await waitFor(() => {
      expect(screen.getByRole('button', { name: /Creating.../i })).toBeInTheDocument()
    })
  })

  it('displays error message when session creation fails', async () => {
    api.createSession.mockRejectedValue(new Error('Network error'))
    
    render(<App />)
    
    const button = screen.getByRole('button', { name: /Create New Session/i })
    fireEvent.click(button)
    
    // Wait for error to display
    await waitFor(() => {
      expect(screen.getByText(/Failed to create session/i)).toBeInTheDocument()
    })
  })
})

describe('App Component - Main Application (With Session)', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    // Setup location with session parameter
    delete window.location
    window.location = {
      origin: 'http://localhost:5173',
      pathname: '/',
      search: '?session=123e4567-e89b-12d3-a456-426614174000',
    }
  })

  it('loads session from URL parameter on mount', async () => {
    const mockSession = {
      session_id: '123e4567-e89b-12d3-a456-426614174000',
      language: 'python',
      created_at: '2025-12-09T05:00:00Z',
      active_users: 0,
    }
    
    api.getSession.mockResolvedValue(mockSession)
    
    render(<App />)
    
    // Should call getSession with the ID from URL
    await waitFor(() => {
      expect(api.getSession).toHaveBeenCalledWith('123e4567-e89b-12d3-a456-426614174000')
    })
    
    // Should render the main app
    expect(screen.getByText(/Collaborative Coding Interview/i)).toBeInTheDocument()
  })

  it('renders Copy Session Link button', () => {
    render(<App />)
    
    const copyButton = screen.getByRole('button', { name: /Copy Session Link/i })
    expect(copyButton).toBeInTheDocument()
  })

  it('renders code editor', () => {
    render(<App />)
    
    const editor = screen.getByTestId('code-editor')
    expect(editor).toBeInTheDocument()
  })

  it('renders connection status indicator', () => {
    render(<App />)
    
    const status = screen.getByTestId('connection-status')
    expect(status).toBeInTheDocument()
  })

  it('copies session link to clipboard when copy button is clicked', async () => {
    // Mock clipboard API
    const mockWriteText = vi.fn().mockResolvedValue()
    Object.assign(navigator, {
      clipboard: {
        writeText: mockWriteText,
      },
    })
    
    // Mock alert
    window.alert = vi.fn()
    
    render(<App />)
    
    const copyButton = screen.getByRole('button', { name: /Copy Session Link/i })
    fireEvent.click(copyButton)
    
    await waitFor(() => {
      expect(mockWriteText).toHaveBeenCalledWith(
        'http://localhost:5173/?session=123e4567-e89b-12d3-a456-426614174000'
      )
      expect(window.alert).toHaveBeenCalledWith('Session link copied to clipboard!')
    })
  })

  it('displays error when session fails to load', async () => {
    api.getSession.mockRejectedValue(new Error('Session not found'))
    
    render(<App />)
    
    // Wait for error handling
    await waitFor(() => {
      expect(api.getSession).toHaveBeenCalled()
    })
    
    // The app should still render (error is logged but not blocking)
    expect(screen.getByText(/Collaborative Coding Interview/i)).toBeInTheDocument()
  })
})

describe('App Component - Code Editing', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    delete window.location
    window.location = {
      origin: 'http://localhost:5173',
      pathname: '/',
      search: '?session=123e4567-e89b-12d3-a456-426614174000',
    }
  })

  it('initializes with default Python comment', () => {
    render(<App />)
    
    const textarea = screen.getByTestId('code-textarea')
    expect(textarea.value).toContain('# Write your Python code here')
  })

  it('updates code when user types in editor', () => {
    render(<App />)
    
    const textarea = screen.getByTestId('code-textarea')
    fireEvent.change(textarea, { target: { value: 'print("Hello, World!")' } })
    
    expect(textarea.value).toBe('print("Hello, World!")')
  })
})
