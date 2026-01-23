#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if .venv exists, create if not
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv .venv
fi

# Activate virtual environment
if [ -z "$VIRTUAL_ENV" ] || [[ "$VIRTUAL_ENV" != *".venv"* ]]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
else
    echo "Virtual environment already active: $VIRTUAL_ENV"
fi

# Check if dependencies are installed
echo "Checking dependencies..."
if ! command -v uvicorn &> /dev/null; then
    echo "Dependencies missing. Installing..."
    pip install -r requirements.txt
else
    # Ensure all requirements are met; pip install is fast if already satisfied.
    pip install -r requirements.txt --quiet
fi

# Start the server
echo "Starting LamiNode backend..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
