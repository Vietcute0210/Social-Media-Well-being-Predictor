"""
Model Training Script for Social Media Well-being Predictor
Trains all 3 ML models using the instagram_users_lifestyle.csv dataset
"""

import os
import json
import numpy as np
import pandas as pd
from joblib import dump
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans

# Configuration
CSV_PATH = "../instagram_users_lifestyle.csv"
MODELS_DIR = "models"
SAMPLE_SIZE = 50_000  # LIGHT: 50K rows for fast startup
RANDOM_SEED = 42

# Model hyperparameters (Optimized for speed/memory)
RF_N_ESTIMATORS = 50   # 50 trees
RF_MAX_DEPTH = 20      # Limit depth to prevent huge files

# Target variables
TARGET_STRESS = "perceived_stress_score"
TARGET_HAPPY = "self_reported_happiness"

# Features to use (matching notebook)
FEATURES = [
    # Demographics
    "age", "gender", "country", "urban_rural", "income_level",
    "employment_status", "education_level", "relationship_status", "has_children",
    
    # Lifestyle/health
    "sleep_hours_per_night", "exercise_hours_per_week", "daily_steps_count",
    "diet_quality", "smoking", "alcohol_frequency", "body_mass_index",
    "weekly_work_hours", "hobbies_count", "social_events_per_month",
    
    # Instagram usage
    "daily_active_minutes_instagram", "sessions_per_day",
    "reels_watched_per_day", "stories_viewed_per_day",
    "time_on_feed_per_day", "time_on_reels_per_day",
    "likes_given_per_day", "comments_written_per_day",
    "notification_response_rate",
]


def load_and_sample_data():
    """Load and sample dataset"""
    print(f"[1/7] Loading dataset from {CSV_PATH}...")
    
    # Read with chunking for large files
    chunks = []
    chunk_size = 100_000
    rows_read = 0
    
    for chunk in pd.read_csv(CSV_PATH, chunksize=chunk_size):
        need = SAMPLE_SIZE - rows_read
        if need <= 0:
            break
        take = min(len(chunk), need)
        chunks.append(chunk.sample(n=take, random_state=RANDOM_SEED))
        rows_read += take
    
    df = pd.concat(chunks, ignore_index=True)
    print(f"   Loaded {len(df)} rows")
    return df


def preprocess_data(df):
    """Clean and preprocess data"""
    print("[2/7] Preprocessing data...")
    
    # Clean data
    df = df.dropna(subset=[TARGET_STRESS, TARGET_HAPPY])
    df = df.drop_duplicates()

    # Filter unrealistic data (Outliers)
    # Cap usage at 4 hours (240 mins) to ensure "Moderate" classification is realistic
    if "daily_active_minutes_instagram" in df.columns:
        print(f"   Filtering outliers (usage > 240 mins)...")
        df = df[df["daily_active_minutes_instagram"] <= 240]
    
    # Convert Yes/No to 1/0
    yes_no_cols = ["has_children", "smoking"]
    for col in yes_no_cols:
        if col in df.columns:
            df[col] = df[col].map({"Yes": 1, "No": 0})
    
    # Keep only required features that exist
    available_features = [f for f in FEATURES if f in df.columns]
    
    X = df[available_features].copy()
    y_stress = df[TARGET_STRESS].copy()
    y_happy = df[TARGET_HAPPY].copy()
    
    print(f"   Features: {len(available_features)}")
    print(f"   Final dataset: {len(X)} rows")
    
    return X, y_stress, y_happy, available_features


def create_preprocessor(features, X):
    """Create preprocessing pipeline"""
    numeric_features = [f for f in features if pd.api.types.is_numeric_dtype(X[f])]
    categorical_features = [f for f in features if f not in numeric_features]
    
    print(f"   Numeric: {len(numeric_features)}")
    print(f"   Categorical: {len(categorical_features)}")
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ],
        remainder="drop"
    )
    
    return preprocessor


