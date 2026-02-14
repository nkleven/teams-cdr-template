import { Router, Request, Response } from 'express';
import { ConfidentialClientApplication } from '@azure/msal-node';

const router = Router();

// MSAL configuration
const msalConfig = {
  auth: {
    clientId: process.env.CLIENT_ID || '',
    authority: `https://login.microsoftonline.com/${process.env.TENANT_ID}`,
    clientSecret: process.env.CLIENT_SECRET || '',
  },
};

const cca = new ConfidentialClientApplication(msalConfig);

// Get access token using client credentials flow
router.post('/token', async (_req: Request, res: Response) => {
  try {
    const tokenRequest = {
      scopes: [process.env.GRAPH_SCOPES || 'https://graph.microsoft.com/.default'],
    };

    const response = await cca.acquireTokenByClientCredential(tokenRequest);

    if (response?.accessToken) {
      res.json({
        accessToken: response.accessToken,
        expiresOn: response.expiresOn,
      });
    } else {
      throw new Error('Failed to acquire access token');
    }
  } catch (error) {
    console.error('Authentication error:', error);
    res.status(500).json({
      error: 'Authentication failed',
      message: error instanceof Error ? error.message : 'Unknown error',
    });
  }
});

export { router as authRouter };
