#!/bin/bash

# Check if script is run with sudo
if [ "$(id -u)" -ne 0 ]; then
  echo "This script requires sudo. Please run as root."
  exit 1
fi

# Function to install python3 and pip for Debian-based systems (e.g., Ubuntu)
install_debian() {
  echo "Debian/Ubuntu detected. Installing python3 and pip..."
  apt update
  apt install -y python3 python3-pip
}

# Function to install python3 and pip for Arch-based systems
install_arch() {
  echo "Arch Linux detected. Installing python3 and pip..."
  pacman -Syu --noconfirm python python-pip
}

# Check if python3 and pip are installed
if ! command -v python3 &> /dev/null; then
  echo "python3 not found. Installing..."
  if [ -f /etc/debian_version ]; then
    install_debian
  elif [ -f /etc/arch-release ]; then
    install_arch
  else
    echo "Unsupported distribution. Please install python3 manually."
    exit 1
  fi
else
  echo "python3 is already installed."
fi

if ! command -v pip3 &> /dev/null; then
  echo "pip3 not found. Installing..."
  if [ -f /etc/debian_version ]; then
    apt install -y python3-pip
  elif [ -f /etc/arch-release ]; then
    pacman -Syu --noconfirm python-pip
  else
    echo "Unsupported distribution. Please install pip3 manually."
    exit 1
  fi
else
  echo "pip3 is already installed."
fi

# Install Python requirements from a text file
if [ -f "requirements.txt" ]; then
  echo "Installing requirements from requirements.txt..."
  pip3 install -r requirements.txt
else
  echo "requirements.txt not found."
  exit 1
fi

echo "Script completed successfully."
