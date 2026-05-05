#!/bin/bash

# Kali AI Assistant - Installation Script
# This script installs the Kali AI Assistant on Kali Linux

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}"
echo "╔════════════════════════════════════════════╗"
echo "║   🐲 KALI AI ASSISTANT INSTALLER 🐲      ║"
echo "║     Powered by Groq                        ║"
echo "╚════════════════════════════════���═══════════╝"
echo -e "${NC}"

# Check if running on Kali
if [[ ! -f /etc/os-release ]] || ! grep -q "Kali" /etc/os-release; then
    echo -e "${YELLOW}⚠ Warning: This doesn't appear to be Kali Linux${NC}"
    echo -e "${YELLOW}Continue anyway? (y/n)${NC}"
    read -r response
    if [[ "$response" != "y" ]]; then
        echo -e "${RED}Installation cancelled${NC}"
        exit 1
    fi
fi

# Check Python version
echo -e "${GREEN}✓ Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 is required but not installed${NC}"
    echo -e "${GREEN}Installing Python 3...${NC}"
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-venv
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Python ${PYTHON_VERSION} found${NC}"

# Create project directory if not already here
if [ ! -d "src" ]; then
    echo -e "${RED}✗ src directory not found${NC}"
    echo -e "${YELLOW}Please run this script from the kali-ai-assistant directory${NC}"
    exit 1
fi

# Create virtual environment
echo -e "${GREEN}✓ Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${GREEN}✓ Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${GREEN}✓ Upgrading pip...${NC}"
pip install --upgrade pip setuptools wheel

# Install system dependencies
echo -e "${GREEN}✓ Installing system dependencies...${NC}"
sudo apt-get update
sudo apt-get install -y \
    python3-dev \
    portaudio19-dev \
    libportaudio2 \
    flac \
    espeak

echo -e "${GREEN}✓ System dependencies installed${NC}"

# Install Python requirements
echo -e "${GREEN}✓ Installing Python dependencies...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✓ Python dependencies installed${NC}"

# Setup environment file
echo -e "${GREEN}✓ Setting up configuration...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠ Please edit .env file and add your Groq API key${NC}"
    echo -e "${YELLOW}  Get it at: https://console.groq.com${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

# Create symbolic link for easy access
echo -e "${GREEN}✓ Creating command alias...${NC}"
if ! command -v kali-ai &> /dev/null; then
    SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
    echo "alias kali-ai='cd $SCRIPT_DIR && source venv/bin/activate && python3 -m src.main'" >> ~/.bashrc
    echo -e "${GREEN}✓ Alias created! Reload shell with: source ~/.bashrc${NC}"
fi

# Create cache directory
mkdir -p .cache
echo -e "${GREEN}✓ Cache directory created${NC}"

# Test installation
echo -e "${GREEN}✓ Testing installation...${NC}"
python3 -c "from src.groq_integration import GroqClient; from src.cache_manager import CacheManager; from src.voice_handler import VoiceHandler" && echo -e "${GREEN}✓ All modules loaded successfully${NC}" || echo -e "${RED}✗ Module loading failed${NC}"

echo -e "\n${GREEN}"
echo "╔════════════════════════════════════════════╗"
echo "║      ✓ Installation Complete! ✓           ║"
echo "╚════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${GREEN}Next steps:${NC}"
echo -e "  1. Edit .env file: ${YELLOW}nano .env${NC}"
echo -e "  2. Add your Groq API key${NC}"
echo -e "  3. Run the assistant: ${YELLOW}python3 -m src.main${NC}"
echo -e "  4. Or use alias: ${YELLOW}kali-ai${NC}"
echo ""
echo -e "${GREEN}Quick start:${NC}"
echo -e "  ${YELLOW}source venv/bin/activate${NC}"
echo -e "  ${YELLOW}python3 -m src.main${NC}"
echo ""
echo -e "${GREEN}For help:${NC}"
echo -e "  ${YELLOW}python3 -m src.main --help${NC}"
echo ""
