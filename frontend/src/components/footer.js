/**
 * Footer Component
 * Renders the footer with copyright and links
 */

function renderFooter() {
    const currentYear = new Date().getFullYear();
    
    // Detect if we're in a subdirectory (pages/) or root
    const currentPath = window.location.pathname;
    const isInSubdir = currentPath.includes('/pages/');
    
    // Set base path for navigation
    const basePath = isInSubdir ? '../' : '';
    const homeLink = isInSubdir ? '../index.html' : 'index.html';
    
    const footerHTML = `
        <footer class="app-footer">
            <div class="footer-container">
                <div class="footer-content">
                    <div class="footer-section footer-about">
                        <h3 class="footer-title">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.5 2A2.5 2.5 0 0112 4.5v15a2.5 2.5 0 01-4.96.44 2.5 2.5 0 01-2.96-3.08 3 3 0 01-.34-5.58 2.5 2.5 0 011.32-4.24 2.5 2.5 0 011.98-3A2.5 2.5 0 019.5 2z"/><path d="M14.5 2A2.5 2.5 0 0012 4.5v15a2.5 2.5 0 004.96.44 2.5 2.5 0 002.96-3.08 3 3 0 00.34-5.58 2.5 2.5 0 00-1.32-4.24 2.5 2.5 0 00-1.98-3A2.5 2.5 0 0014.5 2z"/></svg>
                            Social Media Well-being Predictor
                        </h3>
                        <p class="footer-description">
                            Phân tích sức khỏe tinh thần dựa trên thói quen sử dụng mạng xã hội bằng mô hình Machine Learning
                        </p>
                    </div>
                    
                    <div class="footer-section footer-links">
                        <h4 class="footer-subtitle">Liên kết nhanh</h4>
                        <ul class="footer-link-list">
                            <li><a href="${homeLink}" class="footer-link">Trang chủ</a></li>
                            <li><a href="${basePath}pages/about.html" class="footer-link">Giới thiệu</a></li>
                            <li><a href="${basePath}pages/history.html" class="footer-link">Lịch sử</a></li>
                            <li><a href="${basePath}pages/help.html" class="footer-link">Hướng dẫn</a></li>
                        </ul>
                    </div>
                    
                    <div class="footer-section footer-info">
                        <h4 class="footer-subtitle">Thông tin</h4>
                        <ul class="footer-info-list">
                            <li>Đồ án môn Trí Tuệ Nhân Tạo</li>
                            <li>Học viện Công nghệ Bưu chính Viễn thông (PTIT)</li>
                            <li>Năm học ${currentYear}</li>
                            <li>Version 2.0</li>
                        </ul>
                    </div>
                </div>
                
                <div class="footer-bottom">
                    <p class="footer-copyright">
                        © ${currentYear} Social Media Well-being Predictor | PTIT AI Project
                    </p>
                    <p class="footer-tech">
                        Built with FastAPI + Scikit-learn + PostgreSQL
                    </p>
                </div>
            </div>
        </footer>
    `;
    
    return footerHTML;
}

// Insert footer into page
document.addEventListener('DOMContentLoaded', function() {
    const footerContainer = document.getElementById('footerContainer');
    if (footerContainer) {
        footerContainer.innerHTML = renderFooter();
    }
});
