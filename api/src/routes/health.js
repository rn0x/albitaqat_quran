import { Hono } from "hono";
import { getData } from "../lib/data.js";

const health = new Hono();
const startTime = Date.now();

health.get("/", (c) => {
  const healthCheck = {
    status: "healthy",
    timestamp: new Date().toISOString(),
    uptime: Math.floor((Date.now() - startTime) / 1000),
    version: "1.0.0",
    local_storage: process.env.LOCAL_STORAGE_ENABLED === "true",
  };

  return c.json({
    success: true,
    data: healthCheck,
  });
});

health.get("/ready", (c) => {
  try {
    const data = getData();
    const surahs = data.getAllSurahs();

    if (surahs.length === 0) {
      return c.json(
        {
          success: false,
          error: "Data not loaded",
        },
        503
      );
    }

    return c.json({
      success: true,
      data: {
        ready: true,
        surahsLoaded: surahs.length,
      },
    });
  } catch {
    return c.json(
      {
        success: false,
        error: "Service not ready",
      },
      503
    );
  }
});

export default health;
