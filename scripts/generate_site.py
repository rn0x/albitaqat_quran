#!/usr/bin/env python3
"""
Generate data.js for the website from JSON data files.
This script reads the JSON data and creates a JavaScript file
that can be used by the website.
"""

import json
import os
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'data'
WEB_DIR = PROJECT_ROOT / 'web'
OUTPUT_FILE = WEB_DIR / 'js' / 'data.js'

def load_json(filepath):
    """Load JSON file and return data."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_data_js():
    """Generate data.js from JSON files."""
    
    # Load data
    print("Loading data files...")
    quran_cards = load_json(DATA_DIR / 'quran_cards_full.json')
    audio_links = load_json(DATA_DIR / 'audio_links.json')
    pdf_links = load_json(DATA_DIR / 'pdf_links.json')
    youtube_videos = load_json(DATA_DIR / 'youtube_videos.json')
    
    # Extract surahs
    surahs = quran_cards.get('surahs', [])
    
    # Count stats
    total_surahs = len(surahs)
    total_ayahs = sum(s.get('ayahs_count', 0) for s in surahs)
    meccan_count = sum(1 for s in surahs if s.get('revelation_type') == 'مكية')
    medinan_count = sum(1 for s in surahs if s.get('revelation_type') == 'مدنية')
    total_videos = len(youtube_videos)
    
    # Generate JS content
    pages_json = json.dumps(quran_cards.get('pages', {}), ensure_ascii=False, indent=2)
    collections_json = json.dumps(quran_cards.get('archive_collections', {}), ensure_ascii=False, indent=2)
    surahs_json = json.dumps(surahs, ensure_ascii=False, indent=2)
    audio_json = json.dumps(audio_links, ensure_ascii=False, indent=2)
    pdf_json = json.dumps(pdf_links, ensure_ascii=False, indent=2)
    youtube_json = json.dumps(youtube_videos, ensure_ascii=False, indent=2)
    
    js_content = f"""// ========================================
// Auto-generated data file
// Generated from: quran_cards_full.json
// ========================================

const PROJECT_DATA = {{
  source: "{quran_cards.get('source', '')}",
  project: "{quran_cards.get('project', '')}",
  author: "{quran_cards.get('author', '')}",
  total_surahs: {total_surahs},
  total_ayahs: {total_ayahs},
  meccan_surahs: {meccan_count},
  medinan_surahs: {medinan_count},
  total_videos: {total_videos},
  pages: {pages_json},
  archive_collections: {collections_json}
}};

const SURAHS_DATA = {surahs_json};

const AUDIO_LINKS = {audio_json};

const PDF_LINKS = {pdf_json};

const YOUTUBE_VIDEOS = {youtube_json};

// Make data available globally
if (typeof window !== 'undefined') {{
  window.surahsData = SURAHS_DATA;
  window.projectData = PROJECT_DATA;
  window.audioLinks = AUDIO_LINKS;
  window.pdfLinks = PDF_LINKS;
  window.youtubeVideos = YOUTUBE_VIDEOS;
}}
"""
    
    # Write output
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"✅ Generated {OUTPUT_FILE}")
    print(f"   - {total_surahs} surahs")
    print(f"   - {total_ayahs} ayahs")
    print(f"   - {meccan_count} Meccan, {medinan_count} Medinan")
    print(f"   - {total_videos} YouTube videos")

if __name__ == '__main__':
    generate_data_js()
