@echo off
echo ========================================
echo  Social Media Well-being Predictor
echo  Frontend Launcher
echo ========================================
echo.

cd /d "%~dp0frontend"

echo Starting frontend server...
echo Frontend will run at: http://localhost:3000
echo.
echo Make sure the backend is running at: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

python -m http.server 3000

pause
