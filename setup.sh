#!/bin/bash

# Install dependencies
# echo "Installing dependencies..."
# sudo apt-get update
# sudo apt-get install -y python3

# Create a symbolic link
echo "Setting up wpt-mode..."
chmod +x wpt-mode.py
sudo ln -s "$(pwd)/wpt-mode.py" /usr/local/bin/wpt-mode

echo "Setup complete! wpt-mode"