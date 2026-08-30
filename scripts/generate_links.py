#!/usr/bin/env python3
"""
سكربت إنشاء ملفات JSON لبيانات بطاقات القرآن الكريم
يتضمن روابط التحميل المباشرة للصوت والـ PDF وروابط يوتيوب
"""

import json
import re
from urllib.parse import unquote, quote

try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call(["pip", "install", "requests", "-q"])
    import requests

# ─── بيانات السور ───────────────────────────────────────────────
SURAH_DATA = [
    {"number": 1, "name_ar": "الفاتحة", "name_en": "Al-Fatihah", "ayahs": 7, "type": "مكية", "slug": "al-fatihah"},
    {"number": 2, "name_ar": "البقرة", "name_en": "Al-Baqarah", "ayahs": 286, "type": "مدنية", "slug": "al-baqarah"},
    {"number": 3, "name_ar": "آل عمران", "name_en": "Al-Imran", "ayahs": 200, "type": "مدنية", "slug": "al-imran"},
    {"number": 4, "name_ar": "النساء", "name_en": "An-Nisa", "ayahs": 176, "type": "مدنية", "slug": "an-nisa"},
    {"number": 5, "name_ar": "المائدة", "name_en": "Al-Maidah", "ayahs": 120, "type": "مدنية", "slug": "al-maidah"},
    {"number": 6, "name_ar": "الأنعام", "name_en": "Al-Anam", "ayahs": 165, "type": "مكية", "slug": "al-anam"},
    {"number": 7, "name_ar": "الأعراف", "name_en": "Al-Araf", "ayahs": 206, "type": "مكية", "slug": "al-araf"},
    {"number": 8, "name_ar": "الأنفال", "name_en": "Al-Anfal", "ayahs": 75, "type": "مدنية", "slug": "al-anfal"},
    {"number": 9, "name_ar": "التوبة", "name_en": "At-Tawbah", "ayahs": 129, "type": "مدنية", "slug": "at-tawbah"},
    {"number": 10, "name_ar": "يونس", "name_en": "Yunus", "ayahs": 109, "type": "مكية", "slug": "yoonus"},
    {"number": 11, "name_ar": "هود", "name_en": "Hud", "ayahs": 123, "type": "مكية", "slug": "hud"},
    {"number": 12, "name_ar": "يوسف", "name_en": "Yusuf", "ayahs": 111, "type": "مكية", "slug": "yusuf"},
    {"number": 13, "name_ar": "الرعد", "name_en": "Ar-Rad", "ayahs": 43, "type": "مدنية", "slug": "ar-rad"},
    {"number": 14, "name_ar": "إبراهيم", "name_en": "Ibrahim", "ayahs": 52, "type": "مكية", "slug": "ibrahim"},
    {"number": 15, "name_ar": "الحجر", "name_en": "Al-Hijr", "ayahs": 99, "type": "مكية", "slug": "al-hijr"},
    {"number": 16, "name_ar": "النحل", "name_en": "An-Nahl", "ayahs": 128, "type": "مكية", "slug": "an-nahl"},
    {"number": 17, "name_ar": "الإسراء", "name_en": "Al-Isra", "ayahs": 111, "type": "مكية", "slug": "al-isra"},
    {"number": 18, "name_ar": "الكهف", "name_en": "Al-Kahf", "ayahs": 110, "type": "مكية", "slug": "al-kahf"},
    {"number": 19, "name_ar": "مريم", "name_en": "Maryam", "ayahs": 98, "type": "مكية", "slug": "maryam"},
    {"number": 20, "name_ar": "طه", "name_en": "Taha", "ayahs": 135, "type": "مكية", "slug": "ta-ha"},
    {"number": 21, "name_ar": "الأنبياء", "name_en": "Al-Anbiya", "ayahs": 112, "type": "مكية", "slug": "al-anbiya"},
    {"number": 22, "name_ar": "الحج", "name_en": "Al-Hajj", "ayahs": 78, "type": "مدنية", "slug": "al-hajj"},
    {"number": 23, "name_ar": "المؤمنون", "name_en": "Al-Muminun", "ayahs": 118, "type": "مكية", "slug": "al-muminun"},
    {"number": 24, "name_ar": "النور", "name_en": "An-Nur", "ayahs": 64, "type": "مدنية", "slug": "an-nur"},
    {"number": 25, "name_ar": "الفرقان", "name_en": "Al-Furqan", "ayahs": 77, "type": "مكية", "slug": "al-furqan"},
    {"number": 26, "name_ar": "الشعراء", "name_en": "Ash-Shuara", "ayahs": 227, "type": "مكية", "slug": "ash-shuara"},
    {"number": 27, "name_ar": "النمل", "name_en": "An-Naml", "ayahs": 93, "type": "مكية", "slug": "an-naml"},
    {"number": 28, "name_ar": "القصص", "name_en": "Al-Qasas", "ayahs": 88, "type": "مكية", "slug": "al-qasas"},
    {"number": 29, "name_ar": "العنكبوت", "name_en": "Al-Ankabut", "ayahs": 69, "type": "مكية", "slug": "al-ankabut"},
    {"number": 30, "name_ar": "الروم", "name_en": "Ar-Rum", "ayahs": 60, "type": "مكية", "slug": "ar-rum"},
    {"number": 31, "name_ar": "لقمان", "name_en": "Luqman", "ayahs": 34, "type": "مكية", "slug": "luqman"},
    {"number": 32, "name_ar": "السجدة", "name_en": "As-Sajdah", "ayahs": 30, "type": "مكية", "slug": "as-sajdah"},
    {"number": 33, "name_ar": "الأحزاب", "name_en": "Al-Ahzab", "ayahs": 73, "type": "مدنية", "slug": "al-ahzab"},
    {"number": 34, "name_ar": "سبأ", "name_en": "Saba", "ayahs": 54, "type": "مكية", "slug": "saba"},
    {"number": 35, "name_ar": "فاطر", "name_en": "Fatir", "ayahs": 45, "type": "مكية", "slug": "fatir"},
    {"number": 36, "name_ar": "يس", "name_en": "Ya-Sin", "ayahs": 83, "type": "مكية", "slug": "ya-sin"},
    {"number": 37, "name_ar": "الصافات", "name_en": "As-Saffat", "ayahs": 182, "type": "مكية", "slug": "as-saffat"},
    {"number": 38, "name_ar": "ص", "name_en": "Sad", "ayahs": 88, "type": "مكية", "slug": "sad"},
    {"number": 39, "name_ar": "الزمر", "name_en": "Az-Zumar", "ayahs": 75, "type": "مكية", "slug": "az-zumar"},
    {"number": 40, "name_ar": "غافر", "name_en": "Ghafir", "ayahs": 85, "type": "مكية", "slug": "ghafir"},
    {"number": 41, "name_ar": "فصلت", "name_en": "Fussilat", "ayahs": 54, "type": "مكية", "slug": "fussilat"},
    {"number": 42, "name_ar": "الشورى", "name_en": "Ash-Shura", "ayahs": 53, "type": "مكية", "slug": "ash-shura"},
    {"number": 43, "name_ar": "الزخرف", "name_en": "Az-Zukhruf", "ayahs": 89, "type": "مكية", "slug": "az-zukhruf"},
    {"number": 44, "name_ar": "الدخان", "name_en": "Ad-Dukhan", "ayahs": 59, "type": "مكية", "slug": "ad-dukhan"},
    {"number": 45, "name_ar": "الجاثية", "name_en": "Al-Jathiyah", "ayahs": 37, "type": "مكية", "slug": "al-jathiyah"},
    {"number": 46, "name_ar": "الأحقاف", "name_en": "Al-Ahqaf", "ayahs": 35, "type": "مكية", "slug": "al-ahqaf"},
    {"number": 47, "name_ar": "محمد", "name_en": "Muhammad", "ayahs": 38, "type": "مدنية", "slug": "muhammad"},
    {"number": 48, "name_ar": "الفتح", "name_en": "Al-Fath", "ayahs": 29, "type": "مدنية", "slug": "al-fath"},
    {"number": 49, "name_ar": "الحجرات", "name_en": "Al-Hujurat", "ayahs": 18, "type": "مدنية", "slug": "al-hujurat"},
    {"number": 50, "name_ar": "ق", "name_en": "Qaf", "ayahs": 45, "type": "مكية", "slug": "qaf"},
    {"number": 51, "name_ar": "الذاريات", "name_en": "Adh-Dhariyat", "ayahs": 60, "type": "مكية", "slug": "ad-dhariyat"},
    {"number": 52, "name_ar": "الطور", "name_en": "At-Tur", "ayahs": 49, "type": "مكية", "slug": "at-tur"},
    {"number": 53, "name_ar": "النجم", "name_en": "An-Najm", "ayahs": 62, "type": "مكية", "slug": "an-najm"},
    {"number": 54, "name_ar": "القمر", "name_en": "Al-Qamar", "ayahs": 55, "type": "مكية", "slug": "al-qamar"},
    {"number": 55, "name_ar": "الرحمن", "name_en": "Ar-Rahman", "ayahs": 78, "type": "مدنية", "slug": "ar-rahman"},
    {"number": 56, "name_ar": "الواقعة", "name_en": "Al-Waqiah", "ayahs": 96, "type": "مكية", "slug": "al-waqiah"},
    {"number": 57, "name_ar": "الحديد", "name_en": "Al-Hadid", "ayahs": 29, "type": "مدنية", "slug": "al-hadid"},
    {"number": 58, "name_ar": "المجادلة", "name_en": "Al-Mujadilah", "ayahs": 22, "type": "مدنية", "slug": "al-mujadilah"},
    {"number": 59, "name_ar": "الحشر", "name_en": "Al-Hashr", "ayahs": 24, "type": "مدنية", "slug": "al-hashr"},
    {"number": 60, "name_ar": "الممتحنة", "name_en": "Al-Mumtahinah", "ayahs": 13, "type": "مدنية", "slug": "al-mumtahanah"},
    {"number": 61, "name_ar": "الصف", "name_en": "As-Saff", "ayahs": 14, "type": "مدنية", "slug": "as-saff"},
    {"number": 62, "name_ar": "الجمعة", "name_en": "Al-Jumuah", "ayahs": 11, "type": "مدنية", "slug": "al-jumuah"},
    {"number": 63, "name_ar": "المنافقون", "name_en": "Al-Munafiqun", "ayahs": 11, "type": "مدنية", "slug": "al-munafiqun"},
    {"number": 64, "name_ar": "التغابن", "name_en": "At-Taghabun", "ayahs": 18, "type": "مدنية", "slug": "at-taghabun"},
    {"number": 65, "name_ar": "الطلاق", "name_en": "At-Talaq", "ayahs": 12, "type": "مدنية", "slug": "at-talaq"},
    {"number": 66, "name_ar": "التحريم", "name_en": "At-Tahrim", "ayahs": 12, "type": "مدنية", "slug": "at-tahrim"},
    {"number": 67, "name_ar": "الملك", "name_en": "Al-Mulk", "ayahs": 30, "type": "مكية", "slug": "al-mulk"},
    {"number": 68, "name_ar": "القلم", "name_en": "Al-Qalam", "ayahs": 52, "type": "مكية", "slug": "al-qalam"},
    {"number": 69, "name_ar": "الحاقة", "name_en": "Al-Haqqah", "ayahs": 52, "type": "مكية", "slug": "al-haqqah"},
    {"number": 70, "name_ar": "المعارج", "name_en": "Al-Maarij", "ayahs": 44, "type": "مكية", "slug": "al-maarij"},
    {"number": 71, "name_ar": "نوح", "name_en": "Nuh", "ayahs": 28, "type": "مكية", "slug": "nuh"},
    {"number": 72, "name_ar": "الجن", "name_en": "Al-Jinn", "ayahs": 28, "type": "مكية", "slug": "al-jinn"},
    {"number": 73, "name_ar": "المزمل", "name_en": "Al-Muzzammil", "ayahs": 20, "type": "مكية", "slug": "al-muzammil"},
    {"number": 74, "name_ar": "المدثر", "name_en": "Al-Muddathir", "ayahs": 56, "type": "مكية", "slug": "al-mudathir"},
    {"number": 75, "name_ar": "القيامة", "name_en": "Al-Qiyamah", "ayahs": 40, "type": "مكية", "slug": "al-qiyamah"},
    {"number": 76, "name_ar": "الإنسان", "name_en": "Al-Insan", "ayahs": 31, "type": "مدنية", "slug": "al-insane"},
    {"number": 77, "name_ar": "المرسلات", "name_en": "Al-Mursalat", "ayahs": 50, "type": "مكية", "slug": "al-mursalat"},
    {"number": 78, "name_ar": "النبأ", "name_en": "An-Naba", "ayahs": 40, "type": "مكية", "slug": "an-naba"},
    {"number": 79, "name_ar": "النازعات", "name_en": "An-Naziat", "ayahs": 46, "type": "مكية", "slug": "an-naziat"},
    {"number": 80, "name_ar": "عبس", "name_en": "Abasa", "ayahs": 42, "type": "مكية", "slug": "abasa"},
    {"number": 81, "name_ar": "التكوير", "name_en": "At-Takwir", "ayahs": 29, "type": "مكية", "slug": "at-takwir"},
    {"number": 82, "name_ar": "الإنفطار", "name_en": "Al-Infitar", "ayahs": 19, "type": "مكية", "slug": "al-infitar"},
    {"number": 83, "name_ar": "المطففين", "name_en": "Al-Mutaffifin", "ayahs": 36, "type": "مكية", "slug": "al-mutaffifeen"},
    {"number": 84, "name_ar": "الانشقاق", "name_en": "Al-Inshiqaq", "ayahs": 25, "type": "مكية", "slug": "al-inshiqaq"},
    {"number": 85, "name_ar": "البروج", "name_en": "Al-Buruj", "ayahs": 22, "type": "مكية", "slug": "al-buruj"},
    {"number": 86, "name_ar": "الطارق", "name_en": "At-Tariq", "ayahs": 17, "type": "مكية", "slug": "at-tariq"},
    {"number": 87, "name_ar": "الأعلى", "name_en": "Al-Ala", "ayahs": 19, "type": "مكية", "slug": "al-ala"},
    {"number": 88, "name_ar": "الغاشية", "name_en": "Al-Ghashiyah", "ayahs": 26, "type": "مكية", "slug": "al-ghashiya"},
    {"number": 89, "name_ar": "الفجر", "name_en": "Al-Fajr", "ayahs": 30, "type": "مكية", "slug": "al-fajr"},
    {"number": 90, "name_ar": "البلد", "name_en": "Al-Balad", "ayahs": 20, "type": "مكية", "slug": "al-balad"},
    {"number": 91, "name_ar": "الشمس", "name_en": "Ash-Shams", "ayahs": 15, "type": "مكية", "slug": "ash-shams"},
    {"number": 92, "name_ar": "الليل", "name_en": "Al-Layl", "ayahs": 21, "type": "مكية", "slug": "al-layl"},
    {"number": 93, "name_ar": "الضحى", "name_en": "Ad-Duha", "ayahs": 11, "type": "مكية", "slug": "ad-duha"},
    {"number": 94, "name_ar": "الشرح", "name_en": "Ash-Sharh", "ayahs": 8, "type": "مكية", "slug": "ash-sharh"},
    {"number": 95, "name_ar": "التين", "name_en": "At-Tin", "ayahs": 8, "type": "مكية", "slug": "at-tin"},
    {"number": 96, "name_ar": "العلق", "name_en": "Al-Alaq", "ayahs": 19, "type": "مكية", "slug": "al-alaq"},
    {"number": 97, "name_ar": "القدر", "name_en": "Al-Qadr", "ayahs": 5, "type": "مكية", "slug": "al-qadr"},
    {"number": 98, "name_ar": "البينة", "name_en": "Al-Bayyinah", "ayahs": 8, "type": "مدنية", "slug": "al-bayyinah"},
    {"number": 99, "name_ar": "الزلزلة", "name_en": "Az-Zalzalah", "ayahs": 8, "type": "مدنية", "slug": "az-zalzala"},
    {"number": 100, "name_ar": "العاديات", "name_en": "Al-Adiyat", "ayahs": 11, "type": "مكية", "slug": "al-adiyat"},
    {"number": 101, "name_ar": "القارعة", "name_en": "Al-Qariah", "ayahs": 11, "type": "مكية", "slug": "al-qariah"},
    {"number": 102, "name_ar": "التكاثر", "name_en": "At-Takathur", "ayahs": 8, "type": "مكية", "slug": "at-takathur"},
    {"number": 103, "name_ar": "العصر", "name_en": "Al-Asr", "ayahs": 3, "type": "مكية", "slug": "al-asr"},
    {"number": 104, "name_ar": "الهمزة", "name_en": "Al-Humazah", "ayahs": 9, "type": "مكية", "slug": "al-humazah"},
    {"number": 105, "name_ar": "الفيل", "name_en": "Al-Fil", "ayahs": 5, "type": "مكية", "slug": "al-fil"},
    {"number": 106, "name_ar": "قريش", "name_en": "Quraysh", "ayahs": 4, "type": "مكية", "slug": "al-quraish"},
    {"number": 107, "name_ar": "الماعون", "name_en": "Al-Maun", "ayahs": 7, "type": "مكية", "slug": "al-maun"},
    {"number": 108, "name_ar": "الكوثر", "name_en": "Al-Kawthar", "ayahs": 3, "type": "مكية", "slug": "al-kauthar"},
    {"number": 109, "name_ar": "الكافرون", "name_en": "Al-Kafirun", "ayahs": 6, "type": "مكية", "slug": "al-kafirun"},
    {"number": 110, "name_ar": "النصر", "name_en": "An-Nasr", "ayahs": 3, "type": "مدنية", "slug": "an-nasr"},
    {"number": 111, "name_ar": "المسد", "name_en": "Al-Masad", "ayahs": 5, "type": "مكية", "slug": "al-masad"},
    {"number": 112, "name_ar": "الإخلاص", "name_en": "Al-Ikhlas", "ayahs": 4, "type": "مكية", "slug": "al-ikhlas"},
    {"number": 113, "name_ar": "الفلق", "name_en": "Al-Falaq", "ayahs": 5, "type": "مكية", "slug": "al-falaq"},
    {"number": 114, "name_ar": "الناس", "name_en": "An-Nas", "ayahs": 6, "type": "مكية", "slug": "an-naas"},
]

