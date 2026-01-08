# G1 3D Visualizer - Package Contents

This standalone package contains everything needed to run the Unitree G1 3D temperature visualization dashboard.

## 📦 Package Contents

```
unitree-g1-temperature-monitor/
├── dashboard_3d.py          # Main application (connects to real G1 robot)
├── test_dashboard_3d.py     # Test version with simulated data
├── templates/
│   └── index_3d.html        # 3D visualization frontend (Three.js)
├── assets/
│   └── g1/
│       ├── g1_body29_hand14.urdf    # Robot URDF file (from Unitree)
│       └── meshes/                   # STL mesh files (69 files, from Unitree)
├── requirements.txt         # Python dependencies
├── README.md               # Complete documentation
├── INSTALL.md              # Quick installation guide
├── PACKAGE.md              # This file
├── SUMMARY.md              # Package summary
└── start.sh                # Startup script
```

## 🚀 Quick Start

### Test Mode (No Robot Required)
```bash
./start.sh test
```

### Production Mode (Real Robot)
```bash
./start.sh eth0  # Replace eth0 with your network interface
```

Then open: **http://localhost:8081**

## 📋 Requirements

- Python 3.8+
- Flask & Flask-SocketIO (see requirements.txt)
- unitree_sdk2py (for robot connection)
- ✅ **Robot assets included** (STL files and URDF in `assets/g1/`)

## 📚 Documentation

- **README.md** - Complete documentation with features, installation, usage, and troubleshooting
- **INSTALL.md** - Quick installation guide

## 🎯 Features

✅ Full 3D robot model from STL files  
✅ Real-time temperature visualization with color gradients  
✅ Interactive 3D controls (rotate, zoom, pan, click)  
✅ WebSocket live updates  
✅ Modern glassmorphism UI  
✅ Test mode with simulated data  

## 🔗 Dependencies

The package requires the Unitree SDK2 Python library to connect to the robot. Installation instructions are in README.md.

## 📝 Notes

- Runs on port 8081
- ✅ **All assets included** in `assets/g1/` folder
- Monitors all 35 motors
- Displays surface and winding temperatures
- Color scale: 30°C (blue) to 120°C (red)

---

For complete documentation, see [README.md](README.md)
