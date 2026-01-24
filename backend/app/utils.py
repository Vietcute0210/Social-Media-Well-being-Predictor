from typing import Dict, Any
import pandas as pd


def encode_categorical_features(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert numeric fields to proper types (float/int)
    Categorical fields are kept as-is since the model pipeline handles encoding
    """
    encoded_data = user_data.copy()
    
    # Numeric features that should be float
    numeric_float_fields = [
        "age", "sleep_hours_per_night", "exercise_hours_per_week",
        "daily_steps_count", "body_mass_index", "weekly_work_hours",
        "hobbies_count", "social_events_per_month",
        "daily_active_minutes_instagram", "sessions_per_day",
        "reels_watched_per_day", "stories_viewed_per_day",
        "time_on_feed_per_day", "time_on_reels_per_day",
        "likes_given_per_day", "comments_written_per_day",
        "notification_response_rate"
    ]
    
    # Convert numeric fields to float, handling None/null values
    for field in numeric_float_fields:
        if field in encoded_data:
            value = encoded_data[field]
            if value is None or value == '':
                encoded_data[field] = 0.0
            else:
                try:
                    encoded_data[field] = float(value)
                except (ValueError, TypeError):
                    encoded_data[field] = 0.0
    
    # Boolean fields (Yes/No) - convert to 1/0
    yes_no_fields = ["has_children", "smoking"]
    for field in yes_no_fields:
        if field in encoded_data:
            if isinstance(encoded_data[field], str):
                encoded_data[field] = 1 if encoded_data[field].lower() in ['yes', 'true', '1'] else 0
            elif encoded_data[field] is None:
                encoded_data[field] = 0
    
    # Categorical fields are kept as strings - the pipeline will handle encoding
    # Examples: gender, country, urban_rural, income_level, employment_status,
    # education_level, relationship_status, diet_quality, smoking, alcohol_frequency
    
    return encoded_data



def validate_input_ranges(user_data: Dict[str, Any]) -> tuple[bool, str]:
    """
    Validate that input values are within acceptable ranges
    Returns (is_valid, error_message)
    """
    validations = [
        (user_data.get("age", 0) >= 13 and user_data.get("age", 0) <= 100, 
         "Age must be between 13 and 100"),
        (user_data.get("sleep_hours_per_night", 0) >= 0 and user_data.get("sleep_hours_per_night", 24) <= 24,
         "Sleep hours must be between 0 and 24"),
        (user_data.get("body_mass_index", 0) >= 10 and user_data.get("body_mass_index", 60) <= 60,
         "BMI must be between 10 and 60"),
        (user_data.get("notification_response_rate", 0) >= 0 and user_data.get("notification_response_rate", 1) <= 1,
         "Notification response rate must be between 0 and 1"),
    ]
    
    for is_valid, error_msg in validations:
        if not is_valid:
            return False, error_msg
    
    return True, ""
