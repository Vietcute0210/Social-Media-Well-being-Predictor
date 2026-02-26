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
            if 'model' in persona_model:
                self.persona_pipeline = persona_model['model']
            elif 'pipeline' in persona_model:
                self.persona_pipeline = persona_model['pipeline']
            else:
                self.persona_pipeline = persona_model
        else:
            self.persona_pipeline = persona_model
            
        self.features = models["features"]
        self.persona_labels = models["persona_labels"]
        
        # Usage features for persona prediction
        self.usage_features = [
            "daily_active_minutes_instagram", "sessions_per_day",
            "reels_watched_per_day", "stories_viewed_per_day",
            "time_on_feed_per_day", "time_on_reels_per_day",
            "likes_given_per_day", "comments_written_per_day",
            "notification_response_rate"
        ]
        
        # Log model info for verification
        print(f"📊 Models loaded:")
        print(f"   Happiness pipeline type: {type(self.happiness_pipeline).__name__}")
        print(f"   Stress pipeline type: {type(self.stress_pipeline).__name__}")
        print(f"   Persona pipeline type: {type(self.persona_pipeline).__name__}")
        print(f"   Features count: {len(self.features)}")
        print(f"   Persona labels: {self.persona_labels}")
    
    def prepare_input(self, user_data: Dict[str, Any]) -> pd.DataFrame:
        """Convert user input dict to DataFrame with correct feature order"""
        input_df = pd.DataFrame([user_data])
        input_df = input_df[self.features]
        return input_df
    
    def predict(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make predictions for happiness, stress, and persona"""
        try:
            # Prepare input
            input_df = self.prepare_input(user_data)
            
            # Make predictions using real ML models
            happiness_score = float(self.happiness_pipeline.predict(input_df)[0])
            stress_score = float(self.stress_pipeline.predict(input_df)[0])
            
            # Clip scores to valid range [0, 10]
            happiness_score = np.clip(happiness_score, 0, 10)
            stress_score = np.clip(stress_score, 0, 10)
            
            # Log raw predictions for debugging
            print(f"🔮 Raw predictions - Happiness: {happiness_score:.2f}, Stress: {stress_score:.2f}")
            
            # Persona prediction using KMeans clustering
            try:
                if isinstance(self.persona_pipeline, dict):
                    # Fallback: rule-based persona from multiple signals
                    persona_class = self._rule_based_persona(user_data, happiness_score, stress_score)
                    print(f"   Persona (rule-based): class={persona_class}")
                else:
                    # Use the KMeans pipeline - it needs only usage features
                    usage_data = {k: float(user_data.get(k, 0)) for k in self.usage_features}
                    usage_df = pd.DataFrame([usage_data])
                    persona_class = int(self.persona_pipeline.predict(usage_df)[0])
                    print(f"   Persona (KMeans): class={persona_class}")
                    print(f"   Usage input: minutes={usage_data.get('daily_active_minutes_instagram')}, "
                          f"sessions={usage_data.get('sessions_per_day')}, "
                          f"reels={usage_data.get('reels_watched_per_day')}")

            except Exception as e:
                print(f"Warning: Persona prediction failed: {str(e)}, using rule-based")
                persona_class = self._rule_based_persona(user_data, happiness_score, stress_score)
            
            # Get persona label
            persona = self.persona_labels.get(str(persona_class), "Unknown")
            
            # Cross-validate persona with happiness/stress scores
            # Nếu model ML cho persona không khớp với stress/happiness, điều chỉnh
            persona = self._validate_persona_consistency(
                persona, happiness_score, stress_score, user_data
            )
            
            print(f"   Final persona: {persona}")
            
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
            print(f"❌ Prediction error: {str(e)}")
            import traceback
            traceback.print_exc()
            raise Exception(f"Prediction error: {str(e)}")
    
    def _validate_persona_consistency(
        self, 
        ml_persona: str, 
        happiness: float, 
        stress: float,
        user_data: Dict[str, Any]
    ) -> str:
        """
        Determine persona based on actual usage patterns + stress/happiness context.
        
        KMeans model clusters có thể bị lệch do dữ liệu training,
        nên ta dùng rule-based classification dựa trên usage metrics thực tế
        kết hợp với stress/happiness để xác định persona chính xác.
        """
        usage_minutes = float(user_data.get("daily_active_minutes_instagram", 0))
        sessions = float(user_data.get("sessions_per_day", 0))
        reels = float(user_data.get("reels_watched_per_day", 0))
        stories = float(user_data.get("stories_viewed_per_day", 0))
        likes = float(user_data.get("likes_given_per_day", 0))
        comments = float(user_data.get("comments_written_per_day", 0))
        notification_rate = float(user_data.get("notification_response_rate", 0))
        
        # Tính điểm engagement tổng hợp
        engagement_score = (
            usage_minutes * 0.4 +          # Thời gian sử dụng là quan trọng nhất
            sessions * 6 +                  # Nhiều sessions = dùng liên tục
            reels * 1.5 +                   # Xem reels nhiều
            stories * 1.0 +                 # Xem stories
            likes * 1.0 +                   # Tương tác like
            comments * 2.5 +                # Viết comment = engagement sâu
            notification_rate * 25          # Phản hồi thông báo nhanh
        )
        
        # Điều chỉnh dựa trên sức khỏe tinh thần
        # Stress cao + happiness thấp = sử dụng tiêu cực
        if stress > 7 and happiness < 5:
            engagement_score *= 1.2  # Tăng 20%
        elif stress > 8 and happiness < 4:
            engagement_score *= 1.35  # Tăng 35%
        
        print(f"   Engagement score: {engagement_score:.1f} (usage={usage_minutes}min, sessions={sessions})")
        
        # Phân loại dựa trên engagement score
        # Light User: engagement < 50 (usage < ~40 phút, ít tương tác)
        # Moderate User: engagement 50-220 (usage ~40-150 phút)
        # Doom-Scroller: engagement > 220 (usage > 150 phút hoặc tương tác rất cao)
        
        if engagement_score > 220:
            persona = "Doom-Scroller"
        elif engagement_score > 50:
            persona = "Moderate User"
        else:
            persona = "Light User"
        
        if persona != ml_persona:
            print(f"   ⚠ Adjusted {ml_persona} → {persona} (engagement={engagement_score:.1f})")
        
        return persona
    
    def _rule_based_persona(self, user_data: Dict[str, Any], 
                            happiness: float = 5.0, stress: float = 5.0) -> int:
        """
        Rule-based fallback for persona classification using multiple signals.
        Returns the cluster index matching the persona labels.
        """
        usage = float(user_data.get("daily_active_minutes_instagram", 0))
        sessions = int(user_data.get("sessions_per_day", 0))
        reels = int(user_data.get("reels_watched_per_day", 0))
        stories = int(user_data.get("stories_viewed_per_day", 0))
        likes = int(user_data.get("likes_given_per_day", 0))
        comments = int(user_data.get("comments_written_per_day", 0))
        notification_rate = float(user_data.get("notification_response_rate", 0))
        
        # Calculate an engagement score from multiple signals
        engagement_score = (
            usage * 0.35 +             # Time spent is primary factor
            sessions * 8 +              # More sessions = more addictive usage
            reels * 2 +                 # Reels consumption
            stories * 1.5 +             # Stories consumption
            likes * 1.5 +               # Active engagement
            comments * 3 +              # Deep engagement
            notification_rate * 30      # Responsive to notifications = more engaged
        )
        
        # Thêm yếu tố stress/happiness vào tính toán
        # Stress cao + happiness thấp = dấu hiệu sử dụng quá mức
        wellbeing_penalty = 0
        if stress > 7 and happiness < 4:
            wellbeing_penalty = 30  # Tăng engagement score đáng kể
        elif stress > 6 and happiness < 5:
            wellbeing_penalty = 15
        
        engagement_score += wellbeing_penalty
        
        print(f"   Rule-based engagement: {engagement_score:.1f} (penalty: {wellbeing_penalty})")
        
        # Find which persona label maps to which cluster
        doom_scroller_id = None
        moderate_id = None
        light_id = None
        
        for key, label in self.persona_labels.items():
            if label == "Doom-Scroller":
                doom_scroller_id = int(key)
            elif label == "Moderate User":
                moderate_id = int(key)
            elif label == "Light User":
                light_id = int(key)
        
        # Thresholds based on engagement score
        if engagement_score > 120:
            return doom_scroller_id if doom_scroller_id is not None else 0
        elif engagement_score > 50:
            return moderate_id if moderate_id is not None else 2
        else:
            return light_id if light_id is not None else 1
    
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
        if happiness < 4:
            recommendations.append("Hãy tham gia các hoạt động mang lại niềm vui và hạnh phúc cho bạn")
            recommendations.append("Dành nhiều thời gian chất lượng hơn với người thân yêu")
        elif happiness < 6:
            recommendations.append("Thử tìm thêm các hoạt động mới để nâng cao tinh thần")
            recommendations.append("Hãy duy trì và cải thiện lối sống hiện tại")
        elif happiness < 8:
            recommendations.append("Bạn đang làm tốt lắm! Hãy duy trì lối sống lành mạnh")
        else:
            recommendations.append("Mức độ hạnh phúc tuyệt vời! Hãy chia sẻ năng lượng tích cực với mọi người")
        
        # Stress-based recommendations
        if stress > 7:
            recommendations.append("Phát hiện căng thẳng cao. Hãy thử thiền định hoặc các bài tập chánh niệm")
            recommendations.append("Đảm bảo bạn ngủ đủ giấc (7-9 tiếng mỗi đêm)")
            if user_data.get("exercise_hours_per_week", 0) < 3:
                recommendations.append("Tăng cường hoạt động thể chất - ít nhất 30 phút mỗi ngày")
        elif stress > 5:
            recommendations.append("Căng thẳng vừa phải. Hãy cân bằng giữa công việc và cuộc sống")
        else:
            recommendations.append("Mức căng thẳng thấp - rất tốt! Hãy tiếp tục duy trì")
        
        # Persona-based recommendations
        if persona == "Doom-Scroller":
            recommendations.append("Giảm thời gian sử dụng mạng xã hội - đặt giới hạn hàng ngày trên Instagram")
            recommendations.append("Tắt thông báo không cần thiết để giảm lo lắng")
            recommendations.append("Dành nhiều thời gian cho các hoạt động ngoại tuyến và sở thích")
            
            if user_data.get("daily_active_minutes_instagram", 0) > 120:
                recommendations.append("Thời gian sử dụng Instagram của bạn khá cao. Hãy cố gắng giới hạn 1-2 tiếng mỗi ngày")
        elif persona == "Moderate User":
            recommendations.append("Thói quen sử dụng mạng xã hội ở mức trung bình. Hãy chú ý không tăng thêm")
            if user_data.get("daily_active_minutes_instagram", 0) > 90:
                recommendations.append("Cân nhắc giảm bớt thời gian xem Reels để có thêm thời gian cho bản thân")
        else:  # Light User
            recommendations.append("Thói quen sử dụng mạng xã hội lành mạnh! Hãy giữ cân bằng")
        
        # Sleep recommendations
        if user_data.get("sleep_hours_per_night", 8) < 6:
            recommendations.append("Bạn cần ngủ nhiều hơn. Hãy cố gắng ngủ 7-9 tiếng mỗi đêm")
        
        # Exercise recommendations
        if user_data.get("exercise_hours_per_week", 0) < 2.5:
            recommendations.append("Tăng cường hoạt động thể chất để cải thiện sức khỏe tinh thần")
        
        # Social connection recommendations
        if user_data.get("social_events_per_month", 0) < 4:
            recommendations.append("Tăng cường giao lưu trực tiếp để cải thiện sức khỏe tinh thần")
        
        return recommendations[:6]  # Limit to 6 recommendations
