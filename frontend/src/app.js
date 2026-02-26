// Configuration
const API_BASE_URL = 'http://localhost:8000';

// Check authentication on page load
window.addEventListener('DOMContentLoaded', async () => {
    // First check localStorage - if user exists, don't block immediately
    const localUser = localStorage.getItem('current_user');
    
    // Retry 3 lần với delay tăng dần cho Supabase cold start
    const maxRetries = 3;
    const retryDelays = [1500, 2500, 0];
    
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 10000);
            
            const response = await fetch(`${API_BASE_URL}/auth/me`, {
                credentials: 'include',
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            
            if (response.ok) {
                return; // Authenticated, proceed normally
            }
            
            // Server says not authenticated
            window.location.href = 'login.html';
            return;
        } catch (error) {
            if (attempt < maxRetries) {
                await new Promise(r => setTimeout(r, retryDelays[attempt - 1]));
            }
        }
    }
    
    // All attempts failed - if no local user, redirect
    if (!localUser) {
        window.location.href = 'login.html';
    }
    // If there IS a local user, let them continue (graceful degradation)
});

// DOM Elements
const predictionForm = document.getElementById('predictionForm');
const formSection = document.getElementById('formSection');
const resultsSection = document.getElementById('resultsSection');
const submitBtn = document.getElementById('submitBtn');
const analyzeAgainBtn = document.getElementById('analyzeAgainBtn');

// Result elements
const happinessScore = document.getElementById('happinessScore');
const stressScore = document.getElementById('stressScore');
const personaType = document.getElementById('personaType');
const recommendationsList = document.getElementById('recommendationsList');
const happinessBar = document.getElementById('happinessBar');
const stressBar = document.getElementById('stressBar');

// Form submission handler
predictionForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Show loading state
    setLoadingState(true);
    
    try {
        // Collect form data
        const formData = new FormData(predictionForm);
        const data = {};
        
        // Convert form data to object with correct types
        for (let [key, value] of formData.entries()) {
            const input = document.getElementById(key);
            const inputType = input.type;
            
            if (inputType === 'number') {
                // Check if it's an integer or float field
                if (input.step && input.step !== '1') {
                    data[key] = parseFloat(value);
                } else {
                    data[key] = parseInt(value);
                }
            } else {
                data[key] = value;
            }
        }
        
        console.log('Sending data:', data);
        
        // Make API request
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include', // Important: send cookies
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Có lỗi xảy ra khi phân tích');
        }
        
        const result = await response.json();
        console.log('Prediction result:', result);
        
        // Display results
        displayResults(result);
        
    } catch (error) {
        console.error('Error:', error);
        alert(`Lỗi: ${error.message}\n\nVui lòng đảm bảo backend đang chạy tại ${API_BASE_URL}`);
    } finally {
        setLoadingState(false);
    }
});

// Analyze again button handler
analyzeAgainBtn.addEventListener('click', () => {
    resultsSection.style.display = 'none';
    formSection.style.display = 'block';
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Set loading state
function setLoadingState(isLoading) {
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoader = submitBtn.querySelector('.btn-loader');
    
    if (isLoading) {
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline';
        submitBtn.disabled = true;
    } else {
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
        submitBtn.disabled = false;
    }
}

// Display results
function displayResults(result) {
    // Update scores
    happinessScore.textContent = `${result.happiness_score}/10`;
    stressScore.textContent = `${result.stress_score}/10`;
    personaType.textContent = result.persona;
    
    // Update progress bars with animation
    const happinessPercent = (result.happiness_score / 10) * 100;
    const stressPercent = (result.stress_score / 10) * 100;
    
    setTimeout(() => {
        happinessBar.style.width = `${happinessPercent}%`;
        stressBar.style.width = `${stressPercent}%`;
    }, 100);
    
    // Add color classes based on scores
    updateScoreCardColor('happiness-card', result.happiness_score);
    updateScoreCardColor('stress-card', result.stress_score, true);
    
    // Update persona card color
    const personaCard = document.querySelector('.persona-card');
    if (result.persona === 'Doom-Scroller') {
        personaCard.classList.add('warning');
    } else {
        personaCard.classList.add('success');
    }
    
    // Display recommendations
    recommendationsList.innerHTML = '';
    result.recommendations.forEach(recommendation => {
        const li = document.createElement('li');
        li.className = 'recommendation-item';
        li.textContent = recommendation;
        recommendationsList.appendChild(li);
        
        // Animate items
        setTimeout(() => {
            li.classList.add('show');
        }, 100);
    });
    
    // Save to localStorage
    savePredictionToLocalStorage(result);
    
    // Show results section and hide form
    formSection.style.display = 'none';
    resultsSection.style.display = 'block';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Save prediction to localStorage
function savePredictionToLocalStorage(result) {
    try {
        // Get form data as input
        const formData = new FormData(predictionForm);
        const inputData = {};
        
        for (let [key, value] of formData.entries()) {
            const input = document.getElementById(key);
            inputData[key] = input.type === 'number' ? parseFloat(value) : value;
        }
        
        // Create prediction object
        const prediction = {
            input: inputData,
            output: {
                happiness_score: result.happiness_score,
                stress_score: result.stress_score,
                persona: result.persona,
                recommendations: result.recommendations
            }
        };
        
        // Use storage.js savePrediction function if available
        if (typeof savePrediction === 'function') {
            savePrediction(prediction);
            console.log('✓ Prediction saved to localStorage');
        } else {
            // Fallback: save directly
            const predictions = JSON.parse(localStorage.getItem('wellbeing_predictions') || '[]');
            predictions.unshift({
                id: 'pred_' + Date.now(),
                timestamp: new Date().toISOString(),
                ...prediction
            });
            localStorage.setItem('wellbeing_predictions', JSON.stringify(predictions));
            console.log('✓ Prediction saved to localStorage (fallback)');
        }
    } catch (error) {
        console.error('Error saving prediction:', error);
    }
}

// Update score card color based on value
function updateScoreCardColor(cardClass, score, isStress = false) {
    const card = document.querySelector(`.${cardClass}`);
    card.classList.remove('low', 'medium', 'high', 'warning', 'success');
    
    if (isStress) {
        // For stress, lower is better
        if (score < 4) {
            card.classList.add('success');
        } else if (score < 7) {
            card.classList.add('medium');
        } else {
            card.classList.add('warning');
        }
    } else {
        // For happiness, higher is better
        if (score < 4) {
            card.classList.add('warning');
        } else if (score < 7) {
            card.classList.add('medium');
        } else {
            card.classList.add('success');
        }
    }
}

// Check backend health on load
async function checkBackendHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            console.log('✓ Backend is connected and healthy');
        } else {
            console.warn('⚠ Backend responded but may have issues');
        }
    } catch (error) {
        console.error('✗ Cannot connect to backend:', error);
        console.log(`Make sure backend is running at ${API_BASE_URL}`);
    }
}

// Check health on page load
checkBackendHealth();
