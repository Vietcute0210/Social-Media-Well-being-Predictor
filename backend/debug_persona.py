import joblib
import pandas as pd
import json
from pathlib import Path

# Load pipeline and labels
model_dir = Path("models")
persona_pipeline = joblib.load(model_dir / "persona_pipeline.joblib")
with open(model_dir / "persona_labels.json", "r") as f:
    labels = json.load(f)

print(f"Loaded labels: {labels}")

# Define features used for clustering
# Must match train_models.py usage_features
usage_features = [
    "daily_active_minutes_instagram", "sessions_per_day",
    "reels_watched_per_day", "stories_viewed_per_day",
    "time_on_feed_per_day", "time_on_reels_per_day",
    "likes_given_per_day", "comments_written_per_day",
    "notification_response_rate"
]

# Create test cases
test_cases = [
    # Case 1: Low usage
    {
        "daily_active_minutes_instagram": 10,
        "sessions_per_day": 2,
        "reels_watched_per_day": 5,
        "stories_viewed_per_day": 5,
        "time_on_feed_per_day": 5,
        "time_on_reels_per_day": 5,
        "likes_given_per_day": 2,
        "comments_written_per_day": 0,
        "notification_response_rate": 0.1
    },
    # Case 2: High usage (should be Doom-Scroller)
    {
        "daily_active_minutes_instagram": 300, # 5 hours
        "sessions_per_day": 50,
        "reels_watched_per_day": 100,
        "stories_viewed_per_day": 100,
        "time_on_feed_per_day": 150,
        "time_on_reels_per_day": 150,
        "likes_given_per_day": 100,
        "comments_written_per_day": 50,
        "notification_response_rate": 0.9
    },
    # Case 3: Mixed (High Time, Low Interaction - likely what user is doing)
    {
        "daily_active_minutes_instagram": 300, # 5 hours
        "sessions_per_day": 5,                 # Defaults
        "reels_watched_per_day": 10,
        "stories_viewed_per_day": 20,
        "time_on_feed_per_day": 30,
        "time_on_reels_per_day": 30,
        "likes_given_per_day": 15,
        "comments_written_per_day": 3,
        "notification_response_rate": 0.5
    },
    # Case 4: Moderate Usage (2.5 hours, moderate interaction)
    {
        "daily_active_minutes_instagram": 150, # 2.5 hours
        "sessions_per_day": 15,
        "reels_watched_per_day": 30,
        "stories_viewed_per_day": 30,
        "time_on_feed_per_day": 60,
        "time_on_reels_per_day": 60,
        "likes_given_per_day": 20,
        "comments_written_per_day": 10,
        "notification_response_rate": 0.5
    }
]

print("\nTesting Predictions:")
for i, data in enumerate(test_cases):
    df = pd.DataFrame([data])
    # The pipeline expects all columns used in training? 
    # Actually train_models.py only fits on usage_features for persona_pipeline
    # But let's check input requirement. 
    # In train_models.py: 
    # persona_preprocessor = ColumnTransformer([("scaler", StandardScaler(), usage_features)])
    # So it only cares about these columns.
    
    cluster = persona_pipeline.predict(df)[0]
    persona = labels.get(str(cluster), "Unknown")
    print(f"Case {i+1} (Minutes: {data['daily_active_minutes_instagram']}): Cluster {cluster} -> {persona}")

# Check Cluster Centers
# print("\nCluster Centers (Scaled):")
# try:
#     centers = persona_pipeline.named_steps['model'].cluster_centers_
#     print(centers)
# except:
#     print("Could not retrieve cluster centers")
