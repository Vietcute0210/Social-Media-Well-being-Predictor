import numpy as np
import pandas as pd
from typing import Dict, Any


class Predictor:
    """Class to make predictions using loaded ML models"""
    
    def __init__(self, models: Dict):
        self.happiness_pipeline = models["happiness"]
        self.stress_pipeline = models["stress"]
        
        # Handle persona pipeline - might be a dict or Pipeline
        persona_model = models["persona"]
        if isinstance(persona_model, dict):
            # If it's a dict, try to extract the pipeline or model
            if 'model' in persona_model:
                self.persona_pipeline = persona_model['model']
            elif 'pipeline' in persona_model:
                self.persona_pipeline = persona_model['pipeline']
            else:
                # Use the dict directly and handle predict differently
                self.persona_pipeline = persona_model
        else:
            self.persona_pipeline = persona_model
            
        self.features = models["features"]
        self.persona_labels = models["persona_labels"]
    
    def prepare_input(self, user_data: Dict[str, Any]) -> pd.DataFrame:
        """Convert user input dict to DataFrame with correct feature order"""
        # Create DataFrame with features in correct order
        input_df = pd.DataFrame([user_data])
        
        # Ensure columns are in the same order as training
        input_df = input_df[self.features]
        
        return input_df
    
    def predict(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make predictions for happiness, stress, and persona"""
        try:
            # Prepare input
            input_df = self.prepare_input(user_data)
            
            # Make predictions
            happiness_score = float(self.happiness_pipeline.predict(input_df)[0])
            stress_score = float(self.stress_pipeline.predict(input_df)[0])
            
            # Clip scores to valid range [0, 10]
            happiness_score = np.clip(happiness_score, 0, 10)
            stress_score = np.clip(stress_score, 0, 10)
            
            # Handle persona prediction - might be dict or pipeline
            try:
                if isinstance(self.persona_pipeline, dict):
                    # If dict, use a simple heuristic based on usage
                    usage = user_data.get("daily_active_minutes_instagram", 0)
                    if usage > 120:
                        persona_class = 1  # Doom-Scroller
                    else:
                        persona_class = 2  # Light User
                else:
                    persona_class = int(self.persona_pipeline.predict(input_df)[0])
                    # Manual overrides removed - using pure ML prediction

            except Exception as e:
                print(f"Warning: Persona prediction failed: {str(e)}, using default")
                persona_class = 2  # Default to Light User
            
            # Get persona label
            persona = self.persona_labels.get(str(persona_class), "Unknown")
            
            # Generate recommendations
            recommendations = self.generate_recommendations(
                happiness_score, stress_score, persona, user_data
            )
            
            return {
                "happiness_score": round(happiness_score, 2),
                "stress_score": round(stress_score, 2),
                "persona": persona,
                "recommendations": recommendations
            }
        except Exception as e:
            raise Exception(f"Prediction error: {str(e)}")
    
    def generate_recommendations(
        self, 
        happiness: float, 
        stress: float, 
        persona: str,
        user_data: Dict[str, Any]
    ) -> list[str]:
        """Generate personalized recommendations based on predictions"""
        recommendations = []
        
        # Happiness-based recommendations
        if happiness < 5:
            recommendations.append("🌟 Hãy tham gia các hoạt động mang lại niềm vui và hạnh phúc cho bạn")
            recommendations.append("🤝 Dành nhiều thời gian chất lượng hơn với người thân yêu")
        elif happiness < 7:
            recommendations.append("😊 Bạn đang làm tốt lắm! Hãy duy trì lối sống hiện tại")
        else:
            recommendations.append("🎉 Mức độ hạnh phúc tuyệt vời! Hãy chia sẻ năng lượng tích cực với mọi người")
        
        # Stress-based recommendations
        if stress > 7:
            recommendations.append("🧘 Phát hiện căng thẳng cao. Hãy thử thiền định hoặc các bài tập chánh niệm")
            recommendations.append("💤 Đảm bảo bạn ngủ đủ giấc (7-9 tiếng mỗi đêm)")
            if user_data.get("exercise_hours_per_week", 0) < 3:
                recommendations.append("🏃 Tăng cường hoạt động thể chất - ít nhất 30 phút mỗi ngày")
        elif stress > 5:
            recommendations.append("⚖️ Căng thẳng vừa phải. Hãy cân bằng giữa công việc và cuộc sống")
        
        # Persona-based recommendations
        if persona == "Doom-Scroller":
            recommendations.append("📱 Giảm thời gian sử dụng mạng xã hội - đặt giới hạn hàng ngày trên Instagram")
            recommendations.append("🔕 Tắt thông báo không cần thiết để giảm lo lắng")
            recommendations.append("🌳 Dành nhiều thời gian cho các hoạt động ngoại tuyến và sở thích")
            
            # Check specific Instagram usage
            if user_data.get("daily_active_minutes_instagram", 0) > 120:
                recommendations.append("⏰ Thời gian sử dụng Instagram của bạn khá cao. Hãy cố gắng giới hạn 1-2 tiếng mỗi ngày")
        else:
            recommendations.append("✅ Thói quen sử dụng mạng xã hội lành mạnh! Hãy giữ cân bằng")
        
        # Sleep recommendations
        if user_data.get("sleep_hours_per_night", 8) < 6:
            recommendations.append("😴 Bạn cần ngủ nhiều hơn. Hãy cố gắng ngủ 7-9 tiếng mỗi đêm")
        
        # Exercise recommendations
        if user_data.get("exercise_hours_per_week", 0) < 2.5:
            recommendations.append("💪 Tăng cường hoạt động thể chất để cải thiện sức khỏe tinh thần")
        
        # Social connection recommendations
        if user_data.get("social_events_per_month", 0) < 4:
            recommendations.append("👥 Tăng cường giao lưu trực tiếp để cải thiện sức khỏe tinh thần")
        
        return recommendations[:6]  # Limit to 6 recommendations
