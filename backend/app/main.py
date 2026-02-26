from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from app.schemas import UserInput, PredictionResponse, HealthResponse
from app.ml.loader import ModelLoader
from app.ml.predictor import Predictor
from app.utils import encode_categorical_features, validate_input_ranges
from app.routers import auth, predictions, admin
from app.database import engine, Base, get_db, SessionLocal
from app.models_db import User, Prediction, vn_now
from sqlalchemy.orm import Session


# Global variables for models
predictor = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup: Load models
    global predictor
    print("🚀 Starting Social Media Well-being Predictor API...")
    
    # Create database tables
    print("🗄️  Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")
    
    # Warm up database connection to avoid cold start
    print("🔌 Warming up database connection...")
    try:
        db_warmup = SessionLocal()
        db_warmup.query(User).first()
        db_warmup.close()
        print("✓ Database connection warm-up complete")
    except Exception as e:
        print(f"⚠ Database warm-up warning: {str(e)} (will retry on first request)")
    
    try:
        loader = ModelLoader(models_dir="models")
        loader.load_models()
        models = loader.get_models()
        predictor = Predictor(models)
        print("✓ Models loaded and ready for predictions")
    except Exception as e:
        print(f"✗ Failed to load models: {str(e)}")
        raise e
    
    print("🟢 Server is ready!")
    
    yield
    
    # Shutdown
    print("👋 Shutting down API...")


# Initialize FastAPI app
app = FastAPI(
    title="Social Media Well-being Predictor API",
    description="API for predicting happiness, stress levels, and user personas based on social media usage and lifestyle factors",
    version="1.0.0",
    lifespan=lifespan
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication router
app.include_router(auth.router)

# Include predictions router
app.include_router(predictions.router)

# Include admin router
app.include_router(admin.router)


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check"""
    return HealthResponse(
        status="success",
        message="Social Media Well-being Predictor API is running"
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    if predictor is None:
        raise HTTPException(status_code=503, detail="Models not loaded yet")
    
    return HealthResponse(
        status="healthy",
        message="All systems operational"
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict_wellbeing(user_input: UserInput, request: Request):
    """
    Predict happiness, stress, and persona based on user input
    (Requires authentication)
    
    Args:
        user_input: UserInput object containing all required features
    
    Returns:
        PredictionResponse with happiness score, stress score, persona, and recommendations
    """
    # Check authentication
    username = request.cookies.get("user_session")
    if not username:
        raise HTTPException(status_code=401, detail="Please login to use this feature")
    
    if predictor is None:
        raise HTTPException(
            status_code=503, 
            detail="Models not loaded. Please try again later."
        )
    
    try:
        # Convert Pydantic model to dict
        user_data = user_input.model_dump()
        
        # Validate input ranges
        is_valid, error_msg = validate_input_ranges(user_data)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Encode categorical features
        encoded_data = encode_categorical_features(user_data)
        
        # Make prediction
        prediction = predictor.predict(encoded_data)
        
        # Save prediction to database
        db_gen = get_db()
        db = next(db_gen)
        try:
            # Get user
            user = db.query(User).filter(User.username == username).first()
            if user:
                db_prediction = Prediction(
                    user_id=user.id,
                    timestamp=vn_now(),
                    input_data=user_data,
                    happiness_score=prediction["happiness_score"],
                    stress_score=prediction["stress_score"],
                    persona=prediction["persona"],
                    recommendations=prediction["recommendations"]
                )
                db.add(db_prediction)
                db.commit()
        finally:
            db.close()
        
        return PredictionResponse(**prediction)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@app.get("/features")
async def get_features():
    """Get list of required features for prediction"""
    if predictor is None:
        raise HTTPException(status_code=503, detail="Models not loaded yet")
    
    return {
        "features": predictor.features,
        "total_features": len(predictor.features)
    }


@app.get("/personas")
async def get_personas():
    """Get available persona labels"""
    if predictor is None:
        raise HTTPException(status_code=503, detail="Models not loaded yet")
    
    return {
        "personas": list(set(predictor.persona_labels.values())),
        "persona_mapping": predictor.persona_labels
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
