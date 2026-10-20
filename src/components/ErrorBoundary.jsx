import React from 'react';

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('AutoAR Caught Boundary Error:', error, errorInfo);
    this.setState({ errorInfo });
  }

  handleReload = () => {
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          minHeight: '100vh',
          backgroundColor: '#080c14',
          color: '#f8fafc',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '24px',
          fontFamily: 'Inter, system-ui, sans-serif',
          textAlign: 'center'
        }}>
          <div style={{
            background: 'rgba(15, 23, 42, 0.85)',
            border: '1px solid rgba(0, 212, 255, 0.3)',
            borderRadius: '16px',
            padding: '36px',
            maxWidth: '560px',
            boxShadow: '0 20px 50px rgba(0, 0, 0, 0.8), 0 0 30px rgba(0, 212, 255, 0.15)',
            backdropFilter: 'blur(12px)'
          }}>
            <div style={{ fontSize: '3.5rem', marginBottom: '16px' }}>🏎️</div>
            <h1 style={{
              fontSize: '1.5rem',
              fontWeight: 800,
              letterSpacing: '0.05em',
              background: 'linear-gradient(135deg, #00d4ff, #38bdf8)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              margin: '0 0 12px 0'
            }}>
              AutoAR Digital Twin Workstation
            </h1>
            <p style={{ color: '#94a3b8', fontSize: '0.95rem', lineHeight: 1.6, margin: '0 0 20px 0' }}>
              The 3D graphics hardware accelerator encountered a transient reset. Click below to recover the session instantly.
            </p>
            {this.state.error && (
              <div style={{
                background: 'rgba(0, 0, 0, 0.5)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '8px',
                padding: '12px',
                fontSize: '0.8rem',
                color: '#f87171',
                fontFamily: 'monospace',
                textAlign: 'left',
                overflowX: 'auto',
                marginBottom: '24px',
                maxHeight: '120px'
              }}>
                {this.state.error.toString()}
              </div>
            )}
            <button
              onClick={this.handleReload}
              style={{
                background: 'linear-gradient(135deg, #00d4ff, #0077ff)',
                color: '#030712',
                border: 'none',
                padding: '12px 28px',
                borderRadius: '10px',
                fontWeight: 800,
                fontSize: '0.95rem',
                cursor: 'pointer',
                letterSpacing: '0.05em',
                boxShadow: '0 0 25px rgba(0, 212, 255, 0.45)',
                transition: 'transform 0.2s, box-shadow 0.2s'
              }}
            >
              ⚡ RESTART WORKSTATION
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}
