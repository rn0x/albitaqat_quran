import { getLogger } from "../lib/logger.js";

export function errorHandler() {
  return async (c, next) => {
    try {
      await next();
    } catch (err) {
      const logger = getLogger();
      const error = err;

      logger.error({
        err: error.message,
        stack: error.stack,
        path: c.req.path,
        method: c.req.method,
      });

      // Not found
      if (error.message.includes("not found") || error.message.includes("غير موجود")) {
        return c.json(
          {
            success: false,
            error: error.message,
          },
          404
        );
      }

      // Internal error
      return c.json(
        {
          success: false,
          error:
            process.env.NODE_ENV === "production"
              ? "Internal server error"
              : error.message,
        },
        500
      );
    }
  };
}
