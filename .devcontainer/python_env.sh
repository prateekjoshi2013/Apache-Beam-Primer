#!/bin/bash

arg1=$1

source /venv/bin/activate

# Install dependencies from requirements.txt
pip install --no-cache-dir -r $arg1