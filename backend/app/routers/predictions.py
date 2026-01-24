from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models_db import Prediction, User
from pydantic import BaseModel

router = APIRouter(prefix="/predictions", tags=["Predictions"])

# Pydantic schemas
class PredictionResponse(BaseModel):
    id: int
    timestamp: datetime
    happiness_score: float
    stress_score: float
    persona: str
    recommendations: List[str]
    input_data: dict
    
    class Config:
        from_attributes = True

class StatsResponse(BaseModel):
    total_predictions: int
    average_happiness: float
    average_stress: float
    most_common_persona: str
    persona_distribution: dict

def get_current_user_id(request: Request, db: Session) -> int:
    """Helper to get current user ID from session cookie"""
    username = request.cookies.get("user_session")
    if not username:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user.id

@router.get("/history", response_model=List[PredictionResponse])
def get_prediction_history(
    request: Request,
    db: Session = Depends(get_db),
    limit: int = 100
):
    """Get user's prediction history"""
    user_id = get_current_user_id(request, db)
    
    predictions = db.query(Prediction).filter(
        Prediction.user_id == user_id
    ).order_by(
        Prediction.timestamp.desc()
    ).limit(limit).all()
    
    return predictions

@router.get("/stats", response_model=StatsResponse)
def get_user_stats(
    request: Request,
    db: Session = Depends(get_db)
):
    """Get user's statistics"""
    user_id = get_current_user_id(request, db)
    
    predictions = db.query(Prediction).filter(
        Prediction.user_id == user_id
    ).all()
    
    if not predictions:
        return StatsResponse(
            total_predictions=0,
            average_happiness=0,
            average_stress=0,
            most_common_persona="N/A",
            persona_distribution={}
        )
    
    # Calculate averages
    avg_happiness = sum(p.happiness_score for p in predictions) / len(predictions)
    avg_stress = sum(p.stress_score for p in predictions) / len(predictions)
    
    # Calculate persona distribution
    persona_counts = {}
    for p in predictions:
        persona_counts[p.persona] = persona_counts.get(p.persona, 0) + 1
    
    most_common = max(persona_counts, key=persona_counts.get)
    
    return StatsResponse(
        total_predictions=len(predictions),
        average_happiness=round(avg_happiness, 1),
        average_stress=round(avg_stress, 1),
        most_common_persona=most_common,
        persona_distribution=persona_counts
    )

@router.delete("/{prediction_id}")
def delete_prediction(
    prediction_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Delete a specific prediction"""
    user_id = get_current_user_id(request, db)
    
    prediction = db.query(Prediction).filter(
        Prediction.id == prediction_id,
        Prediction.user_id == user_id
    ).first()
    
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    
    db.delete(prediction)
    db.commit()
    
    return {"message": "Prediction deleted successfully"}

@router.delete("/all")
def delete_all_predictions(
    request: Request,
    db: Session = Depends(get_db)
):
    """Delete all user's predictions"""
    user_id = get_current_user_id(request, db)
    
    count = db.query(Prediction).filter(
        Prediction.user_id == user_id
    ).delete()
    
    db.commit()
    
    return {"message": f"Deleted {count} predictions"}
