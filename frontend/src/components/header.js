/**
 * Header Component
 * Renders the header with navigation menu
 */

function renderHeader() {
    // Detect if we're in a subdirectory (pages/) or root
    const currentPath = window.location.pathname;
    const isInSubdir = currentPath.includes('/pages/');
    
    // Set base path for navigation
    const basePath = isInSubdir ? '../' : '';
    const homeLink = isInSubdir ? '../index.html' : 'index.html';
    
    const headerHTML = `
        <header class="app-header">
            <div class="header-container">
                <div class="header-brand">
                    <a href="${homeLink}" class="brand-link">
                        <span class="brand-icon">🧠</span>
                        <span class="brand-text">Well-being Predictor</span>
                    </a>
                </div>
                
                <nav class="header-nav">
                    <button class="nav-toggle" id="navToggle" aria-label="Toggle navigation">
                        <span class="hamburger"></span>
                        <span class="hamburger"></span>
                        <span class="hamburger"></span>
                    </button>
                    
                    <ul class="nav-menu" id="navMenu">
                        <li class="nav-item">
                            <a href="${homeLink}" class="nav-link" data-page="home">
                                <span class="nav-icon">🏠</span>
                                <span class="nav-text">Trang chủ</span>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="${basePath}pages/about.html" class="nav-link" data-page="about">
                                <span class="nav-icon">📖</span>
                                <span class="nav-text">Giới thiệu</span>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="${basePath}pages/history.html" class="nav-link" data-page="history">
                                <span class="nav-icon">📊</span>
                                <span class="nav-text">Lịch sử</span>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="${basePath}pages/help.html" class="nav-link" data-page="help">
                                <span class="nav-icon">❓</span>
                                <span class="nav-text">Hướng dẫn</span>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="${basePath}pages/dashboard.html" class="nav-link" data-page="dashboard">
                                <span class="nav-icon">📈</span>
                                <span class="nav-text">Thống kê</span>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="#" class="nav-link" id="logoutBtn">
                                <span class="nav-icon">🚪</span>
                                <span class="nav-text">Đăng xuất</span>
                            </a>
                        </li>
                    </ul>
                </nav>
            </div>
        </header>
    `;
    
    return headerHTML;
}

// Insert header into page
document.addEventListener('DOMContentLoaded', function() {
    const headerContainer = document.getElementById('headerContainer');
    if (headerContainer) {
        headerContainer.innerHTML = renderHeader();
        initializeNavigation();
    }
});

// Initialize navigation functionality
function initializeNavigation() {
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    
    // Mobile menu toggle
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!event.target.closest('.header-nav')) {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            }
        });
    }
    
    // Set active page
    setActivePage();
    
    // Logout functionality
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            
            try {
                await fetch('http://localhost:8000/auth/logout', {
                    method: 'POST',
                    credentials: 'include'
                });
                
                // Redirect to login
                window.location.href = 'login.html';
            } catch (error) {
                console.error('Logout failed:', error);
                // Still redirect on error
                window.location.href = 'login.html';
            }
        });
    }
}

// Set active page based on current URL
function setActivePage() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        
        // Check if current page matches link
        if (currentPath.includes('index.html') || currentPath.endsWith('/')) {
            if (link.dataset.page === 'home') {
                link.classList.add('active');
            }
        } else if (currentPath.includes(link.dataset.page)) {
            link.classList.add('active');
        }
    });
}
