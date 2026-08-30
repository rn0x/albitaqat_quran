import { Hono } from "hono";
import { existsSync, createReadStream } from "fs";
import { getStorage } from "../lib/storage.js";

const local = new Hono();

// GET /local/audio/:number - Serve local audio file
local.get("/audio/:number", async (c) => {
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

  const storage = getStorage();
  const filePath = storage.getAudioPath(number);

  if (!filePath || !existsSync(filePath)) {
    return c.json(
      {
        success: false,
        error: `Audio file for surah ${number} not downloaded locally`,
      },
      404
    );
  }

  const fileStream = createReadStream(filePath);
  const chunks = [];

  return new Promise((resolve) => {
    fileStream.on("data", (chunk) => chunks.push(chunk));
    fileStream.on("end", () => {
      const buffer = Buffer.concat(chunks);
      resolve(
        new Response(buffer, {
          headers: {
            "Content-Type": "audio/mpeg",
            "Content-Disposition": `attachment; filename="${filePath.split("/").pop()}"`,
          },
        })
      );
    });
    fileStream.on("error", () => {
      resolve(
        c.json({ success: false, error: "Error reading file" }, 500)
      );
    });
  });
});

// GET /local/pdf/:number - Serve local PDF file
local.get("/pdf/:number", async (c) => {
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

  const storage = getStorage();
  const filePath = storage.getPdfPath(number);

  if (!filePath || !existsSync(filePath)) {
    return c.json(
      {
        success: false,
        error: `PDF file for surah ${number} not downloaded locally`,
      },
      404
    );
  }

  const fileStream = createReadStream(filePath);
  const chunks = [];

  return new Promise((resolve) => {
    fileStream.on("data", (chunk) => chunks.push(chunk));
    fileStream.on("end", () => {
      const buffer = Buffer.concat(chunks);
      resolve(
        new Response(buffer, {
          headers: {
            "Content-Type": "application/pdf",
            "Content-Disposition": `attachment; filename="${filePath.split("/").pop()}"`,
          },
        })
      );
    });
    fileStream.on("error", () => {
      resolve(
        c.json({ success: false, error: "Error reading file" }, 500)
      );
    });
  });
});

// GET /local/status - Check local storage status
local.get("/status", (c) => {
  const storage = getStorage();
  const status = storage.getLocalStatus();

  return c.json({
    success: true,
    data: status,
  });
});

// POST /local/download - Trigger download all files
local.post("/download", async (c) => {
  const storage = getStorage();

  try {
    const result = await storage.downloadAll();
    return c.json({
      success: true,
      data: result,
    });
  } catch (err) {
    return c.json(
      {
        success: false,
        error: err.message,
      },
      500
    );
  }
});

// POST /local/download/youtube/:number - Download YouTube video for a surah
local.post("/download/youtube/:number", async (c) => {
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

  const storage = getStorage();

  try {
    const result = await storage.downloadYoutube(number);
    if (result) {
      return c.json({
        success: true,
        message: `YouTube video for surah ${number} downloaded successfully`,
      });
    } else {
      return c.json(
        {
          success: false,
          error: `Failed to download YouTube video for surah ${number}`,
        },
        500
      );
    }
  } catch (err) {
    return c.json(
      {
        success: false,
        error: err.message,
      },
      500
    );
  }
});

export default local;
