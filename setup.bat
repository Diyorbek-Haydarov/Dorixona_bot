@echo off
REM PharmaGuide Bot Setup Script for Windows
REM This script sets up the complete environment for the PharmaGuide Bot

echo 🚀 PharmaGuide Bot Setup Script
echo ================================

REM Check if Python is installed
echo [INFO] Checking Python version...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is required but not installed
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)
echo [SUCCESS] Python found

REM Check if pip is installed
echo [INFO] Checking pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pip is required but not installed
    pause
    exit /b 1
)
echo [SUCCESS] pip found

REM Create virtual environment
echo [INFO] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo [SUCCESS] Virtual environment created
) else (
    echo [WARNING] Virtual environment already exists
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
echo [SUCCESS] Virtual environment activated

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip
echo [SUCCESS] pip upgraded

REM Install requirements
echo [INFO] Installing Python packages...
pip install -r requirements.txt
echo [SUCCESS] All packages installed

REM Create .env file if it doesn't exist
echo [INFO] Setting up environment configuration...
if not exist ".env" (
    copy .env.example .env
    echo [SUCCESS] .env file created from template
    echo [WARNING] Please edit .env file with your bot token and other settings
) else (
    echo [WARNING] .env file already exists
)

REM Initialize database
echo [INFO] Initializing database...
python -c "import asyncio; import sys; import os; sys.path.append(os.path.dirname(os.path.abspath('.'))); from bot.database import db; asyncio.run(db.init_db()); print('Database initialized successfully')"
echo [SUCCESS] Database initialized

REM Create admin user
echo [INFO] Creating admin user...
python init_admin.py
echo [SUCCESS] Admin user created

REM Ask if user wants to add sample data
echo.
set /p add_sample="Do you want to add sample data? (y/n): "
if /i "%add_sample%"=="y" (
    echo [INFO] Adding sample data...
    python sample_data.py
    echo [SUCCESS] Sample data added
)

REM Create run scripts
echo [INFO] Creating run scripts...

REM Bot run script
echo @echo off > run_bot.bat
echo call venv\Scripts\activate.bat >> run_bot.bat
echo python run_bot.py >> run_bot.bat
echo pause >> run_bot.bat

REM Admin run script
echo @echo off > run_admin.bat
echo call venv\Scripts\activate.bat >> run_admin.bat
echo python run_admin.py >> run_admin.bat
echo pause >> run_admin.bat

echo [SUCCESS] Run scripts created

REM Final instructions
echo.
echo 🎉 Setup completed successfully!
echo ================================
echo.
echo Next steps:
echo 1. Edit .env file with your bot token and settings
echo 2. Start the bot: run_bot.bat
echo 3. Start admin panel: run_admin.bat
echo 4. Open admin panel: http://localhost:5000
echo.
echo Default admin credentials:
echo Username: admin
echo Password: admin123
echo.
echo ⚠️  Remember to change the default admin password!
echo.
echo For help, check README.md or QUICKSTART.md
echo.
echo [SUCCESS] Setup complete! 🚀
pause
