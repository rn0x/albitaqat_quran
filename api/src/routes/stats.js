import { Hono } from "hono";
import { getData } from "../lib/data.js";
import { getCache } from "../lib/cache.js";

const stats = new Hono();

stats.get("/", (c) => {
  const cache = getCache();
  const cached = cache.get("stats");
  if (cached) return c.json(cached);

  const data = getData();
  const statsData = data.getStats();

  const response = {
    success: true,
    data: statsData,
  };

  cache.set("stats", response, 300);
  return c.json(response);
});

export default stats;
