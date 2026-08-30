import { serve } from "@hono/node-server";
import { createApp } from "./app.js";
import { getLogger } from "./lib/logger.js";

// Load environment
const env = {
  PORT: parseInt(process.env.PORT || "3000"),
  NODE_ENV: process.env.NODE_ENV || "development",
  CORS_ORIGINS: (process.env.CORS_ORIGINS || "http://localhost:3000").split(",").map((s) => s.trim()),
  RATE_LIMIT_MAX: parseInt(process.env.RATE_LIMIT_MAX || "100"),
  RATE_LIMIT_WINDOW: parseInt(process.env.RATE_LIMIT_WINDOW || "60"),
  LOCAL_STORAGE_ENABLED: process.env.LOCAL_STORAGE_ENABLED !== "false",
  LOCAL_STORAGE_PATH: process.env.LOCAL_STORAGE_PATH || "./data/local",
  AUTO_DOWNLOAD_ON_START: process.env.AUTO_DOWNLOAD_ON_START !== "false",
  LOG_LEVEL: process.env.LOG_LEVEL || "info",
};

const logger = getLogger(env.LOG_LEVEL);

// Create app
const app = createApp(env);

// Start server
logger.info(`🚀 Starting server on port ${env.PORT}...`);

serve(
  {
    fetch: app.fetch,
    port: env.PORT,
  },
  (info) => {
    logger.info(`✅ Server running at http://localhost:${info.port}`);
    logger.info(`📝 Environment: ${env.NODE_ENV}`);
    logger.info(`🔗 API: http://localhost:${info.port}/api`);
    if (env.LOCAL_STORAGE_ENABLED) {
      logger.info(`💾 Local storage: ${env.LOCAL_STORAGE_PATH}`);
    }
  }
);
