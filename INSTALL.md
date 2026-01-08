# Installation and Setup

## Quick Install

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install Unitree SDK2 Python
git clone https://github.com/unitreerobotics/unitree_sdk2_python.git
cd unitree_sdk2_python
pip install -e .
cd ..

# 3. Run the visualizer
./start.sh test  # Test mode with simulated data
# OR
./start.sh eth0  # Production mode (replace eth0 with your network interface)
```

## What's Included

✅ **All robot assets are included!**
- URDF file and 69 STL mesh files in `assets/g1/` (provided by Unitree Robotics)
- No additional downloads required

## Detailed Setup

See [README.md](README.md) for complete installation instructions and troubleshooting.