# ─── الروابط الأساسية ───────────────────────────────────────────
AUDIO_COLLECTION = "AlBitaqat-Sounds"
PDF_COLLECTION = "al-bitaqat-book-ar_pages"
BOOK_COLLECTION = "al-bitaqat-book"
ARCHIVE_BASE = "https://archive.org/download"

# ─── استثناءات أسماء الملفات (ملفات بأسماء مختلفة عن المعتاد) ──
AUDIO_OVERRIDES = {
    79: {
        "filename": "79 - Output - Stereo Out.mp3",
        "url": f"{ARCHIVE_BASE}/holy-quran-cards/79%20-%20Output%20-%20Stereo%20Out.mp3",
    },
}

# ─── روابط الصفحات ──────────────────────────────────────────────
PAGES = {
    "home": "https://albitaqat.com/",
    "audio_download": "https://albitaqat.com/تحميل-البطاقات-الصوتية-114-بطاقة/",
    "pdf_book": "https://albitaqat.com/كتاب-البطاقات-114-بطاقة-تعريف-pdf/",
    "buy_book": "https://albitaqat.com/buy-albitaqat-book/",
    "youtube_channel": "https://www.youtube.com/@albitaqat",
}


def fetch_archive_filenames():
    """جلب الأسماء الحقيقية لملفات الصوت من archive.org"""
    from html.parser import HTMLParser

    class ArchiveParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.files = []
        def handle_starttag(self, tag, attrs):
            if tag == 'a':
                for name, value in attrs:
                    if name == 'href' and value.endswith('.mp3'):
                        self.files.append(value)

    url = f"{ARCHIVE_BASE}/{AUDIO_COLLECTION}/"
    print(f"📥 جاري جلب أسماء الملفات من {url}...")

    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        print(f"⚠️ فشل جلب الأسماء: {e}")
        return {}

    parser = ArchiveParser()
    parser.feed(resp.text)

    # بناء قاموس: رقم -> اسم الملف
    audio_map = {}
    for f in parser.files:
        num = f[:3]
        decoded = unquote(f)
        audio_map[num] = {
            "encoded": f,
            "decoded": decoded,
        }

    print(f"✅ تم جلب {len(audio_map)} ملف صوتي")
    return audio_map


