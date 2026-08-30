# Al-Bitaqat Quran API

واجهة برمجة تطبيقات REST لبيانات بطاقات القرآن الكريم. مبنية بـ [Hono](https://hono.dev/) للأداء السريع.

## الميزات

- سرعة عالية وخفية (إطار Hono)
- حمايةامن(Security Headers + Rate Limiting)
- تحميل تلقائي للصوت و PDF عند التشغيل
- 114 سورة مع جميع البيانات
- روابط صوت و PDF و يوتيوب
- روابط محلية للتحميل بدون إنترنت
- Docker مع حفظ البيانات (Volume)
- اختبارات شاملة

## التشغيل

### محلياً

```bash
cd api
npm install
npm run dev
```

### Docker

```bash
# من المجلد الرئيسي للمشروع
docker build -t albitaqat-api -f api/Dockerfile .
docker run -p 3000:3000 albitaqat-api

# أو باستخدام docker-compose
cd api
docker compose up -d --build
```

**ملاحظة:** عند تشغيل Docker للمرة الأولى، يحمّل جميع ملفات الصوت (114 MP3) و PDF (114 ملف) تلقائياً (~5 دقائق).

## متغيرات البيئة

| المتغير | الافتراضي | الوصف |
|---------|-----------|-------|
| `PORT` | `3000` | المنفذ |
| `NODE_ENV` | `development` | البيئة |
| `CORS_ORIGINS` | `http://localhost:3000` | المصادر المسموحة |
| `RATE_LIMIT_MAX` | `100` | الحد الأقصى للطلبات |
| `RATE_LIMIT_WINDOW` | `60` | نافذة الوقت (ثانية) |
| `LOCAL_STORAGE_ENABLED` | `true` | تفعيل التخزين المحلي |
| `LOCAL_STORAGE_PATH` | `./data/local` | مسار التخزين |
| `AUTO_DOWNLOAD_ON_START` | `true` | تحميل تلقائي عند التشغيل |
| `LOG_LEVEL` | `info` | مستوى السجلات |

## API Endpoints

### Health

| Method | Endpoint | الوصف |
|--------|----------|-------|
| GET | `/api/health` | فحص صحة الخادم |
| GET | `/api/health/ready` | فحص الجاهزية |

### Surahs

| Method | Endpoint | الوصف |
|--------|----------|-------|
| GET | `/api/surahs` | جميع السور (114) |
| GET | `/api/surahs/:number` | سورة برقمها |
| GET | `/api/surahs/slug/:slug` | سورة بالاسم |
| GET | `/api/surahs/search?q=query` | بحث في السور |
| GET | `/api/surahs/type/:type` | مكية/مدنية |

### Media

| Method | Endpoint | الوصف |
|--------|----------|-------|
| GET | `/api/audio` | جميع روابط الصوت |
| GET | `/api/audio/:number` | صوت سورة محددة |
| GET | `/api/pdf` | جميع روابط PDF |
| GET | `/api/pdf/:number` | PDF سورة محددة |
| GET | `/api/youtube` | فيديوهات يوتيوب |
| GET | `/api/youtube/:number` | فيديو سورة محددة |
| GET | `/api/stats` | إحصائيات المشروع |

### Local Storage

| Method | Endpoint | الوصف |
|--------|----------|-------|
| GET | `/local/status` | حالة التخزين المحلي |
| GET | `/local/audio/:number` | تحميل صوت محلي |
| GET | `/local/pdf/:number` | تحميل PDF محلي |
| POST | `/local/download` | تحميل جميع الملفات |
| POST | `/local/download/youtube/:number` | تحميل فيديو يوتيوب |

## هيكل Response

```json
{
  "success": true,
  "data": { ... },
  "total": 114
}
```

### مثال: سورة مع روابط محلية

```json
{
  "success": true,
  "data": {
    "number": 4,
    "name_arabic": "النساء",
    "name_english": "An-Nisa",
    "downloads": {
      "audio": {
        "filename": "004_An-Nisa'.mp3",
        "url": "https://archive.org/download/.../004_An-Nisa%27.mp3",
        "local_url": "/local/audio/4"
      },
      "pdf": {
        "filename": "AlBitaqat-Book-ar_004.pdf",
        "url": "https://archive.org/download/.../AlBitaqat-Book-ar_004.pdf",
        "local_url": "/local/pdf/4"
      },
      "youtube_video": {
        "video_id": "cnsQgSxjJzU",
        "title": "البطاقات | البطاقة 4 | سورة النساء",
        "url": "https://www.youtube.com/watch?v=cnsQgSxjJzU",
        "thumbnail": "https://i2.ytimg.com/vi/cnsQgSxjJzU/hqdefault.jpg"
      }
    }
  }
}
```

**ملاحظة:** `local_url` يظهر فقط إذا كان الملف محمّلاً محلياً.

## الاختبارات

```bash
cd api
npm test
```

```
✅ Health Routes (2 tests)
✅ Surahs Routes (7 tests)
✅ Audio Routes (2 tests)
✅ PDF Routes (2 tests)
✅ YouTube Routes (2 tests)
✅ Stats Routes (1 test)
✅ Root Route (1 test)
✅ 404 Handler (1 test)
━━━━━━━━━━━━━━━━━━━━━━━━━━
18/18 tests passing
```

## التوثيق

راجع [docs/API.md](docs/API.md) للتفاصيل الكاملة.
