"""
Database Migration Script
Adds role and created_at columns to users table
Run this with: python run_migration.py
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine
from sqlalchemy import text

def run_migration():
    """Execute migration to add role and created_at columns"""
    
    print("🔄 Starting database migration...")
    
    with engine.connect() as conn:
        try:
            # Start transaction
            trans = conn.begin()
            
            # Add role column
            print("➕ Adding 'role' column...")
            conn.execute(text(
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR DEFAULT 'user' NOT NULL"
            ))
            
            # Update admindeptrai to admin
            print("👑 Setting admindeptrai as admin...")
            result = conn.execute(text(
                "UPDATE users SET role = 'admin' WHERE username = 'admindeptrai'"
            ))
            print(f"   Updated {result.rowcount} user(s)")
            
            # Add created_at column
            print("➕ Adding 'created_at' column...")
            conn.execute(text(
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL"
            ))
            
            # Commit transaction
            trans.commit()
            print("✅ Migration completed successfully!")
            
            # Verify
            print("\n📊 Verifying changes...")
            result = conn.execute(text(
                "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'users' ORDER BY column_name"
            ))
            
            print("\nUsers table columns:")
            for row in result:
                print(f"  - {row[0]}: {row[1]}")
            
            print("\n✅ Database is ready!")
            return True
            
        except Exception as e:
            trans.rollback()
            print(f"❌ Migration failed: {str(e)}")
            return False

if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)
