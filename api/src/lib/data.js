import { readFileSync, existsSync } from "fs";
import { join } from "path";
import { fileURLToPath } from "url";
import { dirname } from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

class QuranData {
  constructor() {
    this.surahs = [];
    this.surahsFull = [];
    this.audioLinks = [];
    this.pdfLinks = [];
    this.youtubeVideos = [];
    this.loaded = false;
  }

  load(dataDir) {
    if (this.loaded) return;

    // Try multiple paths
    const possiblePaths = [
      dataDir,
      "../data",
      "./data",
      join(process.cwd(), "data"),
    ].filter(Boolean);

    let dataPath = null;
    for (const path of possiblePaths) {
      const fullPath = join(process.cwd(), path);
      if (existsSync(fullPath)) {
        dataPath = fullPath;
        break;
      }
    }

    if (!dataPath) {
      console.error("❌ Data directory not found");
      return;
    }

    // Load quran_cards_full.json
    const fullJsonPath = join(dataPath, "quran_cards_full.json");
    if (existsSync(fullJsonPath)) {
      const fullData = JSON.parse(readFileSync(fullJsonPath, "utf-8"));
      this.surahs = fullData.surahs || [];
    }

    // Load quran_cards.json (with card_data)
    const cardsJsonPath = join(dataPath, "quran_cards.json");
    if (existsSync(cardsJsonPath)) {
      const cardsData = JSON.parse(readFileSync(cardsJsonPath, "utf-8"));
      this.surahsFull = cardsData.surahs || [];
    }

    // Load audio_links.json
    const audioPath = join(dataPath, "audio_links.json");
    if (existsSync(audioPath)) {
      const audioData = JSON.parse(readFileSync(audioPath, "utf-8"));
      this.audioLinks = audioData.files || [];
    }

    // Load pdf_links.json
    const pdfPath = join(dataPath, "pdf_links.json");
    if (existsSync(pdfPath)) {
      const pdfData = JSON.parse(readFileSync(pdfPath, "utf-8"));
      this.pdfLinks = pdfData.files || [];
    }

    // Load youtube_videos.json
    const ytPath = join(dataPath, "youtube_videos.json");
    if (existsSync(ytPath)) {
      const ytData = JSON.parse(readFileSync(ytPath, "utf-8"));
      this.youtubeVideos = ytData.videos || [];
    }

    this.loaded = true;
  }

  ensureLoaded() {
    if (!this.loaded) this.load();
  }

  getAllSurahs() {
    this.ensureLoaded();
    return this.surahs;
  }

  getSurahByNumber(number) {
    this.ensureLoaded();
    return this.surahs.find((s) => s.number === number);
  }

  getSurahBySlug(slug) {
    this.ensureLoaded();
    return this.surahs.find((s) => s.slug === slug);
  }

  getSurahsByType(type) {
    this.ensureLoaded();
    return this.surahs.filter((s) => s.revelation_type === type);
  }

  searchSurahs(query) {
    this.ensureLoaded();
    const q = query.toLowerCase();
    return this.surahs.filter(
      (s) =>
        s.name_arabic.toLowerCase().includes(q) ||
        s.name_english.toLowerCase().includes(q) ||
        s.slug.toLowerCase().includes(q)
    );
  }

  getAudioLinks() {
    this.ensureLoaded();
    return this.audioLinks;
  }

  getAudioByNumber(number) {
    this.ensureLoaded();
    return this.audioLinks.find((a) => a.surah_number === number);
  }

  getPdfLinks() {
    this.ensureLoaded();
    return this.pdfLinks;
  }

  getPdfByNumber(number) {
    this.ensureLoaded();
    return this.pdfLinks.find((p) => p.surah_number === number);
  }

  getYoutubeVideos() {
    this.ensureLoaded();
    return this.youtubeVideos;
  }

  getYoutubeByNumber(number) {
    this.ensureLoaded();
    return this.youtubeVideos.filter((v) => v.card_number === number);
  }

  getStats() {
    this.ensureLoaded();
    const meccan = this.surahs.filter((s) => s.revelation_type === "مكية").length;
    const medinan = this.surahs.filter((s) => s.revelation_type === "مدنية").length;
    const totalAyahs = this.surahs.reduce((sum, s) => sum + s.ayahs_count, 0);
    const withYoutube = this.surahs.filter((s) => s.downloads?.youtube_video).length;

    return {
      total_surahs: this.surahs.length,
      meccan_surahs: meccan,
      medinan_surahs: medinan,
      total_ayahs: totalAyahs,
      surahs_with_youtube: withYoutube,
      total_youtube_videos: this.youtubeVideos.length,
    };
  }

  reload() {
    this.loaded = false;
    this.load();
  }
}

// Singleton instance
let instance = null;

export function getData(dataDir = "data") {
  if (!instance) {
    instance = new QuranData();
    instance.load(dataDir);
  }
  return instance;
}

export function resetData() {
  instance = null;
}
