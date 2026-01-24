from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    """User model for authentication"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user", nullable=False)  # 'admin' or 'user'
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship
    predictions = relationship("Prediction", back_populates="user", cascade="all, delete-orphan")

class Prediction(Base):
    """Prediction model for storing user prediction history"""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Input data (stored as JSON)
    input_data = Column(JSON)
    
    # Output results
    happiness_score = Column(Float)
    stress_score = Column(Float)
    persona = Column(String)
    recommendations = Column(JSON)
    
    # Relationship
    user = relationship("User", back_populates="predictions")
