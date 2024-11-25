#!/bin/bash

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed. Please install Python 3.x and try again."
    exit 1
fi

# Check Node.js installation
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed. Please install Node.js and try again."
    exit 1
fi

echo "Setting up backend..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating a new one..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install backend dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing backend dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Please add the file and try again."
    exit 1
fi

# Start backend server
echo "Starting backend server..."
python xlens/src/xlens/main.py &

echo "Setting up frontend..."

# Install frontend dependencies
echo "Installing frontend dependencies..."
npm install

# Run npm audit fix
echo "Running npm audit fix..."
npm audit fix || echo "Warning: npm audit fix encountered issues"

# Start frontend and open browser
echo "Starting frontend development server..."
npm run dev
(sleep 5 && open http://localhost:5173 || xdg-open http://localhost:5173 || start http://localhost:5173) &

echo "Setup complete! Both frontend and backend servers should be starting..."
