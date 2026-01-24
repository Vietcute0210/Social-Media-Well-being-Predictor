/**
 * Storage Utility
 * Handles localStorage operations for predictions history
 */

const STORAGE_KEYS = {
    PREDICTIONS: 'wellbeing_predictions',
    STATS: 'wellbeing_stats'
};

/**
 * Save a new prediction to localStorage
 * @param {Object} predictionData - The prediction data to save
 * @returns {boolean} Success status
 */
function savePrediction(predictionData) {
    try {
        const predictions = getAllPredictions();
        
        // Create prediction object with timestamp and unique ID
        const prediction = {
            id: generateId(),
            timestamp: new Date().toISOString(),
            input: predictionData.input,
            output: predictionData.output
        };
        
        // Add to beginning of array (newest first)
        predictions.unshift(prediction);
        
        // Save to localStorage
        localStorage.setItem(STORAGE_KEYS.PREDICTIONS, JSON.stringify(predictions));
        
        // Update stats
        updateStats();
        
        return true;
    } catch (error) {
        console.error('Error saving prediction:', error);
        return false;
    }
}

/**
 * Get all predictions from localStorage
 * @returns {Array} Array of predictions
 */
function getAllPredictions() {
    try {
        const data = localStorage.getItem(STORAGE_KEYS.PREDICTIONS);
        return data ? JSON.parse(data) : [];
    } catch (error) {
        console.error('Error getting predictions:', error);
        return [];
    }
}

/**
 * Get a single prediction by ID
 * @param {string} id - Prediction ID
 * @returns {Object|null} Prediction object or null
 */
function getPredictionById(id) {
    const predictions = getAllPredictions();
    return predictions.find(p => p.id === id) || null;
}

/**
 * Delete a prediction by ID
 * @param {string} id - Prediction ID
 * @returns {boolean} Success status
 */
function deletePrediction(id) {
    try {
        const predictions = getAllPredictions();
        const filtered = predictions.filter(p => p.id !== id);
        
        localStorage.setItem(STORAGE_KEYS.PREDICTIONS, JSON.stringify(filtered));
        updateStats();
        
        return true;
    } catch (error) {
        console.error('Error deleting prediction:', error);
        return false;
    }
}

/**
 * Clear all predictions
 * @returns {boolean} Success status
 */
function clearAllPredictions() {
    try {
        localStorage.removeItem(STORAGE_KEYS.PREDICTIONS);
        localStorage.removeItem(STORAGE_KEYS.STATS);
        return true;
    } catch (error) {
        console.error('Error clearing predictions:', error);
        return false;
    }
}

/**
 * Get recent predictions
 * @param {number} count - Number of predictions to retrieve
 * @returns {Array} Array of recent predictions
 */
function getRecentPredictions(count = 5) {
    const predictions = getAllPredictions();
    return predictions.slice(0, count);
}

/**
 * Get predictions within a date range
 * @param {Date} startDate - Start date
 * @param {Date} endDate - End date
 * @returns {Array} Filtered predictions
 */
function getPredictionsByDateRange(startDate, endDate) {
    const predictions = getAllPredictions();
    return predictions.filter(p => {
        const predDate = new Date(p.timestamp);
        return predDate >= startDate && predDate <= endDate;
    });
}

/**
 * Get predictions by persona
 * @param {string} persona - Persona name
 * @returns {Array} Filtered predictions
 */
function getPredictionsByPersona(persona) {
    const predictions = getAllPredictions();
    if (!persona || persona === 'all') {
        return predictions;
    }
    return predictions.filter(p => p.output.persona === persona);
}

/**
 * Export predictions to JSON
 * @returns {string} JSON string
 */
function exportPredictionsToJSON() {
    const predictions = getAllPredictions();
    return JSON.stringify(predictions, null, 2);
}

/**
 * Import predictions from JSON
 * @param {string} jsonString - JSON string
 * @returns {boolean} Success status
 */
function importPredictionsFromJSON(jsonString) {
    try {
        const predictions = JSON.parse(jsonString);
        
        // Validate structure
        if (!Array.isArray(predictions)) {
            throw new Error('Invalid format: must be an array');
        }
        
        localStorage.setItem(STORAGE_KEYS.PREDICTIONS, JSON.stringify(predictions));
        updateStats();
        
        return true;
    } catch (error) {
        console.error('Error importing predictions:', error);
        return false;
    }
}

/**
 * Update statistics in localStorage
 */
function updateStats() {
    try {
        const predictions = getAllPredictions();
        
        const stats = {
            totalPredictions: predictions.length,
            lastUpdated: new Date().toISOString(),
            personaDistribution: calculatePersonaDistributionStats(predictions),
            averageScores: getAverageScores(predictions)
        };
        
        localStorage.setItem(STORAGE_KEYS.STATS, JSON.stringify(stats));
    } catch (error) {
        console.error('Error updating stats:', error);
    }
}

/**
 * Get stats from localStorage
 * @returns {Object} Stats object
 */
function getStats() {
    try {
        const data = localStorage.getItem(STORAGE_KEYS.STATS);
        if (!data) {
            updateStats();
            return JSON.parse(localStorage.getItem(STORAGE_KEYS.STATS) || '{}');
        }
        return JSON.parse(data);
    } catch (error) {
        console.error('Error getting stats:', error);
        return {};
    }
}

/**
 * Generate unique ID
 * @returns {string} Unique ID
 */
function generateId() {
    return 'pred_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

/**
 * Calculate persona distribution from predictions
 * @param {Array} predictions 
 * @returns {Object} Distribution object
 */
function calculatePersonaDistributionStats(predictions) {
    const distribution = {};
    
    predictions.forEach(p => {
        const persona = p.output.persona;
        distribution[persona] = (distribution[persona] || 0) + 1;
    });
    
    return distribution;
}

/**
 * Get average scores
 * @param {Array} predictions 
 * @returns {Object} Average scores
 */
function getAverageScores(predictions) {
    if (predictions.length === 0) {
        return { happiness: 0, stress: 0 };
    }
    
    const totals = predictions.reduce((acc, p) => {
        acc.happiness += p.output.happiness_score;
        acc.stress += p.output.stress_score;
        return acc;
    }, { happiness: 0, stress: 0 });
    
    return {
        happiness: (totals.happiness / predictions.length).toFixed(1),
        stress: (totals.stress / predictions.length).toFixed(1)
    };
}
