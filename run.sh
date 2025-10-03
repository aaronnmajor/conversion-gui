#!/bin/bash
# Run the Conversion GUI application

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the application
python main.py
