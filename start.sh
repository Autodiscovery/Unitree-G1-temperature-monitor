#!/bin/bash

# Unitree G1 3D Temperature Visualizer - Quick Start Script

echo "=========================================="
echo "Unitree G1 3D Temperature Visualizer"
echo "=========================================="
echo ""

# Check if running in test mode or production mode
if [ "$1" == "test" ]; then
    echo "Starting in TEST MODE (simulated data)..."
    echo "No robot connection required."
    echo ""
    python3 test_dashboard_3d.py
elif [ -z "$1" ]; then
    echo "ERROR: Please specify network interface or 'test' mode"
    echo ""
    echo "Usage:"
    echo "  ./start.sh <network_interface>  # Connect to real robot"
    echo "  ./start.sh test                 # Run with simulated data"
    echo ""
    echo "Examples:"
    echo "  ./start.sh eth0"
    echo "  ./start.sh enp3s0"
    echo "  ./start.sh test"
    echo ""
    exit 1
else
    echo "Starting in PRODUCTION MODE..."
    echo "Connecting to G1 robot via interface: $1"
    echo ""
    python3 dashboard_3d.py "$1"
fi
