/* ========================================
   Main JavaScript - Al-Bitaqat Quran
   Version: 2.0 - Enhanced
   ======================================== */

// DOM Ready
document.addEventListener('DOMContentLoaded', () => {
  initMobileMenu();
  initLangToggle();
  initQuickstartTabs();
  initCopyButtons();
  initSmoothScroll();
  initScrollReveal();
  initNavbarScroll();
});

// Mobile Menu Toggle
function initMobileMenu() {
  const menuBtn = document.querySelector('.mobile-menu-btn');
  const navMenu = document.querySelector('.navbar-nav');
  
  if (menuBtn && navMenu) {
    menuBtn.addEventListener('click', () => {
      navMenu.classList.toggle('active');
      const icon = menuBtn.querySelector('.material-symbols-rounded');
      icon.textContent = navMenu.classList.contains('active') ? 'close' : 'menu';
    });
    
    // Close menu when clicking a link
    navMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        const icon = menuBtn.querySelector('.material-symbols-rounded');
        icon.textContent = 'menu';
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
      
      // Update content with animation
      contents.forEach(content => {
        if (content.id === target) {
          content.style.display = 'block';
          content.style.opacity = '0';
          content.style.transform = 'translateY(10px)';
          setTimeout(() => {
            content.style.transition = 'all 0.3s ease';
            content.style.opacity = '1';
            content.style.transform = 'translateY(0)';
          }, 10);
        } else {
          content.style.display = 'none';
        }
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
          const icon = btn.querySelector('.material-symbols-rounded');
          const text = btn.querySelector('span:last-child');
          const originalText = text?.textContent;
          
          if (icon) icon.textContent = 'check';
          if (text) text.textContent = i18n.t('quickstart.copied');
          
          btn.style.background = 'var(--green-700)';
          btn.style.color = 'var(--white)';
          
          setTimeout(() => {
            if (icon) icon.textContent = 'content_copy';
            if (text) text.textContent = originalText || i18n.t('quickstart.copy');
            btn.style.background = '';
            btn.style.color = '';
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
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      
      const target = document.querySelector(targetId);
      if (target) {
        const offset = 80; // Account for fixed navbar
        const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - offset;
        
        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth'
        });
      }
    });
  });
}

// Scroll Reveal Animation
function initScrollReveal() {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
        // Stagger animation for grid items
        const children = entry.target.querySelectorAll('.card, .stat-card, .docker-feature, .example-card');
        children.forEach((child, index) => {
          child.style.animationDelay = `${index * 0.1}s`;
          child.classList.add('animate-fade-in');
        });
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);
  
  // Add reveal class to sections
  document.querySelectorAll('.section-header, .about-grid, .stats-grid, .docker-grid, .examples-grid, .api-preview').forEach(el => {
    el.classList.add('reveal');
    observer.observe(el);
  });
}

// Navbar Scroll Effect
function initNavbarScroll() {
  const navbar = document.getElementById('navbar');
  if (!navbar) return;
  
  let lastScroll = 0;
  
  window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
    
    lastScroll = currentScroll;
  }, { passive: true });
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
    tableBody.innerHTML = filtered.map((surah, index) => `
      <tr style="animation: fadeInUp 0.3s ease ${index * 0.02}s forwards; opacity: 0;">
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
                <span class="material-symbols-rounded">headphones</span>
              </a>
            ` : ''}
            ${surah.downloads?.pdf?.url ? `
              <a href="${surah.downloads.pdf.url}" target="_blank" title="${i18n.t('surahs.pdf')}" download>
                <span class="material-symbols-rounded">picture_as_pdf</span>
              </a>
            ` : ''}
            ${surah.downloads?.youtube_video?.url ? `
              <a href="${surah.downloads.youtube_video.url}" target="_blank" title="${i18n.t('surahs.youtube')}">
                <span class="material-symbols-rounded">play_circle</span>
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
