#!/usr/bin/env python3
"""
النقطة الرئيسية لمشروع بطاقات القرآن الكريم
يقوم بتشغيل scraper و generate_links
"""

import sys
from pathlib import Path

# إضافة المسارات
sys.path.insert(0, str(Path(__file__).parent / "scripts"))
sys.path.insert(0, str(Path(__file__).parent / "src"))


def main():
    """الدالة الرئيسية"""
    print("=" * 60)
    print("🕌 مشروع بطاقات القرآن الكريم")
    print("=" * 60)

    # تشغيل المكشط
    print("\n📥 تشغيل مكشط البيانات...")
    from scraper import scrape_all_surahs, save_results
    surahs = scrape_all_surahs()
    save_results(surahs)

    # تشغيل إنشاء الروابط
    print("\n📥 تشغيل إنشاء الروابط...")
    from generate_links import (
        fetch_youtube_videos, generate_all_data, generate_audio_links,
        generate_pdf_links, save_json, SURAH_DATA, PAGES, ARCHIVE_BASE,
        AUDIO_COLLECTION, PDF_COLLECTION, BOOK_COLLECTION
    )

    yt_videos = fetch_youtube_videos()
    all_data = generate_all_data(yt_videos)

    # حفظ الملفات
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
    }, "data/quran_cards_full.json")

    audio_links = generate_audio_links()
    save_json({
        "type": "audio",
        "format": "MP3",
        "source": "https://albitaqat.com/",
        "archive_collection": f"{ARCHIVE_BASE}/{AUDIO_COLLECTION}",
        "bulk_download": f"{ARCHIVE_BASE}/{AUDIO_COLLECTION}/AlBitaqatAudio.rar",
        "total_files": len(audio_links),
        "files": audio_links,
    }, "data/audio_links.json")

    pdf_links = generate_pdf_links()
    save_json({
        "type": "pdf",
        "format": "PDF",
        "source": "https://albitaqat.com/",
        "archive_collection": f"{ARCHIVE_BASE}/{PDF_COLLECTION}",
        "bulk_download": f"{ARCHIVE_BASE}/{BOOK_COLLECTION}/AlBitaqat-Book-ar.pdf",
        "total_files": len(pdf_links),
        "files": pdf_links,
    }, "data/pdf_links.json")

    save_json({
        "channel": PAGES["youtube_channel"],
        "playlist": PAGES["youtube_playlist"],
        "total_videos": len(yt_videos),
        "surahs_with_video": len([v for v in yt_videos if v.get("card_number")]),
        "videos": yt_videos,
    }, "data/youtube_videos.json")

    print("\n" + "=" * 60)
    print("✅ اكتمل بنجاح!")
    print("=" * 60)


if __name__ == "__main__":
    main()
