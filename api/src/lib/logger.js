import pino from "pino";

let logger = null;

export function getLogger(level = "info") {
  if (!logger) {
    logger = pino({
      level,
      transport:
        process.env.NODE_ENV !== "production"
          ? { target: "pino-pretty", options: { colorize: true } }
          : undefined,
    });
  }
  return logger;
}

export function resetLogger() {
  logger = null;
}
