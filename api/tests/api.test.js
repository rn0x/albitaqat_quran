import { describe, it, before, after } from "node:test";
import assert from "node:assert";
import { createApp } from "../src/app.js";

// Test environment
const testEnv = {
  PORT: 3001,
  NODE_ENV: "test",
  CORS_ORIGINS: ["http://localhost:3000"],
  RATE_LIMIT_MAX: 100,
  RATE_LIMIT_WINDOW: 60,
  LOCAL_STORAGE_ENABLED: false,
  LOCAL_STORAGE_PATH: "./data/local",
  AUTO_DOWNLOAD_ON_START: false,
  LOG_LEVEL: "silent",
};

let app;

before(() => {
  app = createApp(testEnv);
});

describe("Health Routes", () => {
  it("GET /api/health should return healthy status", async () => {
    const res = await app.request("/api/health");
    const data = await res.json();

    assert.strictEqual(res.status, 200);
    assert.strictEqual(data.success, true);
    assert.strictEqual(data.data.status, "healthy");
    assert.ok(data.data.version);
    assert.ok(data.data.uptime >= 0);
  });

  it("GET /api/health/ready should return ready status", async () => {
    const res = await app.request("/api/health/ready");
    const data = await res.json();

    assert.strictEqual(res.status, 200);
    assert.strictEqual(data.success, true);
    assert.strictEqual(data.data.ready, true);
    assert.ok(data.data.surahsLoaded > 0);
  });
});

describe("Surahs Routes", () => {
  it("GET /api/surahs should return all 114 surahs", async () => {
    const res = await app.request("/api/surahs");
    const data = await res.json();

    assert.strictEqual(res.status, 200);
    assert.strictEqual(data.success, true);
    assert.strictEqual(data.total, 114);
    assert.ok(Array.isArray(data.data));
  });

  it("GET /api/surahs/1 should return Al-Fatihah", async () => {
    const res = await app.request("/api/surahs/1");
    const data = await res.json();

    assert.strictEqual(res.status, 200);
    assert.strictEqual(data.success, true);
    assert.strictEqual(data.data.number, 1);
    assert.strictEqual(data.data.name_arabic, "الفاتحة");
  });

  it("GET /api/surahs/999 should return 400 (out of range)", async () => {
    const res = await app.request("/api/surahs/999");
    const data = await res.json();

    assert.strictEqual(res.status, 400);
    assert.strictEqual(data.success, false);
  });

  it("GET /api/surahs/abc should return 400", async () => {
    const res = await app.request("/api/surahs/abc");
    const data = await res.json();

    assert.strictEqual(res.status, 400);
    assert.strictEqual(data.success, false);
  });

  it("GET /api/surahs/slug/al-fatihah should return Al-Fatihah", async () => {
    const res = await app.request("/api/surahs/slug/al-fatihah");
    const data = await res.json();

    assert.strictEqual(res.status, 200);
    assert.strictEqual(data.data.number, 1);
  });

  it("GET /api/surahs/search?q=بقرة should return Al-Baqarah", async () => {
    const res = await app.request("/api/surahs/search?q=بقرة");
    const data = await res.json();

    assert.strictEqual(res.status, 200);
    assert.ok(data.data.length > 0);
    assert.strictEqual(data.data[0].name_arabic, "البقرة");
  });

  it("GET /api/surahs/type/مكية should return Meccan surahs", async () => {
    const res = await app.request("/api/surahs/type/مكية");
    const data = await res.json();

    assert.strictEqual(res.status, 200);
    assert.ok(data.data.length > 0);
    data.data.forEach((s) => {
      assert.strictEqual(s.revelation_type, "مكية");
    });
  });
});

describe("Audio Routes", () => {
  it("GET /api/audio should return all audio links", async () => {
    const res = await app.request("/api/audio");
    const data = await res.json();

    assert.strictEqual(res.status, 200);
    assert.strictEqual(data.total, 114);
  });

  it("GET /api/audio/1 should return audio for Al-Fatihah", async () => {
    const res = await app.request("/api/audio/1");
    const data = await res.json();

    assert.strictEqual(res.status, 200);
    assert.strictEqual(data.data.surah_number, 1);
    assert.ok(data.data.url.includes("Al-Fatihah"));
  });
});

describe("PDF Routes", () => {
  it("GET /api/pdf should return all PDF links", async () => {
    const res = await app.request("/api/pdf");
    const data = await res.json();

    assert.strictEqual(res.status, 200);
    assert.strictEqual(data.total, 114);
  });

  it("GET /api/pdf/1 should return PDF for Al-Fatihah", async () => {
    const res = await app.request("/api/pdf/1");
    const data = await res.json();

    assert.strictEqual(res.status, 200);
    assert.strictEqual(data.data.surah_number, 1);
    assert.ok(data.data.url.includes("AlBitaqat-Book-ar_001"));
  });
});

describe("YouTube Routes", () => {
  it("GET /api/youtube should return all YouTube videos", async () => {
    const res = await app.request("/api/youtube");
    const data = await res.json();

    assert.strictEqual(res.status, 200);
    assert.ok(data.total > 0);
  });

  it("GET /api/youtube/1 should return videos for Al-Fatihah", async () => {
    const res = await app.request("/api/youtube/1");
    const data = await res.json();

    assert.strictEqual(res.status, 200);
    assert.ok(data.data.length > 0);
    assert.ok(data.data[0].video_id);
  });
});

describe("Stats Routes", () => {
  it("GET /api/stats should return project statistics", async () => {
    const res = await app.request("/api/stats");
    const data = await res.json();

    assert.strictEqual(res.status, 200);
    assert.strictEqual(data.data.total_surahs, 114);
    assert.ok(data.data.meccan_surahs > 0);
    assert.ok(data.data.medinan_surahs > 0);
    assert.ok(data.data.total_ayahs > 0);
  });
});

describe("Root Route", () => {
  it("GET / should return API info", async () => {
    const res = await app.request("/");
    const data = await res.json();

    assert.strictEqual(res.status, 200);
    assert.strictEqual(data.name, "Al-Bitaqat Quran API");
    assert.ok(data.endpoints);
  });
});

describe("404 Handler", () => {
  it("GET /nonexistent should return 404", async () => {
    const res = await app.request("/nonexistent");
    const data = await res.json();

    assert.strictEqual(res.status, 404);
    assert.strictEqual(data.success, false);
  });
});
