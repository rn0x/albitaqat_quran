/* ========================================
   Main JavaScript - Al-Bitaqat Quran
   ======================================== */

// DOM Ready
document.addEventListener('DOMContentLoaded', () => {
  initMobileMenu();
  initLangToggle();
  initQuickstartTabs();
  initCopyButtons();
  initSmoothScroll();
  initScrollAnimation();
});

// Mobile Menu Toggle
function initMobileMenu() {
  const menuBtn = document.querySelector('.mobile-menu-btn');
  const navMenu = document.querySelector('.navbar-nav');
  
  if (menuBtn && navMenu) {
    menuBtn.addEventListener('click', () => {
      navMenu.classList.toggle('active');
      menuBtn.textContent = navMenu.classList.contains('active') ? '✕' : '☰';
    });
    
    // Close menu when clicking a link
    navMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        menuBtn.textContent = '☰';
      });
    });
  }
}

// Language Toggle
function initLangToggle() {
  const langBtn = document.querySelector('.lang-toggle');
  if (langBtn) {
    langBtn.addEventListener('click', () => {
      i18n.toggleLang();
    });
  }
}

// Quickstart Tabs
function initQuickstartTabs() {
  const tabs = document.querySelectorAll('.quickstart-tab');
  const contents = document.querySelectorAll('.quickstart-content');
  
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const target = tab.getAttribute('data-tab');
      
      // Update active tab
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      
      // Update content
      contents.forEach(content => {
        content.style.display = content.id === target ? 'block' : 'none';
      });
    });
  });
}

// Copy Code Buttons
function initCopyButtons() {
  document.querySelectorAll('.copy-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      const codeBlock = btn.closest('.code-block');
      const code = codeBlock.querySelector('code')?.textContent || 
                   codeBlock.querySelector('pre')?.textContent;
      
      if (code) {
        try {
          await navigator.clipboard.writeText(code);
          const originalText = btn.textContent;
          btn.textContent = i18n.t('quickstart.copied');
          setTimeout(() => {
            btn.textContent = originalText;
          }, 2000);
        } catch (err) {
          console.error('Failed to copy:', err);
        }
      }
    });
  });
}

// Smooth Scroll
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
}

// Scroll Animation
function initScrollAnimation() {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-fade-in');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);
  
  document.querySelectorAll('.section').forEach(section => {
    observer.observe(section);
  });
}

// Surahs Page Functions
function initSurahsPage() {
  const searchInput = document.querySelector('.search-box input');
  const filterBtns = document.querySelectorAll('.filter-btn');
  const tableBody = document.querySelector('.surahs-table tbody');
  
  if (!tableBody) return;
  
  let currentFilter = 'all';
  let searchQuery = '';
  
  // Render surahs
  function renderSurahs() {
    const surahs = window.surahsData || [];
    
    let filtered = surahs;
    
    // Apply filter
    if (currentFilter !== 'all') {
      filtered = filtered.filter(s => 
        currentFilter === 'makki' ? s.revelation_type === 'مكية' : s.revelation_type === 'مدنية'
      );
    }
    
    // Apply search
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(s => 
        s.name_english.toLowerCase().includes(query) ||
        s.name_arabic.includes(searchQuery) ||
        s.number.toString().includes(query)
      );
    }
    
    // Render
    tableBody.innerHTML = filtered.map(surah => `
      <tr>
        <td class="surah-number">${surah.number}</td>
        <td class="surah-arabic">${surah.name_arabic}</td>
        <td class="surah-name">${surah.name_english}</td>
        <td>${surah.ayahs_count}</td>
        <td>
          <span class="surah-type ${surah.revelation_type === 'مكية' ? 'type-makki' : 'type-madani'}">
            ${i18n.currentLang === 'ar' ? surah.revelation_type : (surah.revelation_type === 'مكية' ? 'Meccan' : 'Medinan')}
          </span>
        </td>
        <td>
          <div class="surah-links">
            ${surah.downloads?.audio?.url ? `
              <a href="${surah.downloads.audio.url}" target="_blank" title="${i18n.t('surahs.audio')}" download>
                🔊
              </a>
            ` : ''}
            ${surah.downloads?.pdf?.url ? `
              <a href="${surah.downloads.pdf.url}" target="_blank" title="${i18n.t('surahs.pdf')}" download>
                📄
              </a>
            ` : ''}
            ${surah.downloads?.youtube_video?.url ? `
              <a href="${surah.downloads.youtube_video.url}" target="_blank" title="${i18n.t('surahs.youtube')}">
                🎬
              </a>
            ` : ''}
          </div>
        </td>
      </tr>
    `).join('');
  }
  
  // Search handler
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value;
      renderSurahs();
    });
  }
  
  // Filter handlers
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentFilter = btn.getAttribute('data-filter');
      renderSurahs();
    });
  });
  
  // Initial render
  renderSurahs();
}

// Export for use in surahs.html
if (typeof window !== 'undefined') {
  window.initSurahsPage = initSurahsPage;
}
