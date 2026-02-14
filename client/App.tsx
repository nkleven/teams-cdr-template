import React, { useState } from 'react';
import { CallRecordsList } from './components/CallRecordsList';
import { AuthStatus } from './components/AuthStatus';
import { apiService } from './services/apiService';
import type { CallRecord } from './types/callRecord';

const App: React.FC = () => {
  const [callRecords, setCallRecords] = useState<CallRecord[]>([]);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);

  const handleLogin = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const token = await apiService.getAccessToken();
      setAccessToken(token);
      setIsAuthenticated(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Authentication failed');
      setIsAuthenticated(false);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchCallRecords = async () => {
    if (!accessToken) {
      setError('Please authenticate first');
      return;
    }

    try {
      setIsLoading(true);
      setError(null);
      const records = await apiService.getCallRecords(accessToken);
      setCallRecords(records);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch call records');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Teams Call Detail Records (CDR)</h1>
        <p className="subtitle">View and analyze Microsoft Teams call history</p>
      </header>

      <main className="app-main">
        <AuthStatus 
          isAuthenticated={isAuthenticated}
          isLoading={isLoading}
          onLogin={handleLogin}
        />

        {error && (
          <div className="error-message">
            <strong>Error:</strong> {error}
          </div>
        )}

        {isAuthenticated && (
          <div className="actions">
            <button 
              onClick={fetchCallRecords}
              disabled={isLoading}
              className="btn-primary"
            >
              {isLoading ? 'Loading...' : 'Fetch Call Records'}
            </button>
          </div>
        )}

        {callRecords.length > 0 && (
          <CallRecordsList records={callRecords} />
        )}
      </main>

      <footer className="app-footer">
        <p>Powered by Microsoft Graph API</p>
      </footer>
    </div>
  );
};

export default App;
