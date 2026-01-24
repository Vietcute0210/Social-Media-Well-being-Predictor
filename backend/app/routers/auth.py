from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
import bcrypt
from pydantic import BaseModel

from app.database import get_db
from app.models_db import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Pydantic schemas
class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

@router.post("/register")
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if username exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Determine role (all new users are 'user' by default)
    role = "user"
    
    # Create new user
    hashed_pw = hash_password(user_data.password)
    new_user = User(
        username=user_data.username, 
        hashed_password=hashed_pw,
        role=role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "message": "User registered successfully", 
        "username": new_user.username,
        "role": new_user.role
    }

@router.post("/login")
def login(user_data: UserLogin, response: Response, db: Session = Depends(get_db)):
    """Login user"""
    # Hardcoded admin check
    if user_data.username == "admindeptrai" and user_data.password == "123456":
        # Admin login - check if admin user exists in DB
        admin_user = db.query(User).filter(User.username == "admindeptrai").first()
        if not admin_user:
            # Create admin user if not exists
            hashed_pw = hash_password("123456")
            admin_user = User(
                username="admindeptrai",
                hashed_password=hashed_pw,
                role="admin"
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
        else:
            # Update role to admin if user exists but isn't admin
            if admin_user.role != "admin":
                admin_user.role = "admin"
                db.commit()
        
        # Set session cookie
        response.set_cookie(
            key="user_session",
            value=admin_user.username,
            httponly=True,
            max_age=3600 * 24  # 24 hours
        )
        
        return {
            "message": "Login successful",
            "username": admin_user.username,
            "role": admin_user.role,
            "user_id": admin_user.id
        }
    
    # Regular user login
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Set session cookie
    response.set_cookie(
        key="user_session",
        value=user.username,
        httponly=True,
        max_age=3600 * 24  # 24 hours
    )
    
    return {
        "message": "Login successful",
        "username": user.username,
        "role": user.role,
        "user_id": user.id
    }

@router.post("/logout")
def logout(response: Response):
    """Logout user"""
    response.delete_cookie("user_session")
    return {"message": "Logged out successfully"}

@router.get("/me")
def get_current_user(request: Request, db: Session = Depends(get_db)):
    """Get current logged in user with role"""
    username = request.cookies.get("user_session")
    if not username:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Get user from database to return full info including role
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return {
        "username": user.username,
        "role": user.role,
        "user_id": user.id
    }
