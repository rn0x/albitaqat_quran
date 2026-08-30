import { getLogger } from "../lib/logger.js";

const rateLimitStore = new Map();

export function rateLimiter(maxRequests = 100, windowSeconds = 60) {
  return async (c, next) => {
    const ip = c.req.header("x-forwarded-for") || c.req.header("x-real-ip") || "unknown";
    const now = Date.now();
    const windowMs = windowSeconds * 1000;

    const entry = rateLimitStore.get(ip);

    if (!entry || now > entry.resetTime) {
      rateLimitStore.set(ip, {
        count: 1,
        resetTime: now + windowMs,
      });
      return next();
    }

    if (entry.count >= maxRequests) {
      const logger = getLogger();
      logger.warn({ ip }, "Rate limit exceeded");

      return c.json(
        {
          success: false,
          error: "Too many requests",
          retryAfter: Math.ceil((entry.resetTime - now) / 1000),
        },
        429
      );
    }

    entry.count++;
    return next();
  };
}

// Cleanup expired entries every 5 minutes
setInterval(() => {
  const now = Date.now();
  for (const [key, entry] of rateLimitStore) {
    if (now > entry.resetTime) {
      rateLimitStore.delete(key);
    }
  }
}, 5 * 60 * 1000);
