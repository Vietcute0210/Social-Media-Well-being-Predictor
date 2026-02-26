import sys
import os
import random
import json
from datetime import datetime, timezone, timedelta

# Add backend directory to sys path so we can import from app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine, Base
from app.models_db import User, Prediction, VN_TZ, vn_now
import bcrypt

def hash_password(password: str) -> str:
    """Generate password hash using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def create_fake_data():
    # Make sure tables exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if users already exist to avoid duplicates
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"Skipping seed: Already found {existing_users} users in DB.")
            return

        now = vn_now()

        print("Generating 10 fake users...")
        users = []
        for i in range(1, 11):
            username = f"user{i}_demo"
            password = "password123"
            hashed_pw = hash_password(password)
            
            user = User(
                username=username,
                hashed_password=hashed_pw,
                role="user" if i > 2 else "admin",
                created_at=now - timedelta(days=random.randint(1, 30))
            )
            users.append(user)
            db.add(user)
            
        db.commit()
        
        for user in users:
            db.refresh(user)
            
        print("Generating 10 fake predictions with diverse personas...")
        
        # Define varied profiles to ensure different personas
        profiles = [
            # Doom-Scroller profile
            {
                "daily_active_minutes_instagram": 200, "sessions_per_day": 15,
                "reels_watched_per_day": 80, "stories_viewed_per_day": 50,
                "time_on_feed_per_day": 90, "time_on_reels_per_day": 100,
                "likes_given_per_day": 60, "comments_written_per_day": 15,
                "notification_response_rate": 0.95,
                "expected_persona": "Doom-Scroller"
            },
            # Doom-Scroller profile 2
            {
                "daily_active_minutes_instagram": 180, "sessions_per_day": 12,
                "reels_watched_per_day": 60, "stories_viewed_per_day": 40,
                "time_on_feed_per_day": 80, "time_on_reels_per_day": 85,
                "likes_given_per_day": 45, "comments_written_per_day": 10,
                "notification_response_rate": 0.88,
                "expected_persona": "Doom-Scroller"
            },
            # Moderate User profile
            {
                "daily_active_minutes_instagram": 90, "sessions_per_day": 6,
                "reels_watched_per_day": 20, "stories_viewed_per_day": 15,
                "time_on_feed_per_day": 35, "time_on_reels_per_day": 30,
                "likes_given_per_day": 15, "comments_written_per_day": 4,
                "notification_response_rate": 0.6,
                "expected_persona": "Moderate User"
            },
            # Moderate User profile 2
            {
                "daily_active_minutes_instagram": 75, "sessions_per_day": 5,
                "reels_watched_per_day": 15, "stories_viewed_per_day": 12,
                "time_on_feed_per_day": 30, "time_on_reels_per_day": 25,
                "likes_given_per_day": 10, "comments_written_per_day": 3,
                "notification_response_rate": 0.5,
                "expected_persona": "Moderate User"
            },
            # Moderate User profile 3
            {
                "daily_active_minutes_instagram": 100, "sessions_per_day": 7,
                "reels_watched_per_day": 25, "stories_viewed_per_day": 20,
                "time_on_feed_per_day": 40, "time_on_reels_per_day": 35,
                "likes_given_per_day": 20, "comments_written_per_day": 5,
                "notification_response_rate": 0.65,
                "expected_persona": "Moderate User"
            },
            # Light User profile
            {
                "daily_active_minutes_instagram": 20, "sessions_per_day": 2,
                "reels_watched_per_day": 3, "stories_viewed_per_day": 5,
                "time_on_feed_per_day": 8, "time_on_reels_per_day": 5,
                "likes_given_per_day": 3, "comments_written_per_day": 1,
                "notification_response_rate": 0.2,
                "expected_persona": "Light User"
            },
            # Light User profile 2
            {
                "daily_active_minutes_instagram": 15, "sessions_per_day": 1,
                "reels_watched_per_day": 2, "stories_viewed_per_day": 3,
                "time_on_feed_per_day": 5, "time_on_reels_per_day": 3,
                "likes_given_per_day": 2, "comments_written_per_day": 0,
                "notification_response_rate": 0.15,
                "expected_persona": "Light User"
            },
            # Light User profile 3
            {
                "daily_active_minutes_instagram": 30, "sessions_per_day": 3,
                "reels_watched_per_day": 5, "stories_viewed_per_day": 8,
                "time_on_feed_per_day": 12, "time_on_reels_per_day": 8,
                "likes_given_per_day": 5, "comments_written_per_day": 2,
                "notification_response_rate": 0.3,
                "expected_persona": "Light User"
            },
            # Doom-Scroller profile 3 (extreme)
            {
                "daily_active_minutes_instagram": 230, "sessions_per_day": 20,
                "reels_watched_per_day": 100, "stories_viewed_per_day": 60,
                "time_on_feed_per_day": 100, "time_on_reels_per_day": 120,
                "likes_given_per_day": 80, "comments_written_per_day": 20,
                "notification_response_rate": 0.98,
                "expected_persona": "Doom-Scroller"
            },
            # Moderate User profile 4
            {
                "daily_active_minutes_instagram": 60, "sessions_per_day": 4,
                "reels_watched_per_day": 10, "stories_viewed_per_day": 10,
                "time_on_feed_per_day": 20, "time_on_reels_per_day": 20,
                "likes_given_per_day": 8, "comments_written_per_day": 2,
                "notification_response_rate": 0.45,
                "expected_persona": "Moderate User"
            },
        ]
        
        personas_list = ["Light User", "Moderate User", "Doom-Scroller"]
        
        for i, profile in enumerate(profiles):
            user = users[i % len(users)]
            
            # Full input data
            input_data = {
                "age": random.choice([18, 21, 24, 28, 32, 35, 40, 45]),
                "gender": random.choice(["Male", "Female"]),
                "country": "Vietnam",
                "urban_rural": random.choice(["Urban", "Rural"]),
                "income_level": random.choice(["Low", "Medium", "High"]),
                "employment_status": random.choice(["Student", "Full-time", "Part-time"]),
                "education_level": random.choice(["Bachelor", "Master", "High School"]),
                "relationship_status": random.choice(["Single", "In a relationship", "Married"]),
                "has_children": random.choice(["Yes", "No"]),
                "sleep_hours_per_night": round(random.uniform(5, 9), 1),
                "exercise_hours_per_week": round(random.uniform(0, 7), 1),
                "daily_steps_count": random.randint(2000, 12000),
                "diet_quality": random.choice(["Poor", "Average", "Good", "Excellent"]),
                "smoking": random.choice(["Yes", "No"]),
                "alcohol_frequency": random.choice(["Never", "Rarely", "Occasionally"]),
                "body_mass_index": round(random.uniform(18, 30), 1),
                "weekly_work_hours": round(random.uniform(20, 50), 0),
                "hobbies_count": random.randint(1, 5),
                "social_events_per_month": random.randint(1, 8),
                **{k: v for k, v in profile.items() if k != "expected_persona"}
            }
            
            # Scoring based on profile type
            expected = profile["expected_persona"]
            if expected == "Doom-Scroller":
                happiness_score = round(random.uniform(3.0, 5.5), 2)
                stress_score = round(random.uniform(6.5, 9.0), 2)
            elif expected == "Moderate User":
                happiness_score = round(random.uniform(5.0, 7.5), 2)
                stress_score = round(random.uniform(4.0, 6.5), 2)
            else:  # Light User
                happiness_score = round(random.uniform(6.5, 9.0), 2)
                stress_score = round(random.uniform(2.0, 4.5), 2)
            
            recommendations = [
                "Hãy duy trì lối sống lành mạnh",
                "Cân bằng giữa công việc và cuộc sống",
                "Tăng cường hoạt động thể chất",
            ]
            
            prediction = Prediction(
                user_id=user.id,
                timestamp=now - timedelta(minutes=random.randint(5, 120)),
                input_data=input_data,
                happiness_score=happiness_score,
                stress_score=stress_score,
                persona=expected,
                recommendations=recommendations
            )
            db.add(prediction)
            
        db.commit()
        
        # Show summary
        print("=" * 50)
        print("  Database seeded successfully!")
        print("=" * 50)
        print(f"  Users: 10 (2 admins + 8 users)")
        print(f"  Predictions: 10 (varied personas)")
        print(f"  Password for all: password123")
        print(f"  Admin accounts: user1_demo, user2_demo")
        print("=" * 50)
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_fake_data()
