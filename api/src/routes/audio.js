import { Hono } from "hono";
import { getData } from "../lib/data.js";
import { getCache } from "../lib/cache.js";

const audio = new Hono();

// GET /api/audio - Get all audio links
audio.get("/", (c) => {
  const cache = getCache();
  const cached = cache.get("audio:all");
  if (cached) return c.json(cached);

  const data = getData();
  const links = data.getAudioLinks();

  const response = {
    success: true,
    data: links,
    total: links.length,
  };

  cache.set("audio:all", response, 600);
  return c.json(response);
});

// GET /api/audio/:number - Get audio for specific surah
audio.get("/:number", (c) => {
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
  const link = data.getAudioByNumber(number);

  if (!link) {
    return c.json(
      {
        success: false,
        error: `Audio for surah ${number} not found`,
      },
      404
    );
  }

  return c.json({
    success: true,
    data: link,
  });
});

export default audio;