def fetch_youtube_videos():
    """جلب فيديوهات يوتيوب من قناتها باستخدام yt-dlp"""
    import subprocess
    import shutil

    if not shutil.which("yt-dlp"):
        print("⚠️ yt-dlp غير مثبت، جاري التثبيت...")
        subprocess.check_call(["pip", "install", "yt-dlp", "-q"])

    channel_url = "https://www.youtube.com/@albitaqat/videos"
    try:
        result = subprocess.run(
            ["yt-dlp", "--flat-playlist", "--print", "%(id)s|||%(title)s", channel_url],
            capture_output=True, text=True, timeout=120
        )

        videos = []
        seen_ids = set()

        for line in result.stdout.strip().split("\n"):
            if "|||" not in line:
                continue
            video_id, title = line.split("|||", 1)
            video_id = video_id.strip()
            title = title.strip()

            if video_id in seen_ids:
                continue
            seen_ids.add(video_id)

            card_num = None
            m = re.search(r'البطاقة\s*[\(]?\s*(\d+)\s*[\)]?', title)
            if m:
                card_num = int(m.group(1))

            videos.append({
                "video_id": video_id,
                "title": title,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "thumbnail": f"https://i2.ytimg.com/vi/{video_id}/hqdefault.jpg",
                "card_number": card_num,
            })

        return videos
    except Exception as e:
        print(f"⚠️ فشل جلب فيديوهات يوتيوب: {e}")
        return []


