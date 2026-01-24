-- Migration script to add role and created_at columns to users table
-- Run this in PostgreSQL to fix the login error

-- Add role column with default 'user'
ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR DEFAULT 'user' NOT NULL;

-- Update existing admindeptrai user to admin role (if exists)
UPDATE users SET role = 'admin' WHERE username = 'admindeptrai';

-- Add created_at column
ALTER TABLE users ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL;

-- Verify changes
SELECT column_name, data_type FROM information_schema.columns 
WHERE table_name = 'users';
