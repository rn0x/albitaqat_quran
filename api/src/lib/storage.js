import { existsSync, mkdirSync, createWriteStream } from "fs";
import { join } from "path";
import { exec } from "child_process";
import { promisify } from "util";
import { getData } from "./data.js";

const execAsync = promisify(exec);

class LocalStorage {
  constructor(basePath, logger) {
    this.basePath = basePath;
    this.audioDir = join(basePath, "audio");
    this.pdfDir = join(basePath, "pdf");
    this.youtubeDir = join(basePath, "youtube");
    this.logger = logger;
    this.ensureDirs();
  }

  ensureDirs() {
    for (const dir of [this.audioDir, this.pdfDir, this.youtubeDir]) {
      if (!existsSync(dir)) {
        mkdirSync(dir, { recursive: true });
      }
    }
  }

  getAudioPath(number) {
    const data = getData();
    const surah = data.getSurahByNumber(number);
    if (!surah?.downloads?.audio) return "";
    return join(this.audioDir, surah.downloads.audio.filename);
  }

  getPdfPath(number) {
    const data = getData();
    const surah = data.getSurahByNumber(number);
    if (!surah?.downloads?.pdf) return "";
    return join(this.pdfDir, surah.downloads.pdf.filename);
  }

  getYoutubeDir(number) {
    const data = getData();
    const surah = data.getSurahByNumber(number);
    if (!surah) return "";
    return join(this.youtubeDir, surah.name_english);
  }

  isAudioDownloaded(number) {
    const path = this.getAudioPath(number);
    return path ? existsSync(path) : false;
  }

  isPdfDownloaded(number) {
    const path = this.getPdfPath(number);
    return path ? existsSync(path) : false;
  }

  async downloadFile(url, dest, retries = 3) {
    for (let attempt = 1; attempt <= retries; attempt++) {
      try {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 60000); // 60s timeout

        const response = await fetch(url, { signal: controller.signal });
        clearTimeout(timeout);

        if (!response.ok) {
          if (attempt === retries) return false;
          await new Promise((r) => setTimeout(r, 1000 * attempt));
          continue;
        }

        const fileStream = createWriteStream(dest);
        const reader = response.body?.getReader();

        if (!reader) return false;

        let downloaded = 0;
        const contentLength = parseInt(response.headers.get("content-length") || "0");

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          fileStream.write(value);
          downloaded += value.length;
        }

        fileStream.end();
        return true;
      } catch (err) {
        if (attempt === retries) return false;
        await new Promise((r) => setTimeout(r, 1000 * attempt));
      }
    }
    return false;
  }

  async downloadAudio(number) {
    const data = getData();
    const surah = data.getSurahByNumber(number);
    if (!surah?.downloads?.audio) return false;

    const dest = this.getAudioPath(number);
    if (existsSync(dest)) return true;

    return this.downloadFile(surah.downloads.audio.url, dest);
  }

  async downloadPdf(number) {
    const data = getData();
    const surah = data.getSurahByNumber(number);
    if (!surah?.downloads?.pdf) return false;

    const dest = this.getPdfPath(number);
    if (existsSync(dest)) return true;

    return this.downloadFile(surah.downloads.pdf.url, dest);
  }

  async downloadAll(concurrency = 5) {
    const data = getData();
    const surahs = data.getAllSurahs();
    const total = surahs.length;
    let audioCount = 0;
    let pdfCount = 0;
    let audioFailed = 0;
    let pdfFailed = 0;

    this.logger?.info(`📥 Starting download of ${total} surahs (audio + pdf)...`);

    // Download in batches
    for (let i = 0; i < total; i += concurrency) {
      const batch = surahs.slice(i, i + concurrency);
      const batchNum = Math.floor(i / concurrency) + 1;
      const totalBatches = Math.ceil(total / concurrency);

      const results = await Promise.all(
        batch.map(async (surah) => {
          const [audio, pdf] = await Promise.all([
            this.downloadAudio(surah.number),
            this.downloadPdf(surah.number),
          ]);
          return { number: surah.number, audio, pdf };
        })
      );

      for (const r of results) {
        if (r.audio) audioCount++;
        else audioFailed++;
        if (r.pdf) pdfCount++;
        else pdfFailed++;
      }

      const progress = Math.min(i + concurrency, total);
      this.logger?.info(
        `📊 Progress: ${progress}/${total} (${Math.round((progress / total) * 100)}%) - Audio: ${audioCount}, PDF: ${pdfCount}`
      );
    }

    this.logger?.info(
      `✅ Download complete! Audio: ${audioCount}/${total}, PDF: ${pdfCount}/${total}`
    );
    if (audioFailed > 0 || pdfFailed > 0) {
      this.logger?.warn(
        `⚠️ Failed: Audio: ${audioFailed}, PDF: ${pdfFailed}`
      );
    }

    return { audio: audioCount, pdf: pdfCount, audioFailed, pdfFailed };
  }

  getStorageInfo() {
    return {
      audioDir: this.audioDir,
      pdfDir: this.pdfDir,
      youtubeDir: this.youtubeDir,
    };
  }

  async downloadYoutube(number) {
    const data = getData();
    const surah = data.getSurahByNumber(number);
    if (!surah?.downloads?.youtube_video) return false;

    const video = surah.downloads.youtube_video;
    const surahDir = join(this.youtubeDir, surah.name_english);

    if (!existsSync(surahDir)) {
      mkdirSync(surahDir, { recursive: true });
    }

    // Check if already downloaded
    const { readdirSync } = await import("fs");
    const files = readdirSync(surahDir);
    if (files.some((f) => f.endsWith(".mp4"))) return true;

    try {
      const cmd = `yt-dlp --no-warnings -f "best[ext=mp4]/best" --merge-output-format mp4 -o "${surahDir}/%(title)s.%(ext)s" "${video.url}"`;
      await execAsync(cmd, { timeout: 300000 }); // 5 min timeout
      return true;
    } catch (err) {
      this.logger?.error({ err, surah: number }, "YouTube download failed");
      return false;
    }
  }

  getLocalStatus() {
    const data = getData();
    const surahs = data.getAllSurahs();
    let audioCount = 0;
    let pdfCount = 0;

    for (const surah of surahs) {
      if (this.isAudioDownloaded(surah.number)) audioCount++;
      if (this.isPdfDownloaded(surah.number)) pdfCount++;
    }

    return {
      total: surahs.length,
      audio: audioCount,
      pdf: pdfCount,
      audioDir: this.audioDir,
      pdfDir: this.pdfDir,
    };
  }
}

// Singleton instance
let storageInstance = null;

export function getStorage(basePath = "./data/local", logger) {
  if (!storageInstance) {
    storageInstance = new LocalStorage(basePath, logger);
  }
  return storageInstance;
}

export function resetStorage() {
  storageInstance = null;
}