def generate_all_data(youtube_videos, audio_map):
    """إنشاء البيانات الشاملة"""
    yt_map = {}
    for v in youtube_videos:
        card_num = v.get("card_number")
        if card_num and 1 <= card_num <= 114:
            if card_num in yt_map:
                existing_title = yt_map[card_num]["title"].lower()
                new_title = v["title"].lower()
                if "شرح" in new_title and "شرح" not in existing_title:
                    yt_map[card_num] = v
                elif "محاضرة" in new_title and "محاضرة" not in existing_title:
                    yt_map[card_num] = v
            else:
                yt_map[card_num] = v

    all_data = []
    for surah in SURAH_DATA:
        num = surah["number"]
        num_str = f"{num:03d}"

        # استخدام الاسم الحقيقي من archive.org
        audio_filename = f"{num_str}_{surah['name_en']}.mp3"
        audio_url = f"{ARCHIVE_BASE}/{AUDIO_COLLECTION}/{audio_filename}"

        # التحقق من وجود استثناء
        if num in AUDIO_OVERRIDES:
            audio_filename = AUDIO_OVERRIDES[num]["filename"]
            audio_url = AUDIO_OVERRIDES[num]["url"]
        elif num_str in audio_map:
            audio_filename = audio_map[num_str]["decoded"]
            audio_url = f"{ARCHIVE_BASE}/{AUDIO_COLLECTION}/{audio_map[num_str]['encoded']}"

        surah_entry = {
            "number": num,
            "name_arabic": surah["name_ar"],
            "name_english": surah["name_en"],
            "ayahs_count": surah["ayahs"],
            "revelation_type": surah["type"],
            "slug": surah["slug"],
            "page_url": f"https://albitaqat.com/{surah['slug']}/",
            "downloads": {
                "audio": {
                    "filename": audio_filename,
                    "url": audio_url,
                },
                "pdf": {
                    "filename": f"AlBitaqat-Book-ar_{num_str}.pdf",
                    "url": f"{ARCHIVE_BASE}/{PDF_COLLECTION}/AlBitaqat-Book-ar_{num_str}.pdf",
                },
                "youtube_video": None,
            },
        }

        if num in yt_map:
            surah_entry["downloads"]["youtube_video"] = {
                "video_id": yt_map[num]["video_id"],
                "title": yt_map[num]["title"],
                "url": yt_map[num]["url"],
                "thumbnail": yt_map[num]["thumbnail"],
            }

        all_data.append(surah_entry)

    return all_data


