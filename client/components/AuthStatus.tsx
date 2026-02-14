import React from 'react';

interface AuthStatusProps {
  isAuthenticated: boolean;
  isLoading: boolean;
  onLogin: () => void;
}

export const AuthStatus: React.FC<AuthStatusProps> = ({ isAuthenticated, isLoading, onLogin }) => {
  return (
    <div className="auth-status">
      {isAuthenticated ? (
        <div className="status-indicator authenticated">
          <span className="status-icon">✓</span>
          <span>Authenticated</span>
        </div>
      ) : (
        <div className="auth-prompt">
          <p>Please authenticate to access Teams call records</p>
          <button 
            onClick={onLogin}
            disabled={isLoading}
            className="btn-primary"
          >
            {isLoading ? 'Authenticating...' : 'Login with Azure AD'}
          </button>
        </div>
      )}
    </div>
  );
};
