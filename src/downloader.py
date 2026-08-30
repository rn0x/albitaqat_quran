#!/usr/bin/env python3
"""
سكربت تحميل ملفات بطاقات القرآن الكريم محلياً
يدعم التحميل من ملفات JSON المنشأة وروابط archive.org
"""

import json
import os
import sys
import time
import hashlib
from pathlib import Path

try:
    import requests
except ImportError:
    print("جاري تثبيت requests...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests

BASE_DIR = Path("quran_data")
AUDIO_DIR = BASE_DIR / "audio"
PDF_DIR = BASE_DIR / "pdf"
IMAGES_DIR = BASE_DIR / "images"
YOUTUBE_DIR = BASE_DIR / "youtube"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}

RETRY_COUNT = 3


def create_dirs():
    """إنشاء مجلدات التخزين"""
    for d in [AUDIO_DIR, PDF_DIR, IMAGES_DIR, YOUTUBE_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def download_file(url, dest, retries=RETRY_COUNT):
    """تحميل ملف مع إعادة المحاولة"""
    if not url:
        return False, "لا يوجد رابط"

    filename = dest.name
    if dest.exists():
        return True, "موجود مسبقاً"

    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=120, stream=True)
            response.raise_for_status()

            dest.parent.mkdir(parents=True, exist_ok=True)
            with open(dest, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return True, "تم التحميل"
        except requests.RequestException as e:
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
            else:
                return False, f"خطأ: {e}"

    return False, "فشل بعد إعادة المحاولة"


def download_youtube_video(video_id, dest_dir, filename=None):
    """تحميل فيديو يوتيوب باستخدام yt-dlp"""
    import subprocess
    import shutil

    if not shutil.which("yt-dlp"):
        print("⚠️ yt-dlp غير مثبت، جاري التثبيت...")
        subprocess.check_call(["pip", "install", "yt-dlp", "-q"])

    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    url = f"https://www.youtube.com/watch?v={video_id}"

    if filename:
        output_template = str(dest_dir / f"{filename}.%(ext)s")
    else:
        output_template = str(dest_dir / "%(title)s.%(ext)s")

    try:
        # استخدام node كـ JavaScript runtime
        result = subprocess.run(
            [
                "yt-dlp",
                "--js-runtimes", "node",
                "--merge-output-format", "mp4",
                "--no-playlist",
                "-o", output_template,
                "--no-overwrites",
                url,
            ],
            capture_output=True, text=True, timeout=300
        )

        if result.returncode == 0:
            return True, "تم التحميل"
        else:
            return False, result.stderr[:200] if result.stderr else "خطأ غير معروف"
    except subprocess.TimeoutExpired:
        return False, "انتهت المهلة"
    except Exception as e:
        return False, str(e)


def format_size(size_bytes):
    """تنسيق حجم الملف"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def download_from_full_json(json_file="quran_cards_full.json", audio=True, pdf=True, images=True, youtube=False):
    """التحميل من الملف الشامل"""
    if not os.path.exists(json_file):
        print(f"❌ ملف {json_file} غير موجود. قم أولاً بتشغيل generate_links.py")
        return None

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    surahs = data.get("surahs", [])
    print(f"📊 تم العثور على {len(surahs)} سورة")

    create_dirs()
    stats = {"audio": [0, 0], "pdf": [0, 0], "image": [0, 0], "youtube": [0, 0]}  # [success, failed]

    for i, surah in enumerate(surahs):
        num = surah["number"]
        name_ar = surah["name_arabic"]
        name_en = surah["name_english"]
        num_str = f"{num:03d}"

        print(f"[{i+1}/114] 📖 {name_ar} ({name_en})", end="")

        downloads = surah.get("downloads", {})

        # تحميل الصوت
        if audio and downloads.get("audio", {}).get("url"):
            audio_url = downloads["audio"]["url"]
            audio_dest = AUDIO_DIR / f"{num_str}_{name_en}.mp3"
            success, _ = download_file(audio_url, audio_dest)
            stats["audio"][0 if success else 1] += 1

        # تحميل PDF
        if pdf and downloads.get("pdf", {}).get("url"):
            pdf_url = downloads["pdf"]["url"]
            pdf_dest = PDF_DIR / f"{num_str}_{name_en}.pdf"
            success, _ = download_file(pdf_url, pdf_dest)
            stats["pdf"][0 if success else 1] += 1

        # تحميل الصورة
        if images and downloads.get("image", {}).get("url"):
            img_url = downloads["image"]["url"]
            img_dest = IMAGES_DIR / f"{num_str}_{name_en}.jpg"
            success, _ = download_file(img_url, img_dest)
            stats["image"][0 if success else 1] += 1

        # تحميل فيديو يوتيوب
        if youtube and downloads.get("youtube_video", {}).get("video_id"):
            video_id = downloads["youtube_video"]["video_id"]
            yt_dest = YOUTUBE_DIR / f"{num_str}_{name_en}"
            success, _ = download_youtube_video(video_id, yt_dest)
            stats["youtube"][0 if success else 1] += 1

        print(" ✅")

    print_stats(stats)
    return stats


def download_from_links_json(json_file="audio_links.json", dest_dir=None):
    """التحميل من ملف روابط"""
    if not os.path.exists(json_file):
        print(f"❌ ملف {json_file} غير موجود")
        return None

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    files = data.get("files", [])
    file_type = data.get("type", "unknown")

    if dest_dir is None:
        dest_dir = BASE_DIR / file_type
    else:
        dest_dir = Path(dest_dir)

    dest_dir.mkdir(parents=True, exist_ok=True)

    print(f"📊 تم العثور على {len(files)} ملف {file_type}")
    print(f"📁 مجلد الحفظ: {dest_dir}")

    success_count = 0
    failed_count = 0

    for i, file_info in enumerate(files):
        name_ar = file_info.get("surah_name_arabic", "")
        name_en = file_info.get("surah_name_english", "")
        url = file_info.get("url", "")
        filename = file_info.get("filename", f"{name_en}.mp3")

        print(f"[{i+1}/{len(files)}] 📖 {name_ar} ({name_en})", end="")

        dest = dest_dir / filename
        success, _ = download_file(url, dest)

        if success:
            success_count += 1
            print(" ✅")
        else:
            failed_count += 1
            print(" ❌")

    print(f"\n📊 النتائج: {success_count} تم التحميل | {failed_count} فشل")
    return {"success": success_count, "failed": failed_count}


def download_bulk(type="audio"):
    """التحميل الجماعي من archive.org"""
    bulk_urls = {
        "audio": "https://archive.org/download/al-bitaqat-audio-ar/AlBitaqatAudio.rar",
        "pdf": "https://archive.org/download/al-bitaqat-book/AlBitaqat-Book-ar.pdf",
    }

    if type not in bulk_urls:
        print(f"❌ نوع غير مدعوم: {type}")
        return

    url = bulk_urls[type]
    dest = BASE_DIR / f"bulk_{type}{'_rar' if type == 'audio' else '.pdf'}"

    print(f"📥 جاري تحميل الملف الجماعي...")
    print(f"   🔗 {url}")
    print(f"   📁 {dest}")

    create_dirs()
    success, msg = download_file(url, dest)
    if success:
        print(f"✅ {msg}")
    else:
        print(f"❌ {msg}")


def verify_downloads(json_file="quran_cards_full.json"):
    """التحقق من سلامة التحميل"""
    if not os.path.exists(json_file):
        print(f"❌ ملف {json_file} غير موجود")
        return

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    surahs = data.get("surahs", [])
    print("🔍 جاري التحقق من الملفات المحملة...\n")

    missing = {"audio": [], "pdf": [], "image": []}

    for surah in surahs:
        num_str = f"{surah['number']:03d}"
        name_en = surah["name_english"]

        if not (AUDIO_DIR / f"{num_str}_{name_en}.mp3").exists():
            missing["audio"].append(f"{surah['name_arabic']} ({name_en})")
        if not (PDF_DIR / f"{num_str}_{name_en}.pdf").exists():
            missing["pdf"].append(f"{surah['name_arabic']} ({name_en})")
        if not (IMAGES_DIR / f"{num_str}_{name_en}.jpg").exists():
            missing["image"].append(f"{surah['name_arabic']} ({name_en})")

    for media_type, items in missing.items():
        if items:
            print(f"❌ ملفات {media_type} مفقودة ({len(items)}):")
            for name in items[:5]:
                print(f"   - {name}")
            if len(items) > 5:
                print(f"   ... و {len(items) - 5} أخرى")

    if not any(missing.values()):
        print("✅ جميع الملفات متوفرة ومحمّلة بنجاح!")

    return {k: len(v) for k, v in missing.items()}


def print_stats(stats):
    """طباعة الإحصائيات"""
    print("\n" + "=" * 60)
    print("📊 إحصائيات التحميل:")
    for media_type, (success, failed) in stats.items():
        emoji = {"audio": "🔊", "pdf": "📄", "image": "🖼️", "youtube": "🎬"}.get(media_type, "📁")
        print(f"   {emoji} {media_type}: {success} تم | {failed} فشل")
    print("=" * 60)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="تحميل ملفات بطاقات القرآن الكريم")
    parser.add_argument("--mode", choices=["full", "audio", "pdf", "images", "youtube", "bulk", "verify"],
                        default="full", help="وضع التحميل")
    parser.add_argument("--json", default=None, help="مسار ملف JSON")
    parser.add_argument("--bulk-type", choices=["audio", "pdf"], default="audio",
                        help="نوع الملف الجماعي")
    parser.add_argument("--no-audio", action="store_true", help="تخطي تحميل الصوت")
    parser.add_argument("--no-pdf", action="store_true", help="تخطي تحميل PDF")
    parser.add_argument("--no-images", action="store_true", help="تخطي تحميل الصور")
    parser.add_argument("--with-youtube", action="store_true", help="تحميل فيديوهات يوتيوب مع الملفات")

    args = parser.parse_args()

    if args.mode == "full":
        json_file = args.json or "quran_cards_full.json"
        download_from_full_json(
            json_file,
            audio=not args.no_audio,
            pdf=not args.no_pdf,
            images=not args.no_images,
            youtube=args.with_youtube,
        )
    elif args.mode == "audio":
        json_file = args.json or "audio_links.json"
        download_from_links_json(json_file)
    elif args.mode == "pdf":
        json_file = args.json or "pdf_links.json"
        download_from_links_json(json_file)
    elif args.mode == "images":
        json_file = args.json or "image_links.json"
        download_from_links_json(json_file)
    elif args.mode == "youtube":
        json_file = args.json or "quran_cards_full.json"
        download_from_full_json(json_file, audio=False, pdf=False, images=False, youtube=True)
    elif args.mode == "bulk":
        download_bulk(args.bulk_type)
    elif args.mode == "verify":
        json_file = args.json or "quran_cards_full.json"
        verify_downloads(json_file)
