#!/bin/bash

# Ensure script runs with sudo if needed for creating the symlink
if [ "$EUID" -ne 0 ]; then
    SUDO="sudo"
else
    SUDO=""
fi

echo "Setting up wpt-mode..."

# Check required dependencies
echo "Checking dependencies..."
for cmd in python3 ip iw nmcli; do
    if ! command -v "$cmd" &> /dev/null; then
        echo "[-] Warning: '$cmd' is not installed or not in PATH."
    fi
done

# Create a symbolic link
chmod +x wpt-mode.py
$SUDO ln -sf "$(pwd)/wpt-mode.py" /usr/local/bin/wpt-mode

echo "Setup complete! You can now run 'wpt-mode'."
