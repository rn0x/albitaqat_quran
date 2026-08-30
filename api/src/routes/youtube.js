import { Hono } from "hono";
import { getData } from "../lib/data.js";
import { getCache } from "../lib/cache.js";

const youtube = new Hono();

// GET /api/youtube - Get all YouTube videos
youtube.get("/", (c) => {
  const cache = getCache();
  const cached = cache.get("youtube:all");
  if (cached) return c.json(cached);

  const data = getData();
  const videos = data.getYoutubeVideos();

  const response = {
    success: true,
    data: videos,
    total: videos.length,
  };

  cache.set("youtube:all", response, 600);
  return c.json(response);
});

// GET /api/youtube/:number - Get YouTube videos for specific surah
youtube.get("/:number", (c) => {
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
  const videos = data.getYoutubeByNumber(number);

  return c.json({
    success: true,
    data: videos,
    total: videos.length,
  });
});

export default youtube;
