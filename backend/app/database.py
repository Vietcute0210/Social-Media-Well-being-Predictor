import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection string
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres.phcxgkqkajycovkhbhwe:Matkhau20262027%40@aws-1-ap-northeast-2.pooler.supabase.com:6543/postgres"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,        # Test connection before using, prevents "first click" failures
    pool_size=5,               # Maintain 5 connections in the pool
    max_overflow=10,           # Allow up to 10 extra connections
    pool_recycle=300,          # Recycle connections every 5 minutes (Supabase may close idle ones)
    pool_timeout=30,           # Wait up to 30s for a connection from pool
    connect_args={
        "connect_timeout": 15,  # 15 second timeout for initial connection (Supabase cold start)
        "options": "-c statement_timeout=30000"  # 30s query timeout
    }
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency for database sessions"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
