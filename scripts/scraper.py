#!/usr/bin/env python3
"""
مكشط بيانات بطاقات القرآن الكريم من موقع albitaqat.com
يقوم باستخراج بيانات جميع السور الـ 114 مع روابط الوسائط المتعددة
"""

import json
import re
import time
import sys
from urllib.parse import urljoin

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("جاري تثبيت المكتبات المطلوبة...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4", "-q"])
    import requests
    from bs4 import BeautifulSoup

BASE_URL = "https://albitaqat.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "ar,en;q=0.9",
}

# بيانات السور الأساسية من القرآن الكريم
SURAH_INFO = [
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


def get_page(url, retries=3):
    """جلب صفحة مع إعادة المحاولة"""
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            if attempt < retries - 1:
                print(f"  ⚠️  خطأ في الاتصال، المحاولة {attempt + 1}/{retries}...")
                time.sleep(2 * (attempt + 1))
            else:
                print(f"  ❌ فشل الاتصال بـ {url}: {e}")
                return None


def extract_surah_links(html):
    """استخراج روابط السور من الصفحة الرئيسية"""
    soup = BeautifulSoup(html, "html.parser")
    links = []

    # البحث عن روابط السور في قائمة البطاقات
    gallery = soup.find("ul", class_="news-gallery-items")
    if gallery:
        for li in gallery.find_all("li"):
            a = li.find("a", href=True)
            if a:
                href = a["href"]
                # استخراج صورة الخلفية
                style = a.get("style", "")
                bg_match = re.search(r"url\(['\"]?(.*?)['\"]?\)", style)
                thumbnail = bg_match.group(1) if bg_match else None
                links.append({"slug": href.strip("/"), "thumbnail": thumbnail})

    return links


def extract_card_data(soup):
    """استخراج بيانات البطاقة من الصفحة"""
    data = {}

    # البحث عن حاوية تفاصيل السورة
    details = soup.find("div", class_="suraDetails") or soup.find("div", id="suraDetails")
    if not details:
        # بديل: البحث عن جميع عناصر card-item
        details = soup.find("div", class_=re.compile(r"card|sura|detail"))

    if not details:
        return data

    # استخراج العناصر
    card_items = details.find_all("div", class_=re.compile(r"card-item"))
    section_keys = [
        "ayahs_count",
        "name_meaning",
        "name_reason",
        "other_names",
        "general_purpose",
        "revelation_reason",
        "virtue",
        "occasions",
    ]
    section_labels = [
        "آياتها",
        "معنى اسمها",
        "سبب تسميتها",
        "أسماؤها",
        "مقصدها العام",
        "سبب نزولها",
        "فضلها",
        "مناسباتها",
    ]

    for i, item in enumerate(card_items):
        if i < len(section_keys):
            # استخراج العنوان
            title_el = item.find(["h3", "h4", "span", "div"], class_=re.compile(r"title|heading"))
            title = title_el.get_text(strip=True) if title_el else section_labels[i]

            # استخراج المحتوى
            content_el = item.find(["p", "div"], class_=re.compile(r"content|text|body"))
            if not content_el:
                content_el = item.find(["p", "div"])
            content = content_el.get_text(strip=True) if content_el else item.get_text(strip=True)

            # تنظيف المحتوى من عنوان العنصر
            if title and content.startswith(title):
                content = content[len(title):].strip()

            data[section_keys[i]] = {
                "title": title,
                "content": content,
            }

    return data


def extract_media_urls(soup, surah_url):
    """استخراج روابط الوسائط"""
    media = {"audio": None, "pdf": None, "video_url": None, "image": None}

    # استخراج رابط الصوت
    audio_tag = soup.find("audio")
    if audio_tag:
        source = audio_tag.find("source")
        if source and source.get("src"):
            media["audio"] = urljoin(surah_url, source["src"].split("?")[0])
        elif audio_tag.get("src"):
            media["audio"] = urljoin(surah_url, audio_tag["src"].split("?")[0])

    # استخراج رابط PDF
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if ".pdf" in href.lower():
            media["pdf"] = urljoin(surah_url, href)
            break

    # استخراج رابط الفيديو
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "video" in href.lower():
            media["video_url"] = urljoin(surah_url, href)
            break

    # استخراج صورة البطاقة الكبيرة
    og_image = soup.find("meta", property="og:image")
    if og_image and og_image.get("content"):
        media["image"] = og_image["content"]

    return media


def scrape_surah(surah_info, slug_from_homepage=None):
    """مكشط بيانات سورة واحدة"""
    slug = slug_from_homepage or surah_info["slug"]
    url = f"{BASE_URL}{slug}/"

    print(f"  📖 جاري استخراج بيانات سورة {surah_info['name_ar']}...", end=" ")

    html = get_page(url)
    if not html:
        print("❌ فشل")
        return None

    soup = BeautifulSoup(html, "html.parser")

    # استخراج البيانات
    card_data = extract_card_data(soup)
    media = extract_media_urls(soup, url)

    # استخراج العنوان من الصفحة
    title_tag = soup.find("title")
    page_title = title_tag.get_text(strip=True) if title_tag else ""

    # استخراج الوصف
    desc_tag = soup.find("meta", attrs={"name": "description"})
    description = desc_tag["content"] if desc_tag else ""

    surah_data = {
        "number": surah_info["number"],
        "name_arabic": surah_info["name_ar"],
        "name_english": surah_info["name_en"],
        "ayahs_count": surah_info["ayahs"],
        "revelation_type": surah_info["type"],
        "url": url,
        "slug": slug,
        "page_title": page_title,
        "description": description,
        "card_data": card_data,
        "media": media,
    }

    print("✅")
    return surah_data


def scrape_all():
    """مكشط جميع السور"""
    print("=" * 60)
    print("🕌 مكشط بيانات بطاقات القرآن الكريم")
    print(f"🌐 الموقع: {BASE_URL}")
    print("=" * 60)

    # جلب الصفحة الرئيسية
    print("\n📥 جاري جلب الصفحة الرئيسية...")
    home_html = get_page(BASE_URL)
    if not home_html:
        print("❌ فشل في جلب الصفحة الرئيسية")
        return None

    # استخراج روابط السور من الصفحة الرئيسية (المصدر الأ信赖)
    homepage_links = extract_surah_links(home_html)
    print(f"✅ تم العثور على {len(homepage_links)} سورة في الصفحة الرئيسية")

    # استخراج بيانات كل سورة باستخدام الروابط من الصفحة الرئيسية
    all_surahs = []
    failed = []

    print("\n🔄 جاري استخراج بيانات السور...")
    for i, link in enumerate(homepage_links):
        slug = link["slug"]

        # مطابقة السورة مع البيانات الأساسية
        surah_info = None
        for s in SURAH_INFO:
            if s["slug"] == slug:
                surah_info = s
                break

        if not surah_info:
            # إذا لم تُعثر على المطابقة، نستخدم بيانات افتراضية
            surah_info = {
                "number": i + 1,
                "name_ar": f"سورة {i + 1}",
                "name_en": slug,
                "ayahs": 0,
                "type": "غير محدد",
                "slug": slug,
            }

        print(f"\n[{i+1}/114]", end="")
        result = scrape_surah(surah_info, slug)
        if result:
            all_surahs.append(result)
        else:
            failed.append(surah_info["name_en"])

        # تجنب الحظر
        if i < len(homepage_links) - 1:
            time.sleep(1)

    print("\n" + "=" * 60)
    print(f"📊 النتائج: {len(all_surahs)} سورة تم استخراجها بنجاح")
    if failed:
        print(f"❌ فشل استخراج {len(failed)} سورة: {', '.join(failed)}")
    print("=" * 60)

    return all_surahs


def fetch_youtube_videos():
    """جلب فيديوهات يوتيوب من قناتها باستخدام yt-dlp"""
    import subprocess
    import shutil
    import re

    # التحقق من وجود yt-dlp
    if not shutil.which("yt-dlp"):
        print("⚠️ yt-dlp غير مثبت، جاري التثبيت...")
        subprocess.check_call(["pip", "install", "yt-dlp", "-q"])

    channel_url = "https://www.youtube.com/@albitaqat/videos"
    try:
        print("\n📥 جاري جلب فيديوهات يوتيوب...")
        result = subprocess.run(
            ["yt-dlp", "--flat-playlist", "--print", "%(id)s|||%(title)s", channel_url],
            capture_output=True, text=True, timeout=120
        )

        yt_map = {}
        seen = {}

        for line in result.stdout.strip().split("\n"):
            if "|||" not in line:
                continue
            video_id, title = line.split("|||", 1)
            video_id = video_id.strip()
            title = title.strip()

            # استخراج رقم البطاقة من العنوان
            match = re.search(r'(?:ال)?بطاقة\s*[\(]?\s*(\d+)\s*[\)]?', title)
            if match:
                card_num = int(match.group(1))
                if 1 <= card_num <= 114:
                    # إذا كانت البطاقة لها أكثر من فيديو، ن prefer "شرح"
                    if card_num in seen:
                        existing_title = seen[card_num]["title"].lower()
                        if "شرح" in title.lower() and "شرح" not in existing_title:
                            yt_map[card_num] = {
                                "video_id": video_id,
                                "title": title,
                                "url": f"https://www.youtube.com/watch?v={video_id}",
                            }
                            seen[card_num] = {"title": title}
                    else:
                        yt_map[card_num] = {
                            "video_id": video_id,
                            "title": title,
                            "url": f"https://www.youtube.com/watch?v={video_id}",
                        }
                        seen[card_num] = {"title": title}

        print(f"✅ تم جلب {len(yt_map)} فيديو من يوتيوب")
        return yt_map
    except Exception as e:
        print(f"⚠️ خطأ في جلب فيديوهات يوتيوب: {e}")
        return {}


def save_results(data, filename="quran_cards.json"):
    """حفظ النتائج في ملف JSON"""
    # جلب فيديوهات يوتيوب
    yt_map = fetch_youtube_videos()

    # إضافة روابط يوتيوب لكل سورة داخل media
    for surah in data:
        num = surah.get("number")
        if "media" not in surah:
            surah["media"] = {}
        if num in yt_map:
            surah["media"]["youtube_url"] = yt_map[num]["url"]
            surah["media"]["youtube_title"] = yt_map[num]["title"]
            surah["media"]["youtube_video_id"] = yt_map[num]["video_id"]
        else:
            surah["media"]["youtube_url"] = None
            surah["media"]["youtube_title"] = None
            surah["media"]["youtube_video_id"] = None

    output = {
        "source": "https://albitaqat.com/",
        "project": "بطاقات القرآن الكريم",
        "author": "الدكتور ياسر بن إسماعيل راضي",
        "youtube_channel": "https://www.youtube.com/@albitaqat",
        "total_surahs": len(data),
        "surahs": data,
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n💾 تم حفظ البيانات في: {filename}")


if __name__ == "__main__":
    data = scrape_all()
    if data:
        save_results(data)
        print("\n✅ اكتمل الاستخراج بنجاح!")
    else:
        print("\n❌ فشل الاستخراج")