def train_models(X, y_stress, y_happy, features):
    """Train all 3 models"""
    print("[3/7] Training Stress model...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_stress, test_size=0.2, random_state=RANDOM_SEED
    )
    
    preprocessor = create_preprocessor(features, X)
    stress_pipeline = Pipeline([
        ("preprocess", preprocessor),
        ("model", RandomForestRegressor(
            n_estimators=RF_N_ESTIMATORS,
            max_depth=RF_MAX_DEPTH,
            random_state=RANDOM_SEED,
            n_jobs=-1,
            verbose=1
        ))
    ])
    stress_pipeline.fit(X_train, y_train)
    print(f"   Score: {stress_pipeline.score(X_test, y_test):.3f}")
    
    print("[4/7] Training Happiness model... ")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_happy, test_size=0.2, random_state=RANDOM_SEED
    )
    
    from sklearn.base import clone
    happiness_pipeline = Pipeline([
        ("preprocess", clone(preprocessor)),
        ("model", RandomForestRegressor(
            n_estimators=RF_N_ESTIMATORS,
            max_depth=RF_MAX_DEPTH,
            random_state=RANDOM_SEED,
            n_jobs=-1,
            verbose=1
        ))
    ])
    happiness_pipeline.fit(X_train, y_train)
    print(f"   Score: {happiness_pipeline.score(X_test, y_test):.3f}")
    
    print("[5/7] Training Persona model (KMeans)...")
    # For persona, we use KMeans clustering on Instagram usage patterns
    usage_features = [
        "daily_active_minutes_instagram", "sessions_per_day",
        "reels_watched_per_day", "stories_viewed_per_day",
        "time_on_feed_per_day", "time_on_reels_per_day",
        "likes_given_per_day", "comments_written_per_day",
        "notification_response_rate"
    ]
    X_usage = X[usage_features].fillna(0)
    
    persona_preprocessor = ColumnTransformer([
        ("scaler", StandardScaler(), usage_features)
    ])
    
    persona_pipeline = Pipeline([
        ("preprocess", persona_preprocessor),
        ("model", KMeans(n_clusters=3, random_state=RANDOM_SEED, n_init=10))
    ])
    persona_pipeline.fit(X_usage)
    
    # Create persona labels based on cluster centers
    clusters = persona_pipeline.predict(X_usage)
    usage_means = X['daily_active_minutes_instagram'].groupby(clusters).mean()
    sorted_clusters = usage_means.sort_values().index
    
    persona_labels = {}
    persona_labels[str(sorted_clusters[0])] = "Light User"
    persona_labels[str(sorted_clusters[1])] = "Moderate User" 
    persona_labels[str(sorted_clusters[2])] = "Doom-Scroller"
    
    print(f"   Clusters: {dict(usage_means)}")
    
    return stress_pipeline, happiness_pipeline, persona_pipeline, persona_labels, features


def save_models(stress_pipeline, happiness_pipeline, persona_pipeline, persona_labels, features):
    """Save all models and metadata"""
    print(f"[6/7] Saving models to {MODELS_DIR}/...")
    
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    dump(stress_pipeline, f"{MODELS_DIR}/stress_pipeline.joblib")
    dump(happiness_pipeline, f"{MODELS_DIR}/happiness_pipeline.joblib")
    dump(persona_pipeline, f"{MODELS_DIR}/persona_pipeline.joblib")
    
    with open(f"{MODELS_DIR}/features.json", "w") as f:
        json.dump(features, f, indent=2)
    
    with open(f"{MODELS_DIR}/persona_labels.json", "w") as f:
        json.dump(persona_labels, f, indent=2)
    
    print("   ✓ All models saved!")


def main():
    """Main training pipeline"""
    print("="*60)
    print("  Social Media Well-being Predictor - Model Training")
    print("="*60)
    print()
    
    # Load data
    df = load_and_sample_data()
    
    # Preprocess
    X, y_stress, y_happy, features = preprocess_data(df)
    
    # Train
    stress_pipeline, happiness_pipeline, persona_pipeline, persona_labels, features = train_models(
        X, y_stress, y_happy, features
    )
    
    # Save
    save_models(stress_pipeline, happiness_pipeline, persona_pipeline, persona_labels, features)
    
    print("[7/7] Training complete!")
    print()
    print("="*60)
    print("  Models ready for deployment!")
    print("="*60)


if __name__ == "__main__":
    main()
