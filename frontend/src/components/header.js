/**
 * Header Component with Role-Based Navigation
 * Renders different navigation based on user role (admin/user)
 */

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
                    <i class="fas fa-home nav-icon"></i>
                    <span class="nav-text">Trang chủ</span>
                </a>
            </li>
            <li class="nav-item">
                <a href="${basePath}pages/about.html" class="nav-link" data-page="about">
                    <i class="fas fa-info-circle nav-icon"></i>
                    <span class="nav-text">Giới thiệu</span>
                </a>
            </li>
            <li class="nav-item">
                <a href="${basePath}pages/help.html" class="nav-link" data-page="help">
                    <i class="fas fa-question-circle nav-icon"></i>
                    <span class="nav-text">Hướng dẫn</span>
                </a>
            </li>
        `;
        
        // Role-specific items
        if (user.role === 'admin') {
            // Admin navigation - simplified
            navItems += `
                <li class="nav-item">
                    <a href="${basePath}pages/admin/dashboard.html" class="nav-link" data-page="admin-dashboard">
                        <i class="fas fa-chart-line nav-icon"></i>
                        <span class="nav-text">Dashboard</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a href="${basePath}pages/admin/users.html" class="nav-link" data-page="admin-users">
                        <i class="fas fa-users nav-icon"></i>
                        <span class="nav-text">Người Dùng</span>
                    </a>
                </li>
            `;
        } else {
            // Regular user navigation
            navItems += `
                <li class="nav-item">
                    <a href="${basePath}pages/history.html" class="nav-link" data-page="history">
                        <i class="fas fa-history nav-icon"></i>
                        <span class="nav-text">Lịch sử</span>
                    </a>
                </li>
            `;
        }
        
        // Logout for all logged in users
        navItems += `
            <li class="nav-item">
                <a href="#" class="nav-link" id="logoutBtn">
                    <i class="fas fa-sign-out-alt nav-icon"></i>
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
                ${user.role === 'admin' ? '👑 Admin' : '👤 User'}
            </span>
        </div>
    ` : '';
    
    const headerHTML = `
        <header class="app-header">
            <div class="header-container">
                <div class="header-brand">
                    <a href="${homeLink}" class="brand-link">
                        <span class="brand-icon">🧠</span>
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
