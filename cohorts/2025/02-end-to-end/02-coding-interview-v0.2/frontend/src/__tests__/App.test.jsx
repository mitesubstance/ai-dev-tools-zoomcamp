/**
 * Frontend tests for App component
 * Tests verify the basic React app functionality
 */
import { describe, it, expect } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import App from '../App'

describe('App Component', () => {
  it('renders without crashing', () => {
    render(<App />)
    expect(screen.getByText(/Vite \+ React/i)).toBeInTheDocument()
  })

  it('renders the main heading', () => {
    render(<App />)
    const heading = screen.getByRole('heading', { name: /Vite \+ React/i })
    expect(heading).toBeInTheDocument()
  })

  it('renders Vite logo with correct attributes', () => {
    render(<App />)
    const viteLogo = screen.getByAltText(/Vite logo/i)
    expect(viteLogo).toBeInTheDocument()
    // Vite logo is embedded as data URI in development
    expect(viteLogo).toHaveAttribute('src')
    expect(viteLogo.getAttribute('src')).toBeTruthy()
  })

  it('renders React logo with correct attributes', () => {
    render(<App />)
    const reactLogo = screen.getByAltText(/React logo/i)
    expect(reactLogo).toBeInTheDocument()
    expect(reactLogo.src).toContain('react.svg')
  })

  it('displays initial count of 0', () => {
    render(<App />)
    const button = screen.getByRole('button', { name: /count is 0/i })
    expect(button).toBeInTheDocument()
  })

  it('increments count when button is clicked', () => {
    render(<App />)
    const button = screen.getByRole('button', { name: /count is/i })
    
    // Initial state
    expect(button).toHaveTextContent('count is 0')
    
    // Click once
    fireEvent.click(button)
    expect(button).toHaveTextContent('count is 1')
    
    // Click again
    fireEvent.click(button)
    expect(button).toHaveTextContent('count is 2')
  })

  it('increments count multiple times correctly', () => {
    render(<App />)
    const button = screen.getByRole('button', { name: /count is/i })
    
    // Click 5 times
    for (let i = 0; i < 5; i++) {
      fireEvent.click(button)
    }
    
    expect(button).toHaveTextContent('count is 5')
  })

  it('renders instruction text about HMR', () => {
    render(<App />)
    // Text is split across elements, so we use a custom text matcher
    const hmrText = screen.getByText((content, element) => {
      return element?.textContent === 'Edit src/App.jsx and save to test HMR'
    })
    expect(hmrText).toBeInTheDocument()
  })

  it('renders the read-the-docs text', () => {
    render(<App />)
    const docsText = screen.getByText(/Click on the Vite and React logos to learn more/i)
    expect(docsText).toBeInTheDocument()
  })

  it('has links that open in new tab', () => {
    render(<App />)
    const links = screen.getAllByRole('link')
    
    // Both links should have target="_blank"
    links.forEach(link => {
      expect(link).toHaveAttribute('target', '_blank')
    })
  })

  it('button has correct initial text format', () => {
    render(<App />)
    const button = screen.getByRole('button')
    
    expect(button.textContent).toMatch(/^count is \d+$/)
  })
})
