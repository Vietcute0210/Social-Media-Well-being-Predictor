import joblib
import pandas as pd
import numpy as np
import json
from pathlib import Path

# Load pipeline and labels
model_dir = Path("models")
persona_pipeline = joblib.load(model_dir / "persona_pipeline.joblib")

# 1. Get the Scaler and KMeans model
# Pipeline steps: [('preprocess', ColumnTransformer), ('model', KMeans)]
# ColumnTransformer transformers: [('scaler', StandardScaler, usage_features)]

preprocessor = persona_pipeline.named_steps['preprocess']
kmeans = persona_pipeline.named_steps['model']

# Get the scaler from the ColumnTransformer
# it's named 'scaler' inside the transformer list
scaler = preprocessor.named_transformers_['scaler']

# Get Cluster Centers (these are Scaled values)
centers_scaled = kmeans.cluster_centers_

# 2. Inverse Transform to get Real Values
centers_real = scaler.inverse_transform(centers_scaled)

# 3. Get Feature Names
# The usage features were defined in train_models.py. 
# We can try to access them if stored, or hardcode the ordered list matching training
usage_features = [
    "daily_active_minutes_instagram", "sessions_per_day",
    "reels_watched_per_day", "stories_viewed_per_day",
    "time_on_feed_per_day", "time_on_reels_per_day",
    "likes_given_per_day", "comments_written_per_day",
    "notification_response_rate"
]

# 4. Map Clusters to Labels
with open(model_dir / "persona_labels.json", "r") as f:
    labels_map = json.load(f)

print("="*60)
print("DATA-DRIVEN CLUSTER ANALYSIS")
print("="*60)

# Create a DataFrame for nice display
df_centers = pd.DataFrame(centers_real, columns=usage_features)
df_centers['Cluster_ID'] = df_centers.index
df_centers['Label'] = df_centers['Cluster_ID'].apply(lambda x: labels_map.get(str(x), "Unknown"))

# Reorder columns
cols = ['Label', 'Cluster_ID'] + usage_features
df_centers = df_centers[cols]

# Sort by daily_active_minutes_instagram to see progression
df_centers = df_centers.sort_values('daily_active_minutes_instagram')

print(df_centers.T)

print("\n" + "="*60)
print("THRESHOLDS CALCULATION")
print("="*60)

# Calculate midpoints for Daily Active Minutes
# We assume the sorted order is Light -> Moderate -> Doom
sorted_centers = df_centers['daily_active_minutes_instagram'].values
labels_sorted = df_centers['Label'].values

print(f"Center 1 ({labels_sorted[0]}): {sorted_centers[0]:.2f} minutes")
print(f"Center 2 ({labels_sorted[1]}): {sorted_centers[1]:.2f} minutes")
print(f"Center 3 ({labels_sorted[2]}): {sorted_centers[2]:.2f} minutes")

# Midpoints (Decision Boundaries)
threshold_light_mod = (sorted_centers[0] + sorted_centers[1]) / 2
threshold_mod_doom = (sorted_centers[1] + sorted_centers[2]) / 2

print(f"\nCalculated Boundaries:")
print(f"Light User      < {threshold_light_mod:.2f} mins")
print(f"Moderate User   : {threshold_light_mod:.2f} - {threshold_mod_doom:.2f} mins")
print(f"Doom Scroller   > {threshold_mod_doom:.2f} mins")
