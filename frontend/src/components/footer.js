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
                            <span class="footer-icon">🧠</span>
                            Social Media Well-being Predictor
                        </h3>
                        <p class="footer-description">
                            Phân tích sức khỏe tinh thần dựa trên thói quen sử dụng mạng xã hội
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
                            <li>🎓 Đồ án môn Trí Tuệ Nhân Tạo</li>
                            <li>🏫 Học viện PTIT</li>
                            <li>📅 ${currentYear}</li>
                            <li>📊 Version 2.0</li>
                        </ul>
                    </div>
                </div>
                
                <div class="footer-bottom">
                    <p class="footer-copyright">
                        © ${currentYear} Social Media Well-being Predictor | PTIT AI Project
                    </p>
                    <p class="footer-tech">
                        Built with FastAPI + Machine Learning
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
