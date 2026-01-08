# Unitree G1 3D Temperature Visualizer

A stunning, interactive 3D visualization dashboard for monitoring Unitree G1 robot motor temperatures in real-time. The dashboard renders the complete robot (29DOF with rubber hands) using actual STL models with dynamic temperature-based color gradients.

![G1 3D Visualizer](https://img.shields.io/badge/Status-Production-green) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- **🤖 Full 3D Robot Model**: Renders the complete G1 robot using actual STL mesh files from URDF
- **🌡️ Real-time Temperature Visualization**: Color-coded temperature gradients (blue = cold 30°C, red = hot 120°C)
- **🎮 Interactive Controls**: 
  - Orbit, zoom, and pan the 3D view
  - Click on robot parts to see detailed motor information
  - Auto-rotation mode
  - Wireframe toggle
- **📊 Live Statistics**: Real-time min/max/average temperature tracking
- **🎨 Modern UI**: Glassmorphism design with smooth animations
- **⚡ WebSocket Updates**: Real-time data streaming from the robot
- **🌐 Offline Support**: Works without internet - all dependencies served locally

## 🎬 Demo

The visualization displays all 29 motors of the G1 robot with:
- Surface temperature (external housing)
- Winding temperature (internal coil - typically hotter)
- Average temperature with smooth color gradients
- Interactive part selection for detailed motor info

## 📋 Prerequisites

- Python 3.8 or higher
- Unitree G1 robot (or test mode for development)
- Network connection to robot (for live data)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Autodiscovery/Unitree-G1-temperature-monitor
cd unitree-g1-temperature-monitor
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Unitree SDK2 Python

The Unitree SDK2 Python library is required to connect to the G1 robot:

```bash
# Clone the Unitree SDK2 Python repository
git clone https://github.com/unitreerobotics/unitree_sdk2_python.git

# Install the SDK
cd unitree_sdk2_python
pip install -e .
cd ..
```

**Note**: Make sure you have the correct network interface configured to communicate with your G1 robot.

### 4. Assets Included

✅ **All robot assets are included in this package!**

The visualizer comes with:
- URDF file: `assets/g1/g1_29dof_rev_1_0.urdf` (29DOF with rubber hands)
- STL meshes: `assets/g1/meshes/*.STL` (69 mesh files)
- JavaScript libraries: `assets/js/` (Three.js, Socket.IO, OrbitControls - for offline use)

No internet connection or additional asset downloads required - everything is ready to use!

## 🎯 Usage

### Quick Start (Test Mode)

Test the visualizer with simulated data (no robot connection needed):

```bash
python test_dashboard_3d.py
```

Then open your browser to: **http://localhost:8081**

### Production Mode (Real Robot)

Connect to a real G1 robot:

```bash
python dashboard_3d.py <network_interface>
```

Replace `<network_interface>` with your network interface name (e.g., `eth0`, `enp3s0`).

Example:
```bash
python dashboard_3d.py eth0
```

Then open your browser to: **http://localhost:8081**

## 🎮 Controls

| Action | Control |
|--------|---------|
| **Rotate Camera** | Left mouse button + drag |
| **Pan Camera** | Right mouse button + drag |
| **Zoom** | Mouse scroll wheel |
| **Select Motor** | Click on robot part |
| **Auto-Rotate** | Toggle button in controls panel |
| **Reset View** | Reset camera button |
| **Wireframe Mode** | Toggle wireframe button |

## 🌡️ Temperature Color Scale

The visualization uses a smooth gradient to represent motor temperatures:

| Temperature | Color | Status |
|------------|-------|--------|
| 30°C | 🔵 Blue | Cold / Idle |
| 45°C | 🟢 Green | Normal |
| 60°C | 🟡 Yellow | Warm |
| 75°C | 🟠 Orange | Hot |
| 90°C+ | 🔴 Red | Very Hot |
| 120°C | 🔴 Deep Red | Critical |

## 📁 Project Structure

```
unitree-g1-temperature-monitor/
├── dashboard_3d.py          # Main application (real robot data)
├── test_dashboard_3d.py     # Test version with simulated data
├── config.py                # Configuration and motor mappings
├── templates/
│   └── index_3d.html        # 3D visualization frontend
├── assets/
│   ├── js/                  # Local JavaScript libraries (offline support)
│   │   ├── socket.io.min.js
│   │   ├── three.min.js
│   │   ├── STLLoader.js
│   │   └── OrbitControls.js
│   └── g1/
│       ├── g1_29dof_rev_1_0.urdf    # Robot URDF file (29DOF rubber hands, from Unitree)
│       └── meshes/                   # STL mesh files (69 files, from Unitree)
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── INSTALL.md              # Quick installation guide
├── start.sh                # Startup script
└── PACKAGE.md              # Package overview
```

## 🔧 Technical Details

### Backend (Python/Flask)
- **Flask**: Web server framework
- **Flask-SocketIO**: Real-time WebSocket communication
- **unitree_sdk2py**: Robot data interface
- Serves STL files and URDF from assets directory
- Provides motor-to-mesh mapping API
- Runs on port 8081

### Frontend (JavaScript/Three.js)
- **Three.js**: 3D rendering engine (served locally)
- **STLLoader**: Loads robot mesh files (served locally)
- **OrbitControls**: Interactive camera controls (served locally)
- **Socket.IO**: Real-time data updates (served locally)
- URDF parsing for kinematic tree construction
- Dynamic material coloring based on temperature
- Raycasting for mesh selection
- **Offline capable**: All JavaScript dependencies bundled locally

### Motor-to-Mesh Mapping

The dashboard maps all 29 motors to their corresponding 3D mesh parts:

- **Legs (0-11)**: Hip, knee, ankle joints
- **Torso (12-14)**: Waist yaw/roll/pitch
- **Arms (15-28)**: Shoulder, elbow, wrist joints

Note: Hand palm links are structural components without motors/temperature sensors.

## 🐛 Troubleshooting

### STL Files Not Loading
- Check browser console for errors
- Verify the `assets/g1/meshes/` directory exists (should be included in package)
- Ensure file permissions allow reading

### No Temperature Data
- Check robot connection and network interface
- Verify `unitree_sdk2py` is installed correctly
- Try test mode first: `python test_dashboard_3d.py`
- Check that the robot is powered on and accessible

### Performance Issues
- Close other applications to free up resources
- Disable auto-rotate mode
- Use wireframe mode for better performance
- Reduce browser window size

### Connection Issues
- Ensure correct network interface is specified
- Check firewall settings
- Verify robot IP address is reachable
- Check that port 8081 is not already in use

## 🔒 Network Configuration

The dashboard communicates with the G1 robot over the network. Ensure:
1. Your computer is connected to the same network as the robot
2. The correct network interface is specified when running
3. Firewall allows connections on port 8081
4. The Unitree SDK2 is properly configured

### Environment Variables (Optional)

For enhanced security, you can set a custom Flask secret key:

```bash
export FLASK_SECRET_KEY="your-secret-key-here"
```

If not set, a random secret key will be generated automatically on each startup.

## 📝 Notes

- The dashboard runs on port **8081** (to avoid conflicts with other services)
- Temperature data includes both surface and winding temperatures
- The 3D model uses the official G1 URDF structure
- Color gradients are interpolated smoothly for visual appeal
- All 29 motors are monitored simultaneously

## 📧 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the browser console for errors
3. Ensure all dependencies are installed correctly
4. Verify robot connectivity

## 🙏 Acknowledgments

- Built with [Three.js](https://threejs.org/) for 3D rendering
- Uses [Flask](https://flask.palletsprojects.com/) and [Socket.IO](https://socket.io/) for real-time communication
- Integrates with [Unitree SDK2 Python](https://github.com/unitreerobotics/unitree_sdk2_python)
- **Robot assets** (URDF and STL mesh files) are provided by [Unitree Robotics](https://www.unitree.com/) as part of the G1 robot package

---

**Made with ❤️ for the Unitree G1 robotics community**
