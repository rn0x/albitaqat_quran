import { Hono } from "hono";
import { getData } from "../lib/data.js";
import { getCache } from "../lib/cache.js";
import { getStorage } from "../lib/storage.js";

const surahs = new Hono();

function addLocalUrls(surah) {
  const storage = getStorage();
  const result = { ...surah };
  
  if (surah.downloads) {
    result.downloads = { ...surah.downloads };
    
    if (surah.downloads.audio && storage.isAudioDownloaded(surah.number)) {
      result.downloads.audio = {
        ...surah.downloads.audio,
        local_url: `/local/audio/${surah.number}`,
      };
    }
    
    if (surah.downloads.pdf && storage.isPdfDownloaded(surah.number)) {
      result.downloads.pdf = {
        ...surah.downloads.pdf,
        local_url: `/local/pdf/${surah.number}`,
      };
    }
  }
  
  return result;
}

// GET /api/surahs - Get all surahs
surahs.get("/", (c) => {
  const cache = getCache();
  const cached = cache.get("surahs:all");
  if (cached) return c.json(cached);

  const data = getData();
  const allSurahs = data.getAllSurahs().map(addLocalUrls);

  const response = {
    success: true,
    data: allSurahs,
    total: allSurahs.length,
  };

  cache.set("surahs:all", response, 600);
  return c.json(response);
});

// GET /api/surahs/search - Search surahs
surahs.get("/search", (c) => {
  const query = c.req.query("q");
  if (!query) {
    return c.json(
      {
        success: false,
        error: "Query parameter 'q' is required",
      },
      400
    );
  }

  const data = getData();
  const results = data.searchSurahs(query).map(addLocalUrls);

  return c.json({
    success: true,
    data: results,
    total: results.length,
    query,
  });
});

// GET /api/surahs/type/:type - Get surahs by type
surahs.get("/type/:type", (c) => {
  const type = c.req.param("type");

  if (type !== "مكية" && type !== "مدنية") {
    return c.json(
      {
        success: false,
        error: "Type must be 'مكية' or 'مدنية'",
      },
      400
    );
  }

  const data = getData();
  const results = data.getSurahsByType(type).map(addLocalUrls);

  return c.json({
    success: true,
    data: results,
    total: results.length,
    type,
  });
});

// GET /api/surahs/:number - Get surah by number
surahs.get("/:number", (c) => {
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
  const surah = data.getSurahByNumber(number);

  if (!surah) {
    return c.json(
      {
        success: false,
        error: `Surah ${number} not found`,
      },
      404
    );
  }

  return c.json({
    success: true,
    data: addLocalUrls(surah),
  });
});

// GET /api/surahs/slug/:slug - Get surah by slug
surahs.get("/slug/:slug", (c) => {
  const slug = c.req.param("slug");

  const data = getData();
  const surah = data.getSurahBySlug(slug);

  if (!surah) {
    return c.json(
      {
        success: false,
        error: `Surah with slug '${slug}' not found`,
      },
      404
    );
  }

  return c.json({
    success: true,
    data: addLocalUrls(surah),
  });
});

export default surahs;
