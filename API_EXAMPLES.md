# API Usage Examples

This document provides practical examples of using the Teams CDR Template API.

## Authentication

### Get Access Token

```bash
curl -X POST http://localhost:3001/api/auth/token \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6...",
  "expiresOn": "2024-02-14T23:00:00.000Z"
}
```

### Using the Access Token

Save the token for subsequent requests:
```bash
export ACCESS_TOKEN="your-access-token-here"
```

## Fetch Call Records

### Get All Call Records (Paginated)

```bash
curl -X GET http://localhost:3001/api/graph/callrecords \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "callRecords": [
    {
      "id": "00000000-0000-0000-0000-000000000000",
      "version": 1,
      "type": "groupCall",
      "modalities": ["audio", "video"],
      "lastModifiedDateTime": "2024-02-14T10:30:00Z",
      "startDateTime": "2024-02-14T10:00:00Z",
      "endDateTime": "2024-02-14T10:30:00Z",
      "joinWebUrl": "https://teams.microsoft.com/l/meetup-join/..."
    }
  ],
  "nextLink": "https://graph.microsoft.com/beta/communications/callRecords?$skip=50"
}
```

### Get Specific Call Record by ID

```bash
curl -X GET http://localhost:3001/api/graph/callrecords/{call-record-id} \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "id": "00000000-0000-0000-0000-000000000000",
  "version": 1,
  "type": "groupCall",
  "modalities": ["audio", "video"],
  "lastModifiedDateTime": "2024-02-14T10:30:00Z",
  "startDateTime": "2024-02-14T10:00:00Z",
  "endDateTime": "2024-02-14T10:30:00Z",
  "organizer": {
    "id": "user-id-here",
    "displayName": "John Doe",
    "userPrincipalName": "john.doe@contoso.com"
  }
}
```

### Get Call Sessions

```bash
curl -X GET http://localhost:3001/api/graph/callrecords/{call-record-id}/sessions \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "sessions": [
    {
      "id": "session-id-here",
      "caller": {
        "displayName": "John Doe",
        "userPrincipalName": "john.doe@contoso.com"
      },
      "callee": {
        "displayName": "Jane Smith",
        "userPrincipalName": "jane.smith@contoso.com"
      },
      "startDateTime": "2024-02-14T10:00:00Z",
      "endDateTime": "2024-02-14T10:30:00Z",
      "modalities": ["audio", "video"]
    }
  ]
}
```

## JavaScript/TypeScript Examples

### Using with Fetch API

```typescript
// Get access token
async function getAccessToken(): Promise<string> {
  const response = await fetch('http://localhost:3001/api/auth/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  
  const data = await response.json();
  return data.accessToken;
}

// Fetch call records
async function getCallRecords() {
  const token = await getAccessToken();
  
  const response = await fetch('http://localhost:3001/api/graph/callrecords', {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });
  
  const data = await response.json();
  return data.callRecords;
}

// Usage
const records = await getCallRecords();
console.log(`Found ${records.length} call records`);
```

### Using with Axios

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:3001/api',
});

// Get access token
async function authenticate() {
  const { data } = await api.post('/auth/token');
  return data.accessToken;
}

// Fetch call records with auth
async function fetchCallRecords() {
  const token = await authenticate();
  
  const { data } = await api.get('/graph/callrecords', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  
  return data.callRecords;
}
```

## Python Examples

### Using requests library

```python
import requests
import json

BASE_URL = "http://localhost:3001/api"

# Get access token
def get_access_token():
    response = requests.post(f"{BASE_URL}/auth/token")
    return response.json()["accessToken"]

# Fetch call records
def get_call_records():
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(f"{BASE_URL}/graph/callrecords", headers=headers)
    return response.json()["callRecords"]

# Usage
if __name__ == "__main__":
    records = get_call_records()
    print(f"Found {len(records)} call records")
    for record in records:
        print(f"Call ID: {record['id']}")
        print(f"Type: {record['type']}")
        print(f"Duration: {record['startDateTime']} to {record['endDateTime']}")
        print("---")
```

## PowerShell Examples

```powershell
# Get access token
$tokenResponse = Invoke-RestMethod -Method Post -Uri "http://localhost:3001/api/auth/token"
$accessToken = $tokenResponse.accessToken

# Fetch call records
$headers = @{
    "Authorization" = "Bearer $accessToken"
    "Content-Type" = "application/json"
}

$callRecords = Invoke-RestMethod -Method Get -Uri "http://localhost:3001/api/graph/callrecords" -Headers $headers

# Display results
Write-Host "Found $($callRecords.callRecords.Count) call records"
$callRecords.callRecords | ForEach-Object {
    Write-Host "Call ID: $($_.id)"
    Write-Host "Type: $($_.type)"
    Write-Host "Start: $($_.startDateTime)"
    Write-Host "End: $($_.endDateTime)"
    Write-Host "---"
}
```

## Error Handling

### Handle Authentication Errors

```typescript
async function getAccessTokenWithRetry(maxRetries = 3): Promise<string> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await fetch('http://localhost:3001/api/auth/token', {
        method: 'POST',
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      return data.accessToken;
    } catch (error) {
      console.error(`Attempt ${i + 1} failed:`, error);
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
    }
  }
  throw new Error('Max retries exceeded');
}
```

### Handle API Errors

```typescript
async function getCallRecordsSafe() {
  try {
    const token = await getAccessToken();
    const response = await fetch('http://localhost:3001/api/graph/callrecords', {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    
    if (response.status === 401) {
      throw new Error('Unauthorized: Check your credentials');
    }
    
    if (response.status === 403) {
      throw new Error('Forbidden: Check API permissions');
    }
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }
    
    const data = await response.json();
    return data.callRecords;
  } catch (error) {
    console.error('Error fetching call records:', error);
    return [];
  }
}
```

## Rate Limiting

The Microsoft Graph API has rate limits. Here's how to handle them:

```typescript
async function fetchWithRateLimit(url: string, options: RequestInit) {
  const response = await fetch(url, options);
  
  if (response.status === 429) {
    const retryAfter = response.headers.get('Retry-After');
    const waitTime = retryAfter ? parseInt(retryAfter) * 1000 : 60000;
    
    console.log(`Rate limited. Waiting ${waitTime}ms...`);
    await new Promise(resolve => setTimeout(resolve, waitTime));
    
    return fetchWithRateLimit(url, options);
  }
  
  return response;
}
```

## Pagination

Handle paginated results:

```typescript
async function getAllCallRecords() {
  const token = await getAccessToken();
  let allRecords: any[] = [];
  let nextLink: string | null = '/api/graph/callrecords';
  
  while (nextLink) {
    const response = await fetch(`http://localhost:3001${nextLink}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    
    const data = await response.json();
    allRecords = allRecords.concat(data.callRecords);
    nextLink = data.nextLink ? new URL(data.nextLink).pathname : null;
  }
  
  return allRecords;
}
```

## Testing with Postman

1. Create a new POST request to `http://localhost:3001/api/auth/token`
2. Send request and copy the `accessToken` from response
3. Create a new GET request to `http://localhost:3001/api/graph/callrecords`
4. Add header: `Authorization: Bearer {your-token}`
5. Send request to see call records

## Additional Resources

- [Microsoft Graph REST API Reference](https://docs.microsoft.com/en-us/graph/api/overview)
- [Call Records API Overview](https://docs.microsoft.com/en-us/graph/api/resources/callrecords-api-overview)
- [TypeScript Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
