import { cors } from "hono/cors";

export function corsMiddleware(env) {
  return cors({
    origin: env.CORS_ORIGINS,
    allowMethods: ["GET", "HEAD", "OPTIONS"],
    allowHeaders: ["Content-Type", "Authorization"],
    exposeHeaders: ["X-RateLimit-Limit", "X-RateLimit-Remaining"],
    credentials: false,
    maxAge: 86400,
  });
}
