from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List

from app.database import get_db
from app.models_db import User, Prediction

router = APIRouter(prefix="/admin", tags=["Admin"])

# Admin middleware
def require_admin(request: Request, db: Session = Depends(get_db)):
    """Middleware to check if user is admin"""
    username = request.cookies.get("user_session")
    if not username:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user = db.query(User).filter(User.username == username).first()
    if not user or user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return user

@router.get("/stats")
def get_admin_stats(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Get global statistics for admin dashboard"""
    
    # Total users
    total_users = db.query(func.count(User.id)).scalar()
    
    # Total predictions
    total_predictions = db.query(func.count(Prediction.id)).scalar()
    
    # Average scores
    avg_happiness = db.query(func.avg(Prediction.happiness_score)).scalar() or 0
    avg_stress = db.query(func.avg(Prediction.stress_score)).scalar() or 0
    
    # Active users today
    today = datetime.utcnow().date()
    active_today = db.query(func.count(func.distinct(Prediction.user_id)))\
        .filter(func.date(Prediction.timestamp) == today)\
        .scalar()
    
    # Predictions this week
    week_ago = datetime.utcnow() - timedelta(days=7)
    predictions_this_week = db.query(func.count(Prediction.id))\
        .filter(Prediction.timestamp >= week_ago)\
        .scalar()
    
    # Persona distribution
    persona_distribution = db.query(
        Prediction.persona,
        func.count(Prediction.id).label('count')
    ).group_by(Prediction.persona).all()
    
    persona_dist = {
        persona: count for persona, count in persona_distribution
    }
    
    return {
        "total_users": total_users,
        "total_predictions": total_predictions,
        "avg_happiness": round(float(avg_happiness), 2),
        "avg_stress": round(float(avg_stress), 2),
        "active_users_today": active_today,
        "predictions_this_week": predictions_this_week,
        "persona_distribution": persona_dist
    }

@router.get("/users")
def get_all_users(
    admin: User = Depends(require_admin), 
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Get list of all users with their stats"""
    
    users = db.query(User).offset(skip).limit(limit).all()
    
    users_data = []
    for user in users:
        prediction_count = db.query(func.count(Prediction.id))\
            .filter(Prediction.user_id == user.id)\
            .scalar()
        
        last_prediction = db.query(Prediction)\
            .filter(Prediction.user_id == user.id)\
            .order_by(Prediction.timestamp.desc())\
            .first()
        
        users_data.append({
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "prediction_count": prediction_count,
            "last_prediction": last_prediction.timestamp.isoformat() if last_prediction else None
        })
    
    return {
        "total": db.query(func.count(User.id)).scalar(),
        "users": users_data
    }

@router.get("/predictions")
def get_all_predictions(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    """Get recent predictions from all users"""
    
    predictions = db.query(Prediction)\
        .order_by(Prediction.timestamp.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    predictions_data = []
    for pred in predictions:
        user = db.query(User).filter(User.id == pred.user_id).first()
        
        predictions_data.append({
            "id": pred.id,
            "username": user.username if user else "Unknown",
            "timestamp": pred.timestamp.isoformat(),
            "happiness_score": pred.happiness_score,
            "stress_score": pred.stress_score,
            "persona": pred.persona
        })
    
    return {
        "total": db.query(func.count(Prediction.id)).scalar(),
        "predictions": predictions_data
    }

@router.get("/trends")
def get_prediction_trends(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
    days: int = 30
):
    """Get prediction trends for the last N days"""
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    # Daily prediction counts
    daily_predictions = db.query(
        func.date(Prediction.timestamp).label('date'),
        func.count(Prediction.id).label('count'),
        func.avg(Prediction.happiness_score).label('avg_happiness'),
        func.avg(Prediction.stress_score).label('avg_stress')
    ).filter(Prediction.timestamp >= cutoff_date)\
     .group_by(func.date(Prediction.timestamp))\
     .order_by(func.date(Prediction.timestamp))\
     .all()
    
    trends = []
    for date, count, avg_h, avg_s in daily_predictions:
        trends.append({
            "date": str(date),
            "count": count,
            "avg_happiness": round(float(avg_h), 2) if avg_h else 0,
            "avg_stress": round(float(avg_s), 2) if avg_s else 0
        })
    
    return {"trends": trends}

@router.get("/top-users")
def get_top_users(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
    limit: int = 10
):
    """Get top users by prediction count"""
    
    top_users = db.query(
        User.username,
        func.count(Prediction.id).label('prediction_count'),
        func.avg(Prediction.happiness_score).label('avg_happiness'),
        func.avg(Prediction.stress_score).label('avg_stress')
    ).join(Prediction, User.id == Prediction.user_id)\
     .group_by(User.id, User.username)\
     .order_by(func.count(Prediction.id).desc())\
     .limit(limit)\
     .all()
    
    users_list = []
    for username, count, avg_h, avg_s in top_users:
        users_list.append({
            "username": username,
            "prediction_count": count,
            "avg_happiness": round(float(avg_h), 2) if avg_h else 0,
            "avg_stress": round(float(avg_s), 2) if avg_s else 0
        })
    
    return {"top_users": users_list}
