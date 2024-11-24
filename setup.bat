@echo off

:: Check if Python is installed
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python is not installed. Please install Python 3.x and try again.
    exit /b
)

:: Check if Node.js is installed
node --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Node.js is not installed. Please install Node.js and try again.
    exit /b
)

echo Setting up backend...

:: Check if the virtual environment folder exists
if not exist venv (
    echo Virtual environment not found. Creating a new one...
    python -m venv venv
    if ERRORLEVEL 1 (
        echo Failed to create virtual environment.
        exit /b
    )
)

:: Upgrade pip
echo Upgrading pip...
venv\Scripts\python -m pip install --upgrade pip
if ERRORLEVEL 1 (
    echo Failed to upgrade pip.
    exit /b
)

:: Install backend dependencies
if exist requirements.txt (
    echo Installing backend dependencies from requirements.txt...
    venv\Scripts\python -m pip install -r requirements.txt
    if ERRORLEVEL 1 (
        echo Failed to install backend dependencies.
        exit /b
    )
) else (
    echo requirements.txt not found. Please add the file and try again.
    exit /b
)

:: Run backend
echo Starting backend server...
start venv\Scripts\python xlens.src.xlens.main.py

echo Setting up frontend...

:: Install frontend dependencies
echo Installing frontend dependencies...
npm install
if ERRORLEVEL 1 (
    echo Failed to install frontend dependencies.
    exit /b
)

:: Run npm audit fix
echo Running npm audit fix...
npm audit fix
if ERRORLEVEL 1 (
    echo Warning: npm audit fix encountered issues
)

:: Start frontend development server
echo Starting frontend development server...
start npm run dev

echo Setup complete! Both frontend and backend servers should be starting...
pause
