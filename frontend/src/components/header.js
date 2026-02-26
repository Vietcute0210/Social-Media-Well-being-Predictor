/**
 * Header Component with Role-Based Navigation
 * Uses Lucide-style SVG icons for a clean, professional look
 */

// SVG Icon definitions (Lucide-style, simple and professional)
const ICONS = {
    home: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
    info: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
    help: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 015.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    chart: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
    users: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87"/><path d="M16 3.13a4 4 0 010 7.75"/></svg>',
    history: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    logout: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>',
    brain: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.5 2A2.5 2.5 0 0112 4.5v15a2.5 2.5 0 01-4.96.44 2.5 2.5 0 01-2.96-3.08 3 3 0 01-.34-5.58 2.5 2.5 0 011.32-4.24 2.5 2.5 0 011.98-3A2.5 2.5 0 019.5 2z"/><path d="M14.5 2A2.5 2.5 0 0012 4.5v15a2.5 2.5 0 004.96.44 2.5 2.5 0 002.96-3.08 3 3 0 00.34-5.58 2.5 2.5 0 00-1.32-4.24 2.5 2.5 0 00-1.98-3A2.5 2.5 0 0014.5 2z"/></svg>',
    admin: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>',
    user: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'
};

function renderHeader() {
    // Detect if we're in a subdirectory
    const currentPath = window.location.pathname;
    const isInSubdir = currentPath.includes('/pages/');
    const isInAdminDir = currentPath.includes('/admin/');
    
    // Set base paths
    let basePath = '';
    let homeLink = 'index.html';
    
    if (isInAdminDir) {
        basePath = '../../';
        homeLink = '../../index.html';
    } else if (isInSubdir) {
        basePath = '../';
        homeLink = '../index.html';
    }
    
    // Get current user
    let user = null;
    try {
        const userData = localStorage.getItem('current_user');
        user = userData ? JSON.parse(userData) : null;
    } catch (e) {
        console.error('Error loading user:', e);
    }
    
    // Generate navigation items based on role
    let navItems = '';
    
    if (user) {
        // Common items for all logged in users
        navItems += `
            <li class="nav-item">
                <a href="${homeLink}" class="nav-link" data-page="home">
                    <span class="nav-icon">${ICONS.home}</span>
                    <span class="nav-text">Trang chủ</span>
                </a>
            </li>
            <li class="nav-item">
                <a href="${basePath}pages/about.html" class="nav-link" data-page="about">
                    <span class="nav-icon">${ICONS.info}</span>
                    <span class="nav-text">Giới thiệu</span>
                </a>
            </li>
            <li class="nav-item">
                <a href="${basePath}pages/help.html" class="nav-link" data-page="help">
                    <span class="nav-icon">${ICONS.help}</span>
                    <span class="nav-text">Hướng dẫn</span>
                </a>
            </li>
        `;
        
        // Role-specific items
        if (user.role === 'admin') {
            navItems += `
                <li class="nav-item">
                    <a href="${basePath}pages/admin/dashboard.html" class="nav-link" data-page="admin-dashboard">
                        <span class="nav-icon">${ICONS.chart}</span>
                        <span class="nav-text">Dashboard</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a href="${basePath}pages/admin/users.html" class="nav-link" data-page="admin-users">
                        <span class="nav-icon">${ICONS.users}</span>
                        <span class="nav-text">Người Dùng</span>
                    </a>
                </li>
            `;
        } else {
            navItems += `
                <li class="nav-item">
                    <a href="${basePath}pages/history.html" class="nav-link" data-page="history">
                        <span class="nav-icon">${ICONS.history}</span>
                        <span class="nav-text">Lịch sử</span>
                    </a>
                </li>
            `;
        }
        
        // Logout for all logged in users
        navItems += `
            <li class="nav-item">
                <a href="#" class="nav-link nav-link-logout" id="logoutBtn">
                    <span class="nav-icon">${ICONS.logout}</span>
                    <span class="nav-text">Đăng xuất</span>
                </a>
            </li>
        `;
    }
    
    // User info display
    const userInfo = user ? `
        <div class="user-info">
            <span class="user-name">${user.username}</span>
            <span class="user-badge ${user.role === 'admin' ? 'badge-admin' : 'badge-user'}">
                ${user.role === 'admin' ? ICONS.admin + ' Admin' : ICONS.user + ' User'}
            </span>
        </div>
    ` : '';
    
    const headerHTML = `
        <header class="app-header">
            <div class="header-container">
                <div class="header-brand">
                    <a href="${homeLink}" class="brand-link">
                        <span class="brand-icon">${ICONS.brain}</span>
                        <span class="brand-text">Well-being Predictor</span>
                    </a>
                </div>
                
                ${userInfo}
                
                <nav class="header-nav">
                    <button class="nav-toggle" id="navToggle" aria-label="Toggle navigation">
                        <span class="hamburger"></span>
                        <span class="hamburger"></span>
                        <span class="hamburger"></span>
                    </button>
                    
                    <ul class="nav-menu" id="navMenu">
                        ${navItems}
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
                // Clear localStorage
                localStorage.removeItem('current_user');
                
                // Call logout API
                await fetch('http://localhost:8000/auth/logout', {
                    method: 'POST',
                    credentials: 'include'
                });
                
                console.log('✓ Logged out');
            } catch (error) {
                console.error('Logout error:', error);
            }
            
            // Redirect to login
            const currentPath = window.location.pathname;
            if (currentPath.includes('/admin/')) {
                window.location.href = '../../login.html';
            } else if (currentPath.includes('/pages/')) {
                window.location.href = '../login.html';
            } else {
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
        const page = link.dataset.page;
        if (!page) return;
        
        // Check if current page matches link
        if (currentPath.includes('index.html') || currentPath.endsWith('/')) {
            if (page === 'home') {
                link.classList.add('active');
            }
        } else if (currentPath.includes(page)) {
            link.classList.add('active');
        }
    });
}
