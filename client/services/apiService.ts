import type { CallRecord, CallRecordsResponse } from '../types/callRecord';

const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:3001/api';

class ApiService {
  async getAccessToken(): Promise<string> {
    const response = await fetch(`${API_BASE_URL}/auth/token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Failed to get access token');
    }

    const data = await response.json();
    return data.accessToken;
  }

  async getCallRecords(accessToken: string): Promise<CallRecord[]> {
    const response = await fetch(`${API_BASE_URL}/graph/callrecords`, {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch call records');
    }

    const data: CallRecordsResponse = await response.json();
    return data.callRecords;
  }

  async getCallRecordById(accessToken: string, id: string): Promise<CallRecord> {
    const response = await fetch(`${API_BASE_URL}/graph/callrecords/${id}`, {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch call record');
    }

    return response.json();
  }
}

export const apiService = new ApiService();
