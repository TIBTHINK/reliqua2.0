#!/bin/bash

# Check if script is run with sudo (except on macOS where it's usually not needed)
if [[ "$(uname)" != "Darwin" ]] && [ "$(id -u)" -ne 0 ]; then
  echo "This script requires sudo. Please run as root."
  exit 1
fi

# Function to install python3 and pip for Debian-based systems
install_debian() {
  echo "Debian/Ubuntu detected. Ensuring required packages are installed..."
  to_install=()
  if ! command -v python3 &> /dev/null; then
    to_install+=(python3)
  fi
  if ! command -v pip3 &> /dev/null; then
    to_install+=(python3-pip)
  fi
  if ! command -v patchelf &> /dev/null; then
    to_install+=(patchelf)
  fi
  if [ ${#to_install[@]} -gt 0 ]; then
    apt update
    apt install -y "${to_install[@]}" || {
      echo "Failed to install packages on Debian/Ubuntu."
      exit 1
    }
  else
    echo "All required system packages are already installed."
  fi
}

# Function to install python3 and pip for Arch-based systems
install_arch() {
  echo "Arch Linux detected. Ensuring required packages are installed..."
  to_install=()
  if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    to_install+=(python)
  fi
  if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    to_install+=(python-pip)
  fi
  if ! command -v patchelf &> /dev/null; then
    to_install+=(patchelf)
  fi
  if [ ${#to_install[@]} -gt 0 ]; then
    pacman -Syu --noconfirm "${to_install[@]}" || {
      echo "Failed to install packages on Arch Linux."
      exit 1
    }
  else
    echo "All required system packages are already installed."
  fi
}

# Function to install python3 and pip on macOS
install_macos() {
  echo "macOS detected. Installing python3 and pip..."
  if ! command -v brew &> /dev/null; then
    echo "Homebrew is not installed. Please install Homebrew from https://brew.sh and re-run this script."
    exit 1
  fi
  to_install=()
  if ! command -v python3 &> /dev/null; then
    to_install+=(python)
  fi
  if ! command -v patchelf &> /dev/null; then
    to_install+=(patchelf)
  fi
  if [ ${#to_install[@]} -gt 0 ]; then
    brew update
    brew install "${to_install[@]}" || {
      echo "Failed to install packages via Homebrew."
      exit 1
    }
  else
    echo "All required system packages are already installed."
  fi
}

install_python_tools() {
  if [ -f /etc/debian_version ]; then
    install_debian
  elif [ -f /etc/arch-release ]; then
    install_arch
  elif [[ "$(uname)" == "Darwin" ]]; then
    install_macos
  else
    echo "Unsupported operating system. Please install python3, pip, and patchelf manually."
    exit 1
  fi
}

# Ensure required system packages are present (install missing ones)
echo "Ensuring required system packages (python3/pip3/patchelf) are installed..."
install_python_tools

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
