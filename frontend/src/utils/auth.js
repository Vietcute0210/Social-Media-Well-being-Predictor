/**
 * Authentication Utility
 * Handles user authentication, role checking, and session management
 */

const AUTH_STORAGE_KEY = 'current_user';

/**
 * Save user info to localStorage after login
 * @param {Object} userData - User data from login response {username, role, user_id}
 */
function saveUser(userData) {
    try {
        localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(userData));
        console.log('✓ User saved:', userData.username, '| Role:', userData.role);
    } catch (error) {
        console.error('Error saving user:', error);
    }
}

/**
 * Get current logged in user
 * @returns {Object|null} User object or null if not logged in
 */
function getCurrentUser() {
    try {
        const userData = localStorage.getItem(AUTH_STORAGE_KEY);
        return userData ? JSON.parse(userData) : null;
    } catch (error) {
        console.error('Error getting user:', error);
        return null;
    }
}

/**
 * Check if user is currently logged in
 * @returns {boolean} True if logged in
 */
function isLoggedIn() {
    return getCurrentUser() !== null;
}

/**
 * Check if current user is admin
 * @returns {boolean} True if user is admin
 */
function isAdmin() {
    const user = getCurrentUser();
    return user && user.role === 'admin';
}

/**
 * Check if current user is regular user
 * @returns {boolean} True if user role is 'user'
 */
function isRegularUser() {
    const user = getCurrentUser();
    return user && user.role === 'user';
}

/**
 * Logout current user
 */
async function logout() {
    try {
        // Clear localStorage
        localStorage.removeItem(AUTH_STORAGE_KEY);
        
        // Call logout API
        await fetch('http://localhost:8000/auth/logout', {
            method: 'POST',
            credentials: 'include'
        });
        
        console.log('✓ User logged out');
        
        // Redirect to login
        window.location.href = '/login.html';
    } catch (error) {
        console.error('Error during logout:', error);
        // Still clear local data and redirect
        localStorage.removeItem(AUTH_STORAGE_KEY);
        window.location.href = '/login.html';
    }
}

/**
 * Require authentication - redirect to login if not logged in
 * Call this at the top of pages that need auth
 */
function requireAuth() {
    if (!isLoggedIn()) {
        console.warn('⚠ Not authenticated, redirecting to login...');
        window.location.href = '/login.html';
        return false;
    }
    return true;
}

/**
 * Require admin role - redirect if not admin
 * Call this on admin-only pages
 */
function requireAdmin() {
    if (!isLoggedIn()) {
        console.warn('⚠ Not authenticated, redirecting to login...');
        window.location.href = '/login.html';
        return false;
    }
    
    if (!isAdmin()) {
        console.warn('⚠ Admin access required, redirecting...');
        window.location.href = '/index.html';
        return false;
    }
    
    return true;
}

/**
 * Get user's home page based on role
 * @returns {string} URL to redirect to
 */
function getUserHomePage() {
    const user = getCurrentUser();
    if (!user) return '/login.html';
    
    if (user.role === 'admin') {
        return '/pages/admin/dashboard.html';
    } else {
        return '/index.html';
    }
}

/**
 * Check authentication status with server
 * @returns {Promise<Object|null>} User object or null
 */
async function checkAuthStatus() {
    try {
        const response = await fetch('http://localhost:8000/auth/me', {
            credentials: 'include'
        });
        
        if (response.ok) {
            const userData = await response.json();
            saveUser(userData);
            return userData;
        } else {
            // Clear invalid session
            localStorage.removeItem(AUTH_STORAGE_KEY);
            return null;
        }
    } catch (error) {
        console.error('Error checking auth:', error);
        return null;
    }
}

/**
 * Initialize auth on page load
 * Optionally checks with server to sync session
 */
async function initAuth(checkServer = false) {
    if (checkServer) {
        await checkAuthStatus();
    }
    
    const user = getCurrentUser();
    if (user) {
        console.log('✓ Auth initialized:', user.username, '| Role:', user.role);
    } else {
        console.log('⚠ No active session');
    }
}
