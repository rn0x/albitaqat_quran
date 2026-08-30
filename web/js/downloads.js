/* ========================================
   Downloads Counter - GitHub API
   Fetches download counts for release assets
   ======================================== */

const GITHUB_OWNER = 'rn0x';
const GITHUB_REPO = 'albitaqat_quran';
const RELEASE_TAG = 'v1.0.0';

// File name to element ID mapping
const FILE_MAP = {
  'quran_cards.json': 'dl-quran_cards',
  'quran_cards_full.json': 'dl-quran_cards_full',
  'audio_links.json': 'dl-audio_links',
  'pdf_links.json': 'dl-pdf_links',
  'youtube_videos.json': 'dl-youtube_videos'
};

// Cache download counts in localStorage
const CACHE_KEY = 'albitaqat_downloads';
const CACHE_DURATION = 30 * 60 * 1000; // 30 minutes

function getCachedCounts() {
  try {
    const cached = localStorage.getItem(CACHE_KEY);
    if (cached) {
      const { data, timestamp } = JSON.parse(cached);
      if (Date.now() - timestamp < CACHE_DURATION) {
        return data;
      }
    }
  } catch (e) {
    // Ignore cache errors
  }
  return null;
}

function setCachedCounts(data) {
  try {
    localStorage.setItem(CACHE_KEY, JSON.stringify({
      data,
      timestamp: Date.now()
    }));
  } catch (e) {
    // Ignore cache errors
  }
}

function formatNumber(num) {
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'k';
  }
  return num.toString();
}

async function fetchDownloadCounts() {
  // Check cache first
  const cached = getCachedCounts();
  if (cached) {
    updateUI(cached);
    return;
  }
  
  try {
    // Fetch release info from GitHub API
    const response = await fetch(
      `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/releases/tags/${RELEASE_TAG}`
    );
    
    if (!response.ok) {
      throw new Error('Failed to fetch release info');
    }
    
    const release = await response.json();
    
    // Extract download counts
    const counts = {};
    release.assets.forEach(asset => {
      if (FILE_MAP[asset.name]) {
        counts[asset.name] = asset.download_count;
      }
    });
    
    // Cache the results
    setCachedCounts(counts);
    
    // Update UI
    updateUI(counts);
    
  } catch (error) {
    console.error('Error fetching download counts:', error);
    // Show default values on error
    showDefaultCounts();
  }
}

function updateUI(counts) {
  Object.entries(FILE_MAP).forEach(([fileName, elementId]) => {
    const element = document.getElementById(elementId);
    if (element) {
      const count = counts[fileName] || 0;
      const span = element.querySelector('span:last-child');
      if (span) {
        span.textContent = formatNumber(count);
      }
    }
  });
}

function showDefaultCounts() {
  Object.values(FILE_MAP).forEach(elementId => {
    const element = document.getElementById(elementId);
    if (element) {
      const span = element.querySelector('span:last-child');
      if (span) {
        span.textContent = '-';
      }
    }
  });
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  // Only fetch if we're on the main page with download counts
  if (document.querySelector('[id^="dl-"]')) {
    fetchDownloadCounts();
  }
});

// Export for manual refresh
if (typeof window !== 'undefined') {
  window.refreshDownloadCounts = fetchDownloadCounts;
}
