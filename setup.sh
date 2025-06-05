#!/bin/bash

# Check if script is run with sudo (except on macOS where it's usually not needed)
if [[ "$(uname)" != "Darwin" ]] && [ "$(id -u)" -ne 0 ]; then
  echo "This script requires sudo. Please run as root."
  exit 1
fi

# Function to install python3 and pip for Debian-based systems
install_debian() {
  echo "Debian/Ubuntu detected. Installing python3 and pip..."
  apt update && apt install -y python3 python3-pip || {
    echo "Failed to install packages on Debian/Ubuntu."
    exit 1
  }
}

# Function to install python3 and pip for Arch-based systems
install_arch() {
  echo "Arch Linux detected. Installing python3 and pip..."
  pacman -Syu --noconfirm python python-pip || {
    echo "Failed to install packages on Arch Linux."
    exit 1
  }
}

# Function to install python3 and pip on macOS
install_macos() {
  echo "macOS detected. Installing python3 and pip..."
  if ! command -v brew &> /dev/null; then
    echo "Homebrew is not installed. Please install Homebrew from https://brew.sh and re-run this script."
    exit 1
  fi
  brew update && brew install python || {
    echo "Failed to install Python via Homebrew."
    exit 1
  }
}

# Install Python tools based on OS
install_python_tools() {
  if [ -f /etc/debian_version ]; then
    install_debian
  elif [ -f /etc/arch-release ]; then
    install_arch
  elif [[ "$(uname)" == "Darwin" ]]; then
    install_macos
  else
    echo "Unsupported operating system. Please install python3 and pip manually."
    exit 1
  }
}

# Check and install python3/pip3
if ! command -v python3 &> /dev/null || ! command -v pip3 &> /dev/null; then
  echo "python3 or pip3 not found. Installing..."
  install_python_tools
else
  echo "python3 and pip3 are already installed."
fi

# Install Python requirements
if [ -f "requirements.txt" ]; then
  echo "Installing requirements from requirements.txt..."
  /usr/bin/env pip3 install -r requirements.txt || {
    echo "Failed to install requirements."
    exit 1
  }
else
  echo "requirements.txt not found."
  exit 1
fi

echo "Script completed successfully."
