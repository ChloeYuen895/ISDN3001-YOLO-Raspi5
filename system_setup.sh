#!/bin/bash

# Update package lists
sudo apt update || { echo "Failed to update package lists"; exit 1; }

# Install camera and multimedia tools
sudo apt install -y ffmpeg v4l-utils || { echo "Failed to install ffmpeg or v4l-utils"; exit 1; }

# Check Python version
python3 --version || { echo "Python3 not found"; exit 1; }

# Create and activate virtual environment
python3 -m venv --system-site-packages .venv || { echo "Failed to create virtual environment"; exit 1; }
source .venv/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }

pip install -r requirements.txt || { echo "Failed to install Python packages"; exit 1; }