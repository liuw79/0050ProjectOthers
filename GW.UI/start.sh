#!/bin/bash

# Gaowei School UI Project - Quick Start Script
# Compatible with Mac/Linux systems

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "============================================================"
echo -e "${BLUE}   GAOWEI SCHOOL UI PROJECT - QUICK START${NC}"
echo "============================================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo -e "${RED}❌ Python is not installed${NC}"
        echo "   Please install Python 3.6+ and try again"
        echo "   Mac: brew install python3"
        echo "   Ubuntu: sudo apt install python3"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Check if HTML files exist
if [ ! -f "index.html" ] && [ ! -f "personal-center.html" ]; then
    echo -e "${RED}❌ No HTML files found in current directory${NC}"
    echo "   Please run this script in the project folder"
    exit 1
fi

echo -e "${GREEN}✅ Python detected${NC}"
echo -e "${GREEN}✅ Project files found${NC}"
echo
echo -e "${YELLOW}🚀 Starting development server...${NC}"
echo

# Make the script executable if needed
chmod +x "$0"

# Start the Python server
$PYTHON_CMD start_server.py 