# XLENS 🔍
> A powerful X (Twitter) analysis tool for sentiment analysis, fact-checking, and viral thread generation.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Node.js](https://img.shields.io/badge/node-18%2B-green)](https://nodejs.org/)

## 🌟 Features

- 📊 Sentiment Analysis of Tweets
- ✅ Fact Checking
- 🚀 Viral Thread Generation
- 🔄 Real-time X Integration

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- Node.js 18 or higher
- npm (comes with Node.js)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/XLENS.git
cd XLENS
```

### 2. Automated Setup (Windows)

Run the setup batch file:

```bash
setup.bat
```

Reference to setup script:

```1:76:setup.bat
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
```


### 3. Manual Setup

#### Backend Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
venv\Scripts\activate     # On Windows
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start the backend server:
```bash
python xlens/src/xlens/main.py
```

#### Frontend Setup

1. Install Node.js dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

## 🏗️ Project Structure

```
XLENS/
├── xlens/
│   └── src/
│       └── xlens/
│           ├── main.py          # FastAPI backend
│           ├── crews/           # AI crews
│           └── tools/           # Utility tools
├── src/
│   ├── components/              # React components
│   ├── pages/                   # Frontend pages
│   └── styles/                  # CSS styles
├── setup.bat                    # Windows setup script
├── requirements.txt             # Python dependencies
└── package.json                 # Node.js dependencies
```

## 🔧 Configuration

The application uses the following default ports:
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`

Reference to main backend configuration:

```12:21:XLENS/xlens/src/xlens/main.py
app = FastAPI(title="XLENS", description="APP for X Sentiment Analysis, Fact Checking, and Viral Thread Generation")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```


## 📦 Dependencies

### Backend Dependencies
- FastAPI
- uvicorn
- crewai
- pydantic

### Frontend Dependencies
Reference to package.json:

```12:18:XLENS/package.json
  "dependencies": {
    "axios": "^1.6.7",
    "lucide-react": "^0.344.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-router-dom": "^6.22.2"
  },
```


## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with FastAPI and React
- Powered by CrewAI for intelligent analysis
- Special thanks to all contributors

---
Made with ❤️ by XLENS team