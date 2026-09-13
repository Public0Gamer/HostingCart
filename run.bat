@echo off
title Hosting Wallah Cloud Platform
color 0B
echo ===================================================
echo           HOSTING WALLAH CLOUD PLATFORM
echo     Turnkey Web Hosting Business Engine
echo ===================================================
echo.

echo [1/3] Checking Python 3 environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3 is not found in PATH! Please install Python 3.12.
    pause
    exit /b
)

echo [2/3] Initializing SQLite database and verifying packages...
python -c "from models import init_db; init_db()"

echo [3/3] Launching Hosting Wallah Web Server on http://localhost:5000 ...
echo.
echo ---------------------------------------------------
echo  * Public Storefront:  http://localhost:5000/
echo  * Client hPanel:      http://localhost:5000/hpanel
echo  * Master WHM Admin:   http://localhost:5000/admin
echo.
echo  Official Master Admin: voltaramedia@gmail.com
echo  Support WhatsApp:      +91 9555838550
echo  UPI Payment ID:        pawan8550@naviaxis
echo ---------------------------------------------------
echo.
python app.py
pause
