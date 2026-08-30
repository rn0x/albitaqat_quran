/* ========================================
   i18n - Internationalization
   ======================================== */

const translations = {
  ar: {
    // Navigation
    nav: {
      home: "الرئيسية",
      surahs: "السور",
      api: "API",
      github: "GitHub",
      docs: "التوثيق"
    },
    
    // Hero
    hero: {
      title: "بطاقات القرآن الكريم",
      subtitle: "بيانات 114 سورة متكاملة - صوت، PDF، يوتيوب",
      cta_download: "تحميل البيانات",
      cta_surahs: "تصفح السور",
      cta_api: "استخدم API"
    },
    
    // Stats
    stats: {
      surahs: "سورة",
      videos: "فيديو",
      ayahs: "آية",
      size: "MB"
    },
    
    // About
    about: {
      title: "عن المشروع",
      subtitle: "مشروع وقفي عالمي لخدمة القرآن الكريم",
      author_title: "المؤلف",
      author_name: "أ.د. ياسر بن إسماعيل راضي",
      site_title: "الموقع الرسمي",
      book_title: "الكتاب",
      book_info: "135 صفحة - ISBN: 9786030350469",
      audio_title: "التسجيل الصوتي",
      audio_info: "استديو وقف تعظيم الوحيين",
      description: "برنامج عملي مصاحب لقراءة القرآن الكريم وحفظه، يوفر مَتْنٍ مختصرٍ شاملٍ لسور القرآن مسموعاً ومقروءاً."
    },
    
    // Clone Section
    clone: {
      title: "تحميل المشروع",
      subtitle: "استنسخ المستودع وابدأ خلال دقائق",
      step1: "1. استنسخ المستودع",
      step2: "2. تحقق من الملفات"
    },
    
    // Data Files
    data: {
      title: "ملفات البيانات",
      subtitle: "حمّل البيانات بصيغة JSON لاستخدامها في مشاريعك",
      filename: "اسم الملف",
      size: "الحجم",
      downloads_count: "التحميلات",
      description: "الوصف",
      download: "تحميل",
      cards_original: "البيانات الأصلية المكشطة من الموقع",
      cards_full: "البيانات الشاملة مع روابط الصوت و PDF و يوتيوب",
      audio_links: "روابط تحميل الصوت (114 ملف MP3)",
      pdf_links: "روابط تحميل البطاقات بصيغة PDF",
      youtube_links: "فيديوهات شرح البطاقات من يوتيوب (140+)",
      download_all: "تحميل جميع الملفات من GitHub Releases"
    },
    
    // Examples
    examples: {
      title: "أمثلة الاستخدام",
      subtitle: "كيف تستخدم البيانات في مشاريعك"
    },
    
    // Quick Start
    quickstart: {
      title: "البدء السريع",
      subtitle: "ابدأ باستخدام البيانات في دقائق",
      python: "Python",
      nodejs: "Node.js",
      docker: "Docker",
      api: "API",
      copy: "نسخ",
      copied: "تم النسخ!"
    },
    
    // API Preview
    api: {
      title: "واجهة برمجة التطبيقات",
      subtitle: "API مجاني للوصول لبيانات البطاقات",
      try_it: "جرّب الآن",
      docs: "التوثيق الكامل",
      response: "استجابة API"
    },
    
    // Docker
    docker: {
      title: "Docker",
      subtitle: "شغّل API مع جميع البيانات في ثوانٍ",
      auto_download: "تحميل تلقائي",
      auto_download_desc: "يحمل جميع ملفات الصوت و PDF تلقائياً عند التشغيل",
      persistent: "بيانات محفوظة",
      persistent_desc: "تُحفظ البيانات في Docker Volume ولا تضيع",
      production: "جاهز للإنتاج",
      production_desc: "مبني لأداء عالٍ مع Rate Limiting و Logging"
    },
    
    // Footer
    footer: {
      description: "مشروع وقفي عالمي يهدف إلى خدمة القرآن الكريم وحفّاظِهِ وقارئيه.",
      links: "روابط سريعة",
      official: "الروابط الرسمية",
      copyright: "جميع الحقوق محفوظة للمؤلف",
      quote: "بِالقُرْآنِ نَهْتَدِي، وَبِتَدْبِيرِهِ نَرْتَقِي."
    },
    
    // Surahs Page
    surahs: {
      title: "السور",
      subtitle: "تصفح 114 سورة من القرآن الكريم",
      search: "بحث عن سورة...",
      all: "الكل",
      meccan: "مكية",
      medinan: "مدنية",
      number: "#",
      name: "الاسم",
      english: "English",
      ayahs: "آيات",
      type: "النوع",
      links: "الروابط",
      audio: "الصوت",
      pdf: "PDF",
      youtube: "يوتيوب"
    }
  },
  
  en: {
    // Navigation
    nav: {
      home: "Home",
      surahs: "Surahs",
      api: "API",
      github: "GitHub",
      docs: "Docs"
    },
    
    // Hero
    hero: {
      title: "Al-Bitaqat Quran",
      subtitle: "Complete data for 114 surahs - Audio, PDF, YouTube",
      cta_download: "Download Data",
      cta_surahs: "Browse Surahs",
      cta_api: "Use API"
    },
    
    // Stats
    stats: {
      surahs: "Surahs",
      videos: "Videos",
      ayahs: "Ayahs",
      size: "MB"
    },
    
    // About
    about: {
      title: "About",
      subtitle: "A global endowment project serving the Quran",
      author_title: "Author",
      author_name: "Dr. Yasser bin Ismail Radi",
      site_title: "Official Website",
      book_title: "The Book",
      book_info: "135 pages - ISBN: 9786030350469",
      audio_title: "Audio Recording",
      audio_info: "Studio of Ta'zeem Al-Waheen Foundation",
      description: "A practical program accompanying Quran reading and memorization, providing a concise comprehensive text for all Quran surahs, available as audio and readable content."
    },
    
    // Clone Section
    clone: {
      title: "Clone Project",
      subtitle: "Clone the repository and start in minutes",
      step1: "1. Clone the Repository",
      step2: "2. Verify the Files"
    },
    
    // Data Files
    data: {
      title: "Data Files",
      subtitle: "Download the data in JSON format for your projects",
      filename: "Filename",
      size: "Size",
      downloads_count: "Downloads",
      description: "Description",
      download: "Download",
      cards_original: "Original scraped data from the website",
      cards_full: "Complete data with audio, PDF, and YouTube links",
      audio_links: "Audio download links (114 MP3 files)",
      pdf_links: "PDF card download links",
      youtube_links: "YouTube tutorial videos (140+)",
      download_all: "Download all files from GitHub Releases"
    },
    
    // Examples
    examples: {
      title: "Usage Examples",
      subtitle: "How to use the data in your projects"
    },
    
    // Quick Start
    quickstart: {
      title: "Quick Start",
      subtitle: "Start using the data in minutes",
      python: "Python",
      nodejs: "Node.js",
      docker: "Docker",
      api: "API",
      copy: "Copy",
      copied: "Copied!"
    },
    
    // API Preview
    api: {
      title: "API",
      subtitle: "Free REST API for Quran Cards data",
      try_it: "Try it now",
      docs: "Full Documentation",
      response: "API Response"
    },
    
    // Docker
    docker: {
      title: "Docker",
      subtitle: "Run the API with all data in seconds",
      auto_download: "Auto Download",
      auto_download_desc: "Downloads all audio and PDF files automatically on startup",
      persistent: "Persistent Data",
      persistent_desc: "Data is saved in Docker Volumes and persists",
      production: "Production Ready",
      production_desc: "Built for high performance with Rate Limiting and Logging"
    },
    
    // Footer
    footer: {
      description: "A global endowment project serving the Quran, its memorizers and readers.",
      links: "Quick Links",
      official: "Official Links",
      copyright: "All rights reserved for the author",
      quote: "With the Quran we are guided, and by contemplating it we ascend."
    },
    
    // Surahs Page
    surahs: {
      title: "Surahs",
      subtitle: "Browse 114 surahs of the Holy Quran",
      search: "Search surah...",
      all: "All",
      meccan: "Meccan",
      medinan: "Medinan",
      number: "#",
      name: "Name",
      english: "English",
      ayahs: "Ayahs",
      type: "Type",
      links: "Links",
      audio: "Audio",
      pdf: "PDF",
      youtube: "YouTube"
    }
  }
};

