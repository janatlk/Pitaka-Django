@echo off
echo ========================================
echo Starting PITAKA Django Development Server
echo ========================================
echo.

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Run development server
echo Starting server at http://127.0.0.1:8000
echo Press Ctrl+C to stop
echo.
python manage.py runserver
