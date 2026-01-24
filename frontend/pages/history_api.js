/**
 * History Page API Integration
 * Fetch prediction history from backend API instead of localStorage
 */

const API_BASE = 'http://localhost:8000';

let currentFilter = 'all';
let currentSort = 'newest';
let allPredictions = [];

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    loadHistoryFromAPI();
    setupEventListeners();
});

function setupEventListeners() {
    document.getElementById('personaFilter').addEventListener('change', function(e) {
        currentFilter = e.target.value;
        filterAndDisplayHistory();
    });

    document.getElementById('sortBy').addEventListener('change', function(e) {
        currentSort = e.target.value;
        filterAndDisplayHistory();
    });
}

async function loadHistoryFromAPI() {
    try {
        const response = await fetch(`${API_BASE}/predictions/history`, {
            credentials: 'include'
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                window.location.href = '../login.html';
                return;
            }
            throw new Error('Failed to load history');
        }
        
        allPredictions = await response.json();
        
        // Populate persona filter
        populatePersonaFilter();
        
        // Load stats
        loadStatsFromAPI();
        
        // Display history
        filterAndDisplayHistory();
        
    } catch (error) {
        console.error('Error loading history:', error);
        showError('Không thể tải lịch sử. Vui lòng thử lại.');
    }
}

async function loadStatsFromAPI() {
    try {
        const response = await fetch(`${API_BASE}/predictions/stats`, {
            credentials: 'include'
        });
        
        if (!response.ok) throw new Error('Failed to load stats');
        
        const stats = await response.json();
        
        document.getElementById('totalCount').textContent = stats.total_predictions;
        document.getElementById('avgHappiness').textContent = stats.average_happiness;
        document.getElementById('avgStress').textContent = stats.average_stress;
        document.getElementById('commonPersona').textContent = stats.most_common_persona;
        
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

function populatePersonaFilter() {
    const personaCounts = {};
    allPredictions.forEach(p => {
        personaCounts[p.persona] = (personaCounts[p.persona] || 0) + 1;
    });
    
    const select = document.getElementById('personaFilter');
    // Clear existing options except "All"
    select.innerHTML = '<option value="all">Tất cả</option>';
    
    Object.keys(personaCounts).forEach(persona => {
        const option = document.createElement('option');
        option.value = persona;
        option.textContent = `${persona} (${personaCounts[persona]})`;
        select.appendChild(option);
    });
}

function filterAndDisplayHistory() {
    let filtered = allPredictions;
    
    // Filter by persona
    if (currentFilter !== 'all') {
        filtered = filtered.filter(p => p.persona === currentFilter);
    }
    
    // Sort
    filtered = sortPredictions(filtered, currentSort);
    
    // Display
    displayHistory(filtered);
}

function sortPredictions(predictions, sortBy) {
    const sorted = [...predictions];
    
    switch(sortBy) {
        case 'newest':
            // Already sorted by backend
            break;
        case 'oldest':
            sorted.reverse();
            break;
        case 'happiness':
            sorted.sort((a, b) => b.happiness_score - a.happiness_score);
            break;
        case 'stress':
            sorted.sort((a, b) => b.stress_score - a.stress_score);
            break;
    }
    
    return sorted;
}

function displayHistory(predictions) {
    const tbody = document.getElementById('historyBody');
    const emptyState = document.getElementById('emptyState');
    const table = document.getElementById('historyTable');
    
    if (predictions.length === 0) {
        table.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }
    
    table.style.display = 'table';
    emptyState.style.display = 'none';
    
    tbody.innerHTML = predictions.map(p => {
        const time = formatTimestamp(p.timestamp);
        const happinessClass = p.happiness_score >= 7 ? 'score-high' : 
                              p.happiness_score >= 4 ? 'score-medium' : 'score-low';
        const stressClass = p.stress_score >= 7 ? 'score-low' : 
                           p.stress_score >= 4 ? 'score-medium' : 'score-high';
        
        return `
            <tr>
                <td>
                    <div><strong>${time.relative}</strong></div>
                    <div style="font-size: 0.85rem; color: #999;">${time.absolute}</div>
                </td>
                <td><span class="score-value ${happinessClass}">${p.happiness_score}</span></td>
                <td><span class="score-value ${stressClass}">${p.stress_score}</span></td>
                <td><span class="persona-badge">${p.persona}</span></td>
                <td>
                    <button class="action-btn btn-view" onclick="viewPrediction(${p.id})">👁️ Xem</button>
                    <button class="action-btn btn-delete" onclick="deletePredictionConfirm(${p.id})">🗑️ Xóa</button>
                </td>
            </tr>
        `;
    }).join('');
}

function viewPrediction(id) {
    const prediction = allPredictions.find(p => p.id === id);
    if (!prediction) return;
    
    const details = `
Thời gian: ${formatTimestamp(prediction.timestamp).absolute}

KẾT QUẢ PHÂN TÍCH:
- Chỉ số hạnh phúc: ${prediction.happiness_score}/10
- Chỉ số căng thẳng: ${prediction.stress_score}/10
- Persona: ${prediction.persona}

KHUYẾN NGHỊ:
${prediction.recommendations.map((r, i) => `${i + 1}. ${r}`).join('\n')}
    `;
    
    alert(details);
}

async function deletePredictionConfirm(id) {
    if (confirm('Bạn có chắc muốn xóa kết quả phân tích này?')) {
        try {
            const response = await fetch(`${API_BASE}/predictions/${id}`, {
                method: 'DELETE',
                credentials: 'include'
            });
            
            if (!response.ok) throw new Error('Delete failed');
            
            // Reload history
            await loadHistoryFromAPI();
            
        } catch (error) {
            console.error('Error deleting prediction:', error);
            alert('Không thể xóa. Vui lòng thử lại.');
        }
    }
}

async function clearHistory() {
    if (confirm('Bạn có chắc muốn xóa TẤT CẢ lịch sử phân tích?\n\nHành động này không thể hoàn tác!')) {
        if (confirm('Xác nhận lần cuối: XÓA TẤT CẢ?')) {
            try {
                const response = await fetch(`${API_BASE}/predictions/all`, {
                    method: 'DELETE',
                    credentials: 'include'
                });
                
                if (!response.ok) throw new Error('Clear failed');
                
                // Reload
                location.reload();
                
            } catch (error) {
                console.error('Error clearing history:', error);
                alert('Không thể xóa. Vui lòng thử lại.');
            }
        }
    }
}

async function exportHistory() {
    try {
        const response = await fetch(`${API_BASE}/predictions/history`, {
            credentials: 'include'
        });
        
        if (!response.ok) throw new Error('Export failed');
        
        const data = await response.json();
        const json = JSON.stringify(data, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `wellbeing-history-${new Date().toISOString().split('T')[0]}.json`;
        a.click();
        
    } catch (error) {
        console.error('Error exporting history:', error);
        alert('Không thể xuất dữ liệu. Vui lòng thử lại.');
    }
}

function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    
    // Relative time
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    
    let relative;
    if (days > 0) {
        relative = `${days} ngày trước`;
    } else if (hours > 0) {
        relative = `${hours} giờ trước`;
    } else if (minutes > 0) {
        relative = `${minutes} phút trước`;
    } else {
        relative = 'Vừa xong';
    }
    
    // Absolute time
    const absolute = date.toLocaleString('vi-VN');
    
    return { relative, absolute };
}

function showError(message) {
    const tbody = document.getElementById('historyBody');
    tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: red;">${message}</td></tr>`;
}
