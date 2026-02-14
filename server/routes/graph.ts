import { Router, Request, Response } from 'express';
import { Client } from '@microsoft/microsoft-graph-client';
import 'isomorphic-fetch';

const router = Router();

// Middleware to create Graph client with token from request
const getGraphClient = (accessToken: string) => {
  return Client.init({
    authProvider: (done) => {
      done(null, accessToken);
    },
  });
};

// Get call records from Microsoft Graph
router.get('/callrecords', async (req: Request, res: Response): Promise<void> => {
  try {
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      res.status(401).json({ error: 'Missing or invalid authorization header' });
      return;
    }

    const accessToken = authHeader.substring(7);
    const client = getGraphClient(accessToken);

    // Fetch call records
    // Note: This requires CallRecords.Read.All permission
    const response = await client
      .api('/communications/callRecords')
      .version('beta') // Call Records API is in beta
      .top(50) // Limit to 50 records
      .get();

    res.json({
      callRecords: response.value || [],
      nextLink: response['@odata.nextLink'] || null,
    });
  } catch (error) {
    console.error('Error fetching call records:', error);
    res.status(500).json({
      error: 'Failed to fetch call records',
      message: error instanceof Error ? error.message : 'Unknown error',
    });
  }
});

// Get specific call record by ID
router.get('/callrecords/:id', async (req: Request, res: Response): Promise<void> => {
  try {
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      res.status(401).json({ error: 'Missing or invalid authorization header' });
      return;
    }

    const accessToken = authHeader.substring(7);
    const client = getGraphClient(accessToken);
    const { id } = req.params;

    const callRecord = await client
      .api(`/communications/callRecords/${id}`)
      .version('beta')
      .get();

    res.json(callRecord);
  } catch (error) {
    console.error('Error fetching call record:', error);
    res.status(500).json({
      error: 'Failed to fetch call record',
      message: error instanceof Error ? error.message : 'Unknown error',
    });
  }
});

// Get call sessions for a specific call record
router.get('/callrecords/:id/sessions', async (req: Request, res: Response): Promise<void> => {
  try {
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      res.status(401).json({ error: 'Missing or invalid authorization header' });
      return;
    }

    const accessToken = authHeader.substring(7);
    const client = getGraphClient(accessToken);
    const { id } = req.params;

    const sessions = await client
      .api(`/communications/callRecords/${id}/sessions`)
      .version('beta')
      .get();

    res.json({
      sessions: sessions.value || [],
    });
  } catch (error) {
    console.error('Error fetching call sessions:', error);
    res.status(500).json({
      error: 'Failed to fetch call sessions',
      message: error instanceof Error ? error.message : 'Unknown error',
    });
  }
});

export { router as graphRouter };