// i18n Manager
class I18n {
  constructor() {
    this.currentLang = localStorage.getItem('lang') || 'ar';
    this.init();
  }
  
  init() {
    this.updateDirection();
    this.updateContent();
  }
  
  setLang(lang) {
    this.currentLang = lang;
    localStorage.setItem('lang', lang);
    this.updateDirection();
    this.updateContent();
  }
  
  t(key) {
    const keys = key.split('.');
    let value = translations[this.currentLang];
    for (const k of keys) {
      value = value?.[k];
    }
    return value || key;
  }
  
  updateDirection() {
    const dir = this.currentLang === 'ar' ? 'rtl' : 'ltr';
    document.documentElement.dir = dir;
    document.documentElement.lang = this.currentLang;
  }
  
  updateContent() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      el.textContent = this.t(key);
    });
    
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
      const key = el.getAttribute('data-i18n-placeholder');
      el.placeholder = this.t(key);
    });
    
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
      const key = el.getAttribute('data-i18n-title');
      el.title = this.t(key);
    });
    
    // Update lang toggle button
    const langBtn = document.querySelector('.lang-toggle');
    if (langBtn) {
      const textSpan = langBtn.querySelector('span:last-child');
      if (textSpan) {
        textSpan.textContent = this.currentLang === 'ar' ? 'EN' : 'AR';
      }
    }
    
    // Update active nav link
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.navbar-nav a').forEach(link => {
      const href = link.getAttribute('href');
      if (href === currentPage || (currentPage === '' && href === 'index.html')) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });
  }
  
  toggleLang() {
    const newLang = this.currentLang === 'ar' ? 'en' : 'ar';
    this.setLang(newLang);
  }
}

// Initialize i18n
const i18n = new I18n();
