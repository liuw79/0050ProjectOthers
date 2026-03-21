#!/bin/bash
# OpenClaw EvoMap Integration - Evolver Startup Script
#
# Usage:
#   ./start.sh           # Run once
#   ./start.sh --loop    # Run in loop mode (daemon)
#
# Node ID: node_620d226ef4e6
# Hub URL: https://evomap.ai

cd "$(dirname "$0")"

# Load environment
export $(grep -v '^#' .env | xargs)

echo "============================================"
echo "  OpenClaw EvoMap Evolver"
echo "============================================"
echo "Node ID: $(node -e "require('dotenv').config(); const {getNodeId}=require('./src/gep/a2aProtocol'); console.log(getNodeId())")"
echo "Hub URL: $A2A_HUB_URL"
echo "============================================"

# Run evolver
if [ "$1" == "--loop" ]; then
    echo "Starting in LOOP mode..."
    node index.js --loop
else
    echo "Running single evolution cycle..."
    node index.js run
fi
