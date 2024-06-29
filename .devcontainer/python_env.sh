#!/bin/bash

arg1=$1

# Create a virtual environment named 'venv'
python3 -m venv /venv

# Activate the virtual environment
source /venv/bin/activate

# Install dependencies from requirements.txt
pip install --no-cache-dir -r $arg1