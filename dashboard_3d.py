import sys
import time
import json
import os
import secrets
from threading import Thread, Lock
from flask import Flask, render_template, jsonify, send_from_directory
from flask_socketio import SocketIO

from unitree_sdk2py.core.channel import ChannelSubscriber, ChannelFactoryInitialize
from unitree_sdk2py.idl.unitree_hg.msg.dds_ import LowState_

from config import MOTOR_NAMES, MOTOR_TO_MESH, URDF_FILENAME, URDF_PATH, DEFAULT_PORT, DEFAULT_HOST

app = Flask(__name__)
# Use environment variable for secret key, fallback to random key for security
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(16))
socketio = SocketIO(app, cors_allowed_origins="*")

# Motor mappings imported from config.py

# Global variable to store latest motor data
motor_data = {
    'temperatures': [],
    'timestamp': 0
}
data_lock = Lock()


def low_state_callback(msg: LowState_):
    """Callback function to process received LowState data and update dashboard."""
    global motor_data
    
    if hasattr(msg, 'motor_state') and len(msg.motor_state) > 0:
        temps = []
        for i, motor in enumerate(msg.motor_state):
            # Only process motors 0-28 (29 actual motors with DOF)
            # Skip motors 29-34 as they don't physically exist (hand palm links have no motors)
            if i >= 29:
                continue
                
            if hasattr(motor, 'temperature') and len(motor.temperature) > 0:
                # Store both temperature values
                temps.append({
                    'motor_id': i,
                    'motor_name': MOTOR_NAMES.get(i, f'Motor {i}'),
                    'mesh_name': MOTOR_TO_MESH.get(i, ''),
                    'temp1': int(motor.temperature[0]),
                    'temp2': int(motor.temperature[1]),
                    'avg': (int(motor.temperature[0]) + int(motor.temperature[1])) / 2.0
                })
        
        with data_lock:
            motor_data['temperatures'] = temps
            motor_data['timestamp'] = time.time()
        
        # Emit data to all connected clients
        socketio.emit('motor_update', motor_data)


def init_robot_subscriber(network_interface=None):
    """Initialize the robot data subscriber."""
    print("Initializing robot connection...")
    
    if network_interface:
        ChannelFactoryInitialize(0, network_interface)
    else:
        ChannelFactoryInitialize(0)
    
    lowstate_subscriber = ChannelSubscriber("rt/lowstate", LowState_)
    lowstate_subscriber.Init(low_state_callback, 10)
    
    print("Robot subscriber initialized successfully!")


@app.route('/')
def index():
    """Serve the main 3D dashboard page."""
    return render_template('index_3d.html')


@app.route('/api/motors')
def get_motors():
    """API endpoint to get current motor data."""
    with data_lock:
        return jsonify(motor_data)


@app.route('/api/motor_mapping')
def get_motor_mapping():
    """API endpoint to get motor-to-mesh mapping."""
    return jsonify({
        'motor_names': MOTOR_NAMES,
        'motor_to_mesh': MOTOR_TO_MESH
    })


@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """Serve STL files and other assets."""
    import os
    assets_path = os.path.join(os.path.dirname(__file__), 'assets')
    return send_from_directory(assets_path, filename)


@app.route('/api/urdf')
def get_urdf():
    """Serve the URDF file for parsing."""
    urdf_path = os.path.join(os.path.dirname(__file__), URDF_PATH, URDF_FILENAME)
    try:
        with open(urdf_path, 'r') as f:
            return f.read(), 200, {'Content-Type': 'application/xml'}
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@app.route('/assets/js/<path:filename>')
def serve_js(filename):
    """Serve JavaScript files for offline support."""
    js_path = os.path.join(os.path.dirname(__file__), 'assets', 'js')
    return send_from_directory(js_path, filename)



def run_flask_app():
    """Run the Flask application."""
    socketio.run(app, host=DEFAULT_HOST, port=DEFAULT_PORT, debug=False)


def main():
    # Get network interface from command line if provided
    network_interface = sys.argv[1] if len(sys.argv) > 1 else None
    
    # Initialize robot subscriber
    try:
        init_robot_subscriber(network_interface)
    except Exception as e:
        print(f"Error initializing robot connection: {e}")
        print("Starting dashboard anyway (no live data will be available)")
    
    # Start Flask app
    print("\n" + "="*50)
    print("G1 3D Motor Temperature Dashboard")
    print("="*50)
    print(f"Dashboard available at: http://localhost:8081")
    print("Press Ctrl+C to exit")
    print("="*50 + "\n")
    
    try:
        run_flask_app()
    except KeyboardInterrupt:
        print("\nShutting down dashboard...")


if __name__ == "__main__":
    main()
