/**
 * Statistics Utility
 * Handles calculations and data formatting for dashboard
 */

/**
 * Get total number of predictions
 * @returns {number} Total count
 */
function getTotalPredictions() {
    const predictions = getAllPredictions();
    return predictions.length;
}

/**
 * Calculate persona distribution statistics
 * @returns {Object} Distribution data with counts and percentages
 */
function calculatePersonaDistribution() {
    const predictions = getAllPredictions();
    const distribution = {};
    const total = predictions.length;
    
    if (total === 0) {
        return {};
    }
    
    // Count occurrences with error handling
    predictions.forEach(p => {
        try {
            const persona = p.output?.persona;
            if (persona) {
                if (!distribution[persona]) {
                    distribution[persona] = { count: 0, percentage: 0 };
                }
                distribution[persona].count++;
            }
        } catch (e) {
            console.warn('Skipping malformed prediction in distribution:', p);
        }
    });
    
    // Calculate percentages
    const validTotal = Object.values(distribution).reduce((sum, d) => sum + d.count, 0);
    
    Object.keys(distribution).forEach(persona => {
        distribution[persona].percentage = ((distribution[persona].count / validTotal) * 100).toFixed(1);
    });
    
    return distribution;
}

/**
 * Get average happiness and stress scores
 * @returns {Object} Average scores
 */
function calculateAverageScores() {
    const predictions = getAllPredictions();
    
    if (predictions.length === 0) {
        return {
            happiness: 0,
            stress: 0
        };
    }
    
    const totals = predictions.reduce((acc, p) => {
        // Add error handling for malformed data
        try {
            const happiness = parseFloat(p.output?.happiness_score || 0);
            const stress = parseFloat(p.output?.stress_score || 0);
            
            if (!isNaN(happiness)) acc.happiness += happiness;
            if (!isNaN(stress)) acc.stress += stress;
            acc.count++;
        } catch (e) {
            console.warn('Skipping malformed prediction:', p);
        }
        return acc;
    }, { happiness: 0, stress: 0, count: 0 });
    
    if (totals.count === 0) {
        return { happiness: 0, stress: 0 };
    }
    
    return {
        happiness: (totals.happiness / totals.count).toFixed(1),
        stress: (totals.stress / totals.count).toFixed(1)
    };
}

/**
 * Get most common persona
 * @returns {string} Persona name
 */
function getMostCommonPersona() {
    const distribution = calculatePersonaDistribution();
    
    if (Object.keys(distribution).length === 0) {
        return '-';
    }
    
    let maxCount = 0;
    let mostCommon = '';
    
    Object.keys(distribution).forEach(persona => {
        if (distribution[persona].count > maxCount) {
            maxCount = distribution[persona].count;
            mostCommon = persona;
        }
    });
    
    return mostCommon;
}

/**
 * Get predictions from last N days
 * @param {number} days - Number of days
 * @returns {Array} Filtered predictions
 */
function getPredictionsFromLastDays(days = 7) {
    const predictions = getAllPredictions();
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - days);
    
    return predictions.filter(p => {
        return new Date(p.timestamp) >= cutoffDate;
    });
}

/**
 * Get score trends over time
 * @param {number} days - Number of days to analyze
 * @returns {Object} Trend data
 */
function getScoreTrends(days = 30) {
    const predictions = getPredictionsFromLastDays(days);
    
    if (predictions.length === 0) {
        return {
            happiness: { trend: 'neutral', change: 0 },
            stress: { trend: 'neutral', change: 0 }
        };
    }
    
    // Split into two halves
    const midpoint = Math.floor(predictions.length / 2);
    const firstHalf = predictions.slice(midpoint);
    const secondHalf = predictions.slice(0, midpoint);
    
    const firstAvg = {
        happiness: firstHalf.reduce((sum, p) => sum + parseFloat(p.output.happiness_score), 0) / firstHalf.length,
        stress: firstHalf.reduce((sum, p) => sum + parseFloat(p.output.stress_score), 0) / firstHalf.length
    };
    
    const secondAvg = {
        happiness: secondHalf.reduce((sum, p) => sum + parseFloat(p.output.happiness_score), 0) / secondHalf.length,
        stress: secondHalf.reduce((sum, p) => sum + parseFloat(p.output.stress_score), 0) / secondHalf.length
    };
    
    const happinessChange = secondAvg.happiness - firstAvg.happiness;
    const stressChange = secondAvg.stress - firstAvg.stress;
    
    return {
        happiness: {
            trend: happinessChange > 0.5 ? 'up' : happinessChange < -0.5 ? 'down' : 'neutral',
            change: happinessChange.toFixed(1)
        },
        stress: {
            trend: stressChange > 0.5 ? 'up' : stressChange < -0.5 ? 'down' : 'neutral',
            change: stressChange.toFixed(1)
        }
    };
}

/**
 * Format timestamp for display
 * @param {string} timestamp - ISO timestamp
 * @returns {Object} Formatted time
 */
function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    let relative = '';
    if (diffMins < 1) {
        relative = 'Vừa xong';
    } else if (diffMins < 60) {
        relative = `${diffMins} phút trước`;
    } else if (diffHours < 24) {
        relative = `${diffHours} giờ trước`;
    } else if (diffDays < 7) {
        relative = `${diffDays} ngày trước`;
    } else {
        relative = date.toLocaleDateString('vi-VN');
    }
    
    const absolute = date.toLocaleString('vi-VN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
    
    return {
        relative,
        absolute,
        date
    };
}

/**
 * Get persona chart data for visualization
 * @returns {Array} Chart data points
 */
function getPersonaChartData() {
    const distribution = calculatePersonaDistribution();
    const chartData = [];
    
    Object.keys(distribution).forEach(persona => {
        chartData.push({
            label: persona,
            count: distribution[persona].count,
            percentage: parseFloat(distribution[persona].percentage)
        });
    });
    
    // Sort by count descending
    chartData.sort((a, b) => b.count - a.count);
    
    return chartData;
}

/**
 * Get score trends chart data
 * @param {number} points - Number of data points
 * @returns {Array} Chart data
 */
function getScoreTrendsChartData(points = 10) {
    const predictions = getAllPredictions();
    const dataPoints = [];
    
    if (predictions.length === 0) {
        return [];
    }
    
    // Take evenly spaced predictions
    const step = Math.max(1, Math.floor(predictions.length / points));
    
    for (let i = predictions.length - 1; i >= 0; i -= step) {
        const p = predictions[i];
        dataPoints.push({
            timestamp: formatTimestamp(p.timestamp).relative,
            happiness: parseFloat(p.output.happiness_score),
            stress: parseFloat(p.output.stress_score)
        });
    }
    
    return dataPoints.reverse();
}

/**
 * Get statistics summary for dashboard
 * @returns {Object} Complete stats summary
 */
function getDashboardStats() {
    const predictions = getAllPredictions();
    const recentPredictions = getPredictionsFromLastDays(7);
    
    return {
        total: predictions.length,
        recentCount: recentPredictions.length,
        averageScores: calculateAverageScores(),
        mostCommonPersona: getMostCommonPersona(),
        personaDistribution: calculatePersonaDistribution(),
        trends: getScoreTrends(30)
    };
}
