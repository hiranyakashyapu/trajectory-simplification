#!/bin/bash
# Virtual Environment Setup Script

echo "Setting up virtual environment for Trajectory Simplification Project..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

echo ""
echo "Virtual environment created and dependencies installed!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To deactivate, run:"
echo "  deactivate"