def generate_audio_links(audio_map):
    """روابط الصوت"""
    links = []
    for s in SURAH_DATA:
        num_str = f"{s['number']:03d}"
        audio_filename = f"{num_str}_{s['name_en']}.mp3"
        audio_url = f"{ARCHIVE_BASE}/{AUDIO_COLLECTION}/{audio_filename}"

        # التحقق من وجود استثناء
        if s["number"] in AUDIO_OVERRIDES:
            audio_filename = AUDIO_OVERRIDES[s["number"]]["filename"]
            audio_url = AUDIO_OVERRIDES[s["number"]]["url"]
        elif num_str in audio_map:
            audio_filename = audio_map[num_str]["decoded"]
            audio_url = f"{ARCHIVE_BASE}/{AUDIO_COLLECTION}/{audio_map[num_str]['encoded']}"

        links.append({
            "surah_number": s["number"],
            "surah_name_arabic": s["name_ar"],
            "surah_name_english": s["name_en"],
            "filename": audio_filename,
            "url": audio_url,
        })
    return links


def generate_pdf_links():
    """روابط PDF"""
    links = []
    for s in SURAH_DATA:
        num_str = f"{s['number']:03d}"
        filename = f"AlBitaqat-Book-ar_{num_str}.pdf"
        links.append({
            "surah_number": s["number"],
            "surah_name_arabic": s["name_ar"],
            "surah_name_english": s["name_en"],
            "filename": filename,
            "url": f"{ARCHIVE_BASE}/{PDF_COLLECTION}/{filename}",
        })
    return links


