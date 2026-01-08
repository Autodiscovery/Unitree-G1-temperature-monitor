import sys
import time
import json
from threading import Thread, Lock
from flask import Flask, render_template, jsonify, send_from_directory
from flask_socketio import SocketIO

from unitree_sdk2py.core.channel import ChannelSubscriber, ChannelFactoryInitialize
from unitree_sdk2py.idl.unitree_hg.msg.dds_ import LowState_

app = Flask(__name__)
app.config['SECRET_KEY'] = 'unitree-g1-3d-dashboard'
socketio = SocketIO(app, cors_allowed_origins="*")

# Motor ID to name mapping for G1 robot (35 motors total)
MOTOR_NAMES = {
    0: "Left Hip Pitch",
    1: "Left Hip Roll",
    2: "Left Hip Yaw",
    3: "Left Knee",
    4: "Left Ankle Pitch",
    5: "Left Ankle Roll",
    6: "Right Hip Pitch",
    7: "Right Hip Roll",
    8: "Right Hip Yaw",
    9: "Right Knee",
    10: "Right Ankle Pitch",
    11: "Right Ankle Roll",
    12: "Waist Yaw",
    13: "Waist Roll",
    14: "Waist Pitch",
    15: "Left Shoulder Pitch",
    16: "Left Shoulder Roll",
    17: "Left Shoulder Yaw",
    18: "Left Elbow",
    19: "Left Wrist Roll",
    20: "Left Wrist Pitch",
    21: "Left Wrist Yaw",
    22: "Right Shoulder Pitch",
    23: "Right Shoulder Roll",
    24: "Right Shoulder Yaw",
    25: "Right Elbow",
    26: "Right Wrist Roll",
    27: "Right Wrist Pitch",
    28: "Right Wrist Yaw",
    # Additional motors (likely hands/grippers)
    29: "Left Hand Motor 1",
    30: "Left Hand Motor 2",
    31: "Left Hand Motor 3",
    32: "Right Hand Motor 1",
    33: "Right Hand Motor 2",
    34: "Right Hand Motor 3",
}

# Motor ID to mesh link name mapping (based on URDF structure)
MOTOR_TO_MESH = {
    0: "left_hip_pitch_link",
    1: "left_hip_roll_link",
    2: "left_hip_yaw_link",
    3: "left_knee_link",
    4: "left_ankle_pitch_link",
    5: "left_ankle_roll_link",
    6: "right_hip_pitch_link",
    7: "right_hip_roll_link",
    8: "right_hip_yaw_link",
    9: "right_knee_link",
    10: "right_ankle_pitch_link",
    11: "right_ankle_roll_link",
    12: "waist_yaw_link",
    13: "waist_roll_link",
    14: "torso_link",  # waist_pitch is part of torso
    15: "left_shoulder_pitch_link",
    16: "left_shoulder_roll_link",
    17: "left_shoulder_yaw_link",
    18: "left_elbow_link",
    19: "left_wrist_roll_link",
    20: "left_wrist_pitch_link",
    21: "left_wrist_yaw_link",
    22: "right_shoulder_pitch_link",
    23: "right_shoulder_roll_link",
    24: "right_shoulder_yaw_link",
    25: "right_elbow_link",
    26: "right_wrist_roll_link",
    27: "right_wrist_pitch_link",
    28: "right_wrist_yaw_link",
    # Hand motors - map to hand palm links
    29: "left_hand_palm_link",
    30: "left_hand_palm_link",
    31: "left_hand_palm_link",
    32: "right_hand_palm_link",
    33: "right_hand_palm_link",
    34: "right_hand_palm_link",
}

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
    import os
    urdf_path = os.path.join(os.path.dirname(__file__), 'assets', 'g1', 'g1_body29_hand14.urdf')
    try:
        with open(urdf_path, 'r') as f:
            return f.read(), 200, {'Content-Type': 'application/xml'}
    except Exception as e:
        return jsonify({'error': str(e)}), 404



def run_flask_app():
    """Run the Flask application."""
    socketio.run(app, host='0.0.0.0', port=8081, debug=False, allow_unsafe_werkzeug=True)


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
