from pydantic import BaseModel, Field
from typing import Optional


class UserInput(BaseModel):
    """Schema for user input data"""
    # Personal Information
    age: int = Field(..., ge=13, le=100, description="Age of the user")
    gender: str = Field(..., description="Gender (Male/Female/Other)")
    country: str = Field(..., description="Country of residence")
    urban_rural: str = Field(..., description="Urban or Rural")
    income_level: str = Field(..., description="Income level (Low/Medium/High)")
    employment_status: str = Field(..., description="Employment status")
    education_level: str = Field(..., description="Education level")
    relationship_status: str = Field(..., description="Relationship status")
    has_children: str = Field(..., description="Has children (Yes/No)")
    
    # Health Metrics
    sleep_hours_per_night: float = Field(..., ge=0, le=24, description="Hours of sleep per night")
    exercise_hours_per_week: float = Field(..., ge=0, description="Hours of exercise per week")
    daily_steps_count: int = Field(..., ge=0, description="Daily step count")
    diet_quality: str = Field(..., description="Diet quality (Poor/Average/Good/Excellent)")
    smoking: str = Field(..., description="Smoking status (Yes/No)")
    alcohol_frequency: str = Field(..., description="Alcohol frequency")
    body_mass_index: float = Field(..., ge=10, le=60, description="Body Mass Index")
    
    # Work & Social
    weekly_work_hours: float = Field(..., ge=0, description="Weekly work hours")
    hobbies_count: int = Field(..., ge=0, description="Number of hobbies")
    social_events_per_month: int = Field(..., ge=0, description="Social events per month")
    
    # Instagram Usage
    daily_active_minutes_instagram: float = Field(..., ge=0, description="Daily active minutes on Instagram")
    sessions_per_day: int = Field(..., ge=0, description="Instagram sessions per day")
    reels_watched_per_day: int = Field(..., ge=0, description="Reels watched per day")
    stories_viewed_per_day: int = Field(..., ge=0, description="Stories viewed per day")
    time_on_feed_per_day: float = Field(..., ge=0, description="Time on feed per day (minutes)")
    time_on_reels_per_day: float = Field(..., ge=0, description="Time on reels per day (minutes)")
    likes_given_per_day: int = Field(..., ge=0, description="Likes given per day")
    comments_written_per_day: int = Field(..., ge=0, description="Comments written per day")
    notification_response_rate: float = Field(..., ge=0, le=1, description="Notification response rate (0-1)")


class PredictionResponse(BaseModel):
    """Schema for prediction response"""
    happiness_score: float = Field(..., description="Predicted happiness score")
    stress_score: float = Field(..., description="Predicted stress score")
    persona: str = Field(..., description="User persona classification")
    recommendations: list[str] = Field(..., description="Personalized recommendations")


class HealthResponse(BaseModel):
    """Schema for health check response"""
    status: str
    message: str