def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ {filename}")


if __name__ == "__main__":
    print("=" * 60)
    print("🕌 إنشاء ملفات بيانات بطاقات القرآن الكريم")
    print("=" * 60)

    # جلب الأسماء الحقيقية من archive.org
    audio_map = fetch_archive_filenames()

    # جلب فيديوهات يوتيوب
    print("\n📥 جاري جلب فيديوهات يوتيوب...")
    yt_videos = fetch_youtube_videos()
    print(f"✅ تم جلب {len(yt_videos)} فيديو من يوتيوب")

    # 1. الملف الشامل
    all_data = generate_all_data(yt_videos, audio_map)
    save_json({
        "source": "https://albitaqat.com/",
        "project": "بطاقات القرآن الكريم",
        "author": "أ.د. ياسر بن إسماعيل راضي",
        "total_surahs": len(all_data),
        "pages": PAGES,
        "archive_collections": {
            "audio": f"{ARCHIVE_BASE}/{AUDIO_COLLECTION}",
            "book_pdf": f"{ARCHIVE_BASE}/{BOOK_COLLECTION}/AlBitaqat-Book-ar.pdf",
            "individual_pdfs": f"{ARCHIVE_BASE}/{PDF_COLLECTION}",
        },
        "surahs": all_data,
    }, "quran_cards_full.json")

    # 2. ملف الصوت
    audio_links = generate_audio_links(audio_map)
    save_json({
        "type": "audio",
        "format": "MP3",
        "source": "https://albitaqat.com/",
        "archive_collection": f"{ARCHIVE_BASE}/{AUDIO_COLLECTION}",
        "bulk_download": f"{ARCHIVE_BASE}/{AUDIO_COLLECTION}/AlBitaqatAudio.rar",
        "total_files": len(audio_links),
        "files": audio_links,
    }, "audio_links.json")

    # 3. ملف PDF
    pdf_links = generate_pdf_links()
    save_json({
        "type": "pdf",
        "format": "PDF",
        "source": "https://albitaqat.com/",
        "archive_collection": f"{ARCHIVE_BASE}/{PDF_COLLECTION}",
        "bulk_download": f"{ARCHIVE_BASE}/{BOOK_COLLECTION}/AlBitaqat-Book-ar.pdf",
        "total_files": len(pdf_links),
        "files": pdf_links,
    }, "pdf_links.json")

    # 4. ملف صفحة التحميل الصوتي
    save_json({
        "page_title": "تحميل البطاقات الصوتية 114 بطاقة تعريف بسور القرآن الكريم mp3",
        "page_url": PAGES["audio_download"],
        "project": "بطاقات القرآن الكريم",
        "book_info": {
            "author": "أ.د. ياسر بن إسماعيل راضي",
            "recording_studio": "استديو وقف تعظيم الوحيين (صدى المنورة) بالمدينة المنورة",
            "text_reader": "الدكتور محمد الشاذلي (مذيع في قناة السنة النبوية بالمدينة المنورة)",
            "quran_reader": "الحافظ: أنس بن ياسر",
            "sound_engineer": "سيد مصطفى",
            "file_size_mb": 293.14,
            "total_files": 114,
        },
        "bulk_download": {
            "filename": "AlBitaqatAudio.rar",
            "url": f"{ARCHIVE_BASE}/{AUDIO_COLLECTION}/AlBitaqatAudio.rar",
            "size_mb": 293.14,
            "format": "RAR",
        },
        "social_links": {
            "website": "https://albitaqat.com",
            "facebook": "https://www.facebook.com/Albitaqat",
            "telegram": "https://t.me/albitaqatt",
            "youtube": PAGES["youtube_channel"],
        },
    }, "audio_download_page.json")

    # 5. ملف صفحة كتاب PDF
    save_json({
        "page_title": "تحميل كتاب البطاقات 114 بطاقة تعريف بسور القرآن الكريم Pdf",
        "page_url": PAGES["pdf_book"],
        "project": "بطاقات القرآن الكريم",
        "book_info": {
            "author": "أ.د. ياسر بن إسماعيل راضي",
            "publisher": "دار الميمنة",
            "publish_year": "1441",
            "isbn": "9786030350469",
            "file_size_mb": 17.12,
            "format": "غلاف ورق شمواه",
            "pages_count": 135,
        },
        "bulk_download": {
            "filename": "AlBitaqat-Book-ar.pdf",
            "url": f"{ARCHIVE_BASE}/{BOOK_COLLECTION}/AlBitaqat-Book-ar.pdf",
            "size_mb": 17.12,
            "format": "PDF",
        },
        "social_links": {
            "website": "https://albitaqat.com",
            "facebook": "https://www.facebook.com/Albitaqat",
            "telegram": "https://t.me/albitaqatt",
            "youtube": PAGES["youtube_channel"],
        },
    }, "pdf_book_page.json")

    # 6. ملف فيديوهات يوتيوب
    save_json({
        "channel": PAGES["youtube_channel"],
        "total_videos": len(yt_videos),
        "surahs_with_video": len([v for v in yt_videos if v.get("card_number")]),
        "videos": yt_videos,
    }, "youtube_videos.json")

    print("\n" + "=" * 60)
    print("📊 ملخص الملفات:")
    print(f"   📄 quran_cards_full.json   - بيانات شاملة لـ {len(all_data)} سورة")
    print(f"   🔊 audio_links.json        - روابط صوت {len(audio_links)} ملف")
    print(f"   📄 pdf_links.json          - روابط PDF {len(pdf_links)} ملف")
    print(f"   📖 audio_download_page.json - صفحة التحميل الصوتي")
    print(f"   📖 pdf_book_page.json       - صفحة كتاب PDF")
    print(f"   🎬 youtube_videos.json     - {len(yt_videos)} فيديو يوتيوب")
    print("=" * 60)
