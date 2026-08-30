# هيكل المشروع

```
albitaqat_quran/
├── README.md                    # الوثائق الرئيسية
├── STRUCTURE.md                 # هيكل المشروع
├── main.py                      # النقطة الرئيسية (Python)
├── bt-qr.jpg                    # صورة المشروع
├── logo_up.png                  # الشعار
│
├── data/                        # ملفات البيانات
│   ├── quran_cards.json         # بيانات شاملة مع media
│   ├── quran_cards_full.json    # بيانات شاملة مع downloads
│   ├── audio_links.json         # روابط الصوت
│   ├── pdf_links.json           # روابط PDF
│   ├── youtube_videos.json      # فيديوهات يوتيوب
│   ├── audio_download_page.json # بيانات صفحة الصوت
│   ├── pdf_book_page.json       # بيانات صفحة PDF
│   └── local/                   # الملفات المحملة محلياً
│       ├── audio/
│       └── pdf/
│
├── api/                         # Node.js API (Hono)
│   ├── package.json             # التبعيات
│   ├── .env.example             # متغيرات البيئة
│   ├── Dockerfile               # Docker
│   ├── docker-compose.yml       # Docker Compose
│   ├── .gitignore
│   ├── .dockerignore
│   ├── README.md                # توثيق API
│   │
│   ├── src/
│   │   ├── index.js             # نقطة البداية
│   │   ├── app.js               # إعدادات Hono
│   │   ├── lib/
│   │   │   ├── data.js          # تحميل البيانات
│   │   │   ├── storage.js       # التخزين المحلي
│   │   │   ├── cache.js         # التخزين المؤقت
│   │   │   └── logger.js        # التسجيل
│   │   ├── middleware/
│   │   │   ├── cors.js          # CORS
│   │   │   ├── security.js      # Headers أمنية
│   │   │   ├── rateLimiter.js   # Rate limiting
│   │   │   └── errorHandler.js  # معالجة الأخطاء
│   │   └── routes/
│   │       ├── health.js        # /api/health
│   │       ├── surahs.js        # /api/surahs
│   │       ├── audio.js         # /api/audio
│   │       ├── pdf.js           # /api/pdf
│   │       ├── youtube.js       # /api/youtube
│   │       ├── stats.js         # /api/stats
│   │       └── local.js         # /local/*
│   │
│   ├── tests/
│   │   └── api.test.js          # اختبارات API
│   │
│   └── docs/
│       └── API.md               # توثيق API الكامل
│
├── scripts/                     # سكريبتات Python
│   ├── scraper.py               # مكشط البيانات
│   └── generate_links.py        # مولّد الروابط
│
└── src/                         # كود Python
      ├── __init__.py
      ├── downloader.py            # سكربت التحميل
      └── requirements.txt         # المتطلبات
```

## أوامر التشغيل

### Python Scripts

```bash
# تشغيل المكشط
python3 main.py

# تحميل الملفات
python3 src/downloader.py --mode full
python3 src/downloader.py --mode youtube
python3 src/downloader.py --mode full --with-youtube
```

### Node.js API

```bash
# تطوير
cd api && npm run dev

# إنتاج
cd api && npm start

# اختبارات
cd api && npm test

# Docker
cd api && docker-compose up -d
```

## API Endpoints

| Method | Endpoint | الوصف |
|--------|----------|-------|
| GET | `/api/health` | فحص صحة الخادم |
| GET | `/api/health/ready` | فحص جاهزية الخدمة |
| GET | `/api/surahs` | جميع السور (114) |
| GET | `/api/surahs/:number` | سورة برقمها |
| GET | `/api/surahs/slug/:slug` | سورة بالاسم |
| GET | `/api/surahs/search?q=query` | بحث في السور |
| GET | `/api/surahs/type/:type` | مكية/مدنية |
| GET | `/api/audio` | روابط الصوت |
| GET | `/api/audio/:number` | صوت سورة محددة |
| GET | `/api/pdf` | روابط PDF |
| GET | `/api/pdf/:number` | PDF سورة محددة |
| GET | `/api/youtube` | فيديوهات يوتيوب |
| GET | `/api/youtube/:number` | فيديو سورة محددة |
| GET | `/api/stats` | إحصائيات المشروع |
| GET | `/local/audio/:number` | تحميل صوت محلي |
| GET | `/local/pdf/:number` | تحميل PDF محلي |
| GET | `/local/status` | حالة التخزين المحلي |
| POST | `/local/download` | تحميل جميع الملفات |
| POST | `/local/download/youtube/:number` | تحميل فيديو يوتيوب |

## معلومات المشروع

- **المؤلف:** أ.د. ياسر بن إسماعيل راضي
- **الموقع:** [albitaqat.com](https://albitaqat.com/)
- **عدد السور:** 114 سورة
- **عدد الفيديوهات:** 140+ فيديو
