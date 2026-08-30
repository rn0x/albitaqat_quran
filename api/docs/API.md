# Al-Bitaqat Quran API Documentation

## Overview

REST API for Quran Cards data (Al-Bitaqat). Provides access to 114 Quran surahs with audio, PDF, and YouTube video links.

## Base URL

```
http://localhost:3000
```

## Authentication

No authentication required for public endpoints.

## Rate Limiting

- **Limit**: 100 requests per minute
- **Window**: 60 seconds
- **Response**: 429 Too Many Requests with `retryAfter` field

## Endpoints

### Health Check

#### `GET /api/health`

Check server health status.

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": "2024-01-01T00:00:00.000Z",
    "uptime": 12345,
    "version": "1.0.0",
    "local_storage": true
  }
}
```

#### `GET /api/health/ready`

Check if service is ready.

**Response:**
```json
{
  "success": true,
  "data": {
    "ready": true,
    "surahsLoaded": 114
  }
}
```

---

### Surahs

#### `GET /api/surahs`

Get all 114 Quran surahs.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "number": 1,
      "name_arabic": "الفاتحة",
      "name_english": "Al-Fatihah",
      "ayahs_count": 7,
      "revelation_type": "مكية",
      "slug": "al-fatihah",
      "page_url": "https://albitaqat.com/al-fatihah/",
      "downloads": {
        "audio": {
          "filename": "001_Al-Fatihah.mp3",
          "url": "https://archive.org/download/...",
          "local_url": "/local/audio/1"
        },
        "pdf": {
          "filename": "AlBitaqat-Book-ar_001.pdf",
          "url": "https://archive.org/download/...",
          "local_url": "/local/pdf/1"
        },
        "youtube_video": {
          "video_id": "snpE5nt3fPY",
          "title": "البطاقة (1): سُورَةُ الفَاتِحَةِ",
          "url": "https://www.youtube.com/watch?v=snpE5nt3fPY",
          "thumbnail": "https://i2.ytimg.com/vi/snpE5nt3fPY/hqdefault.jpg"
        }
      }
    }
  ],
  "total": 114
}
```

#### `GET /api/surahs/:number`

Get surah by number (1-114).

**Parameters:**
- `number` (path, required): Surah number (1-114)

**Example:**
```
GET /api/surahs/1
```

**Response:**
```json
{
  "success": true,
  "data": {
    "number": 1,
    "name_arabic": "الفاتحة",
    "name_english": "Al-Fatihah",
    ...
  }
}
```

#### `GET /api/surahs/slug/:slug`

Get surah by URL slug.

**Parameters:**
- `slug` (path, required): Surah slug (e.g., "al-fatihah")

**Example:**
```
GET /api/surahs/slug/al-fatihah
```

#### `GET /api/surahs/search?q=query`

Search surahs by name.

**Parameters:**
- `q` (query, required): Search query

**Example:**
```
GET /api/surahs/search?q=بقرة
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "number": 2,
      "name_arabic": "البقرة",
      ...
    }
  ],
  "total": 1,
  "query": "بقرة"
}
```

#### `GET /api/surahs/type/:type`

Get surahs by revelation type.

**Parameters:**
- `type` (path, required): "مكية" (Meccan) or "مدنية" (Medinan)

**Example:**
```
GET /api/surahs/type/مكية
```

---

### Audio

#### `GET /api/audio`

Get all audio download links.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "surah_number": 1,
      "surah_name_arabic": "الفاتحة",
      "surah_name_english": "Al-Fatihah",
      "filename": "001_Al-Fatihah.mp3",
      "url": "https://archive.org/download/..."
    }
  ],
  "total": 114
}
```

#### `GET /api/audio/:number`

Get audio link for specific surah.

**Parameters:**
- `number` (path, required): Surah number (1-114)

---

### PDF

#### `GET /api/pdf`

Get all PDF download links.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "surah_number": 1,
      "surah_name_arabic": "الفاتحة",
      "surah_name_english": "Al-Fatihah",
      "filename": "AlBitaqat-Book-ar_001.pdf",
      "url": "https://archive.org/download/..."
    }
  ],
  "total": 114
}
```

#### `GET /api/pdf/:number`

Get PDF link for specific surah.

