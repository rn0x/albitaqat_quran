import { Hono } from "hono";
import { corsMiddleware } from "./middleware/cors.js";
import { securityHeaders } from "./middleware/security.js";
import { rateLimiter } from "./middleware/rateLimiter.js";
import { errorHandler } from "./middleware/errorHandler.js";
import { getData } from "./lib/data.js";
import { getStorage } from "./lib/storage.js";
import { getLogger } from "./lib/logger.js";

import healthRoutes from "./routes/health.js";
import surahsRoutes from "./routes/surahs.js";
import audioRoutes from "./routes/audio.js";
import pdfRoutes from "./routes/pdf.js";
import youtubeRoutes from "./routes/youtube.js";
import statsRoutes from "./routes/stats.js";
import localRoutes from "./routes/local.js";

export function createApp(env) {
  const app = new Hono();
  const logger = getLogger(env.LOG_LEVEL);

  // Load data
  logger.info("📦 Loading data...");
  const data = getData("../data");
  logger.info(`✅ Loaded ${data.getAllSurahs().length} surahs`);

  // Auto download on start
  if (env.AUTO_DOWNLOAD_ON_START && env.LOCAL_STORAGE_ENABLED) {
    const storage = getStorage(env.LOCAL_STORAGE_PATH, logger);
    
    // Check if already downloaded
    const status = storage.getLocalStatus();
    if (status.audio < status.total || status.pdf < status.total) {
      logger.info(`📥 Auto-downloading audio and PDF... (${status.audio}/${status.total} audio, ${status.pdf}/${status.total} pdf)`);
      storage.downloadAll().then((result) => {
        logger.info(`✅ Auto-download complete!`);
      }).catch((err) => {
        logger.error({ err }, "Failed to download files");
      });
    } else {
      logger.info(`✅ Local storage ready: ${status.audio} audio, ${status.pdf} pdf`);
    }
  }

  // Global middleware
  app.use("*", errorHandler());
  app.use("*", corsMiddleware(env));
  app.use("*", securityHeaders());
  app.use("*", rateLimiter(env.RATE_LIMIT_MAX, env.RATE_LIMIT_WINDOW));

  // API routes
  app.route("/api/health", healthRoutes);
  app.route("/api/surahs", surahsRoutes);
  app.route("/api/audio", audioRoutes);
  app.route("/api/pdf", pdfRoutes);
  app.route("/api/youtube", youtubeRoutes);
  app.route("/api/stats", statsRoutes);

  // Local storage routes
  if (env.LOCAL_STORAGE_ENABLED) {
    app.route("/local", localRoutes);
  }

  // Root route
  app.get("/", (c) => {
    return c.json({
      name: "Al-Bitaqat Quran API",
      version: "1.0.0",
      description: "API for Quran Cards data",
      endpoints: {
        health: "/api/health",
        surahs: "/api/surahs",
        audio: "/api/audio",
        pdf: "/api/pdf",
        youtube: "/api/youtube",
        stats: "/api/stats",
        local: env.LOCAL_STORAGE_ENABLED ? "/local" : undefined,
      },
    });
  });

  // 404 handler
  app.notFound((c) => {
    return c.json(
      {
        success: false,
        error: "Route not found",
      },
      404
    );
  });

  return app;
}
