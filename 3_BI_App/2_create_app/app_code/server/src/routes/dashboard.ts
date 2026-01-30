import { Router, type Request, type Response, type Router as RouterType } from 'express';
import { authMiddleware, requireAuth } from '../middleware/auth';

export const dashboardRouter: RouterType = Router();

// Apply auth middleware
dashboardRouter.use(authMiddleware);

/**
 * GET /api/dashboard/token - Get the access token for embedding dashboards
 * This endpoint extracts the x-forwarded-access-token header and returns it to the client
 */
dashboardRouter.get('/token', requireAuth, async (req: Request, res: Response) => {
  // Get the access token from the forwarded headers
  const accessToken = req.headers['x-forwarded-access-token'] as string | undefined;

  if (!accessToken) {
    return res.status(401).json({ 
      error: 'No access token available',
      message: 'The x-forwarded-access-token header is not present in the request'
    });
  }

  res.json({ token: accessToken });
});