**Parameters:**
- `number` (path, required): Surah number (1-114)

---

### YouTube

#### `GET /api/youtube`

Get all YouTube videos.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "video_id": "snpE5nt3fPY",
      "title": "البطاقة (1): سُورَةُ الفَاتِحَةِ | البطاقات",
      "url": "https://www.youtube.com/watch?v=snpE5nt3fPY",
      "thumbnail": "https://i2.ytimg.com/vi/snpE5nt3fPY/hqdefault.jpg",
      "card_number": 1
    }
  ],
  "total": 140
}
```

#### `GET /api/youtube/:number`

Get YouTube videos for specific surah.

**Parameters:**
- `number` (path, required): Surah number (1-114)

---

### Statistics

#### `GET /api/stats`

Get project statistics.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_surahs": 114,
    "meccan_surahs": 86,
    "medinan_surahs": 28,
    "total_ayahs": 6236,
    "surahs_with_youtube": 114,
    "total_youtube_videos": 140
  }
}
```

---

### Local Storage

#### `GET /local/audio/:number`

Download local audio file.

**Parameters:**
- `number` (path, required): Surah number (1-114)

**Response:** Binary audio file (MP3)

#### `GET /local/pdf/:number`

Download local PDF file.

**Parameters:**
- `number` (path, required): Surah number (1-114)

**Response:** Binary PDF file

#### `GET /local/status`

Check local storage status.

**Response:**
```json
{
  "success": true,
  "data": {
    "enabled": true,
    "baseDir": "./data/local",
    "audioDir": "./data/local/audio",
    "pdfDir": "./data/local/pdf",
    "audioCount": 114,
    "pdfCount": 114,
    "totalSize": "350.5 MB"
  }
}
```

#### `POST /local/download`

Trigger download all audio and PDF files to local storage.

**Response:**
```json
{
  "success": true,
  "data": {
    "audio": { "downloaded": 114, "failed": 0 },
    "pdf": { "downloaded": 114, "failed": 0 }
  }
}
```

#### `POST /local/download/youtube/:number`

Download YouTube video for a specific surah using yt-dlp.

**Parameters:**
- `number` (path, required): Surah number (1-114)

**Example:**
```
POST /local/download/youtube/1
```

**Response:**
```json
{
  "success": true,
  "message": "YouTube video for surah 1 downloaded successfully"
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "success": false,
  "error": "Error message"
}
```

**Common HTTP Status Codes:**

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request (invalid parameters) |
| 404 | Not Found |
| 429 | Too Many Requests |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `3000` | Server port |
| `NODE_ENV` | `development` | Environment |
| `CORS_ORIGINS` | `http://localhost:3000` | Allowed origins (comma-separated) |
| `RATE_LIMIT_MAX` | `100` | Max requests per window |
| `RATE_LIMIT_WINDOW` | `60` | Window duration in seconds |
| `LOCAL_STORAGE_ENABLED` | `true` | Enable local file storage |
| `LOCAL_STORAGE_PATH` | `./data/local` | Local storage path |
| `AUTO_DOWNLOAD_ON_START` | `true` | Auto-download files on startup |
| `LOG_LEVEL` | `info` | Logging level |

---

## Examples

### cURL

```bash
# Get all surahs
curl http://localhost:3000/api/surahs

# Get surah by number
curl http://localhost:3000/api/surahs/1

# Search surahs
curl "http://localhost:3000/api/surahs/search?q=بقرة"

# Get audio links
curl http://localhost:3000/api/audio

# Get statistics
curl http://localhost:3000/api/stats
```

### JavaScript (fetch)

```javascript
// Get all surahs
const response = await fetch('http://localhost:3000/api/surahs');
const data = await response.json();
console.log(data.data); // Array of 114 surahs

// Get surah by number
const surah = await fetch('http://localhost:3000/api/surahs/1');
const surahData = await surah.json();
console.log(surahData.data.name_arabic); // "الفاتحة"
```

### Python (requests)

```python
import requests

# Get all surahs
response = requests.get('http://localhost:3000/api/surahs')
data = response.json()
print(data['data'])  # List of 114 surahs

# Get surah by number
surah = requests.get('http://localhost:3000/api/surahs/1')
print(surah.json()['data']['name_arabic'])  # "الفاتحة"
```
