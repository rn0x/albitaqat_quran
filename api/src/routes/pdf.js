import { Hono } from "hono";
import { getData } from "../lib/data.js";
import { getCache } from "../lib/cache.js";

const pdf = new Hono();

// GET /api/pdf - Get all PDF links
pdf.get("/", (c) => {
  const cache = getCache();
  const cached = cache.get("pdf:all");
  if (cached) return c.json(cached);

  const data = getData();
  const links = data.getPdfLinks();

  const response = {
    success: true,
    data: links,
    total: links.length,
  };

  cache.set("pdf:all", response, 600);
  return c.json(response);
});

// GET /api/pdf/:number - Get PDF for specific surah
pdf.get("/:number", (c) => {
  const number = parseInt(c.req.param("number"));

  if (isNaN(number) || number < 1 || number > 114) {
    return c.json(
      {
        success: false,
        error: "Invalid surah number. Must be between 1 and 114",
      },
      400
    );
  }

  const data = getData();
  const link = data.getPdfByNumber(number);

  if (!link) {
    return c.json(
      {
        success: false,
        error: `PDF for surah ${number} not found`,
      },
      404
    );
  }

  return c.json({
    success: true,
    data: link,
  });
});

export default pdf;
