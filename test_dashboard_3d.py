#!/usr/bin/env python3
"""
Test script for the 3D dashboard with simulated motor data.
This allows testing the visualization without a real robot connection.
"""

import sys
import time
import random
from threading import Thread
from flask import Flask, render_template, jsonify, send_from_directory
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'unitree-g1-3d-dashboard-test'
socketio = SocketIO(app, cors_allowed_origins="*")

# Motor ID to name mapping for G1 robot (35 motors total)
MOTOR_NAMES = {
    0: "Left Hip Pitch", 1: "Left Hip Roll", 2: "Left Hip Yaw", 3: "Left Knee",
    4: "Left Ankle Pitch", 5: "Left Ankle Roll", 6: "Right Hip Pitch", 7: "Right Hip Roll",
    8: "Right Hip Yaw", 9: "Right Knee", 10: "Right Ankle Pitch", 11: "Right Ankle Roll",
    12: "Waist Yaw", 13: "Waist Roll", 14: "Waist Pitch", 15: "Left Shoulder Pitch",
    16: "Left Shoulder Roll", 17: "Left Shoulder Yaw", 18: "Left Elbow", 19: "Left Wrist Roll",
    20: "Left Wrist Pitch", 21: "Left Wrist Yaw", 22: "Right Shoulder Pitch", 23: "Right Shoulder Roll",
    24: "Right Shoulder Yaw", 25: "Right Elbow", 26: "Right Wrist Roll", 27: "Right Wrist Pitch",
    28: "Right Wrist Yaw", 29: "Left Hand Motor 1", 30: "Left Hand Motor 2", 31: "Left Hand Motor 3",
    32: "Right Hand Motor 1", 33: "Right Hand Motor 2", 34: "Right Hand Motor 3",
}

# Motor ID to mesh link name mapping
MOTOR_TO_MESH = {
    0: "left_hip_pitch_link", 1: "left_hip_roll_link", 2: "left_hip_yaw_link", 3: "left_knee_link",
    4: "left_ankle_pitch_link", 5: "left_ankle_roll_link", 6: "right_hip_pitch_link", 7: "right_hip_roll_link",
    8: "right_hip_yaw_link", 9: "right_knee_link", 10: "right_ankle_pitch_link", 11: "right_ankle_roll_link",
    12: "waist_yaw_link", 13: "waist_roll_link", 14: "torso_link", 15: "left_shoulder_pitch_link",
    16: "left_shoulder_roll_link", 17: "left_shoulder_yaw_link", 18: "left_elbow_link", 19: "left_wrist_roll_link",
    20: "left_wrist_pitch_link", 21: "left_wrist_yaw_link", 22: "right_shoulder_pitch_link", 23: "right_shoulder_roll_link",
    24: "right_shoulder_yaw_link", 25: "right_elbow_link", 26: "right_wrist_roll_link", 27: "right_wrist_pitch_link",
    28: "right_wrist_yaw_link", 29: "left_hand_palm_link", 30: "left_hand_palm_link", 31: "left_hand_palm_link",
    32: "right_hand_palm_link", 33: "right_hand_palm_link", 34: "right_hand_palm_link",
}

motor_data = {'temperatures': [], 'timestamp': 0}

def generate_simulated_data():
    """Generate simulated motor temperature data."""
    temps = []
    for i in range(35):
        # Simulate temperatures between 35°C and 115°C
        base_temp = 40 + random.uniform(0, 60)
        temp1 = int(base_temp + random.uniform(-5, 5))
        temp2 = int(base_temp + random.uniform(0, 10))  # Winding usually hotter
        
        temps.append({
            'motor_id': i,
            'motor_name': MOTOR_NAMES.get(i, f'Motor {i}'),
            'mesh_name': MOTOR_TO_MESH.get(i, ''),
            'temp1': temp1,
            'temp2': temp2,
            'avg': (temp1 + temp2) / 2.0
        })
    
    return {'temperatures': temps, 'timestamp': time.time()}

def update_loop():
    """Continuously update and broadcast simulated data."""
    while True:
        global motor_data
        motor_data = generate_simulated_data()
        socketio.emit('motor_update', motor_data)
        time.sleep(1)  # Update every second

@app.route('/')
def index():
    return render_template('index_3d.html')

@app.route('/api/motors')
def get_motors():
    return jsonify(motor_data)

@app.route('/api/motor_mapping')
def get_motor_mapping():
    return jsonify({'motor_names': MOTOR_NAMES, 'motor_to_mesh': MOTOR_TO_MESH})

@app.route('/assets/<path:filename>')
def serve_assets(filename):
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


if __name__ == "__main__":
    print("\n" + "="*60)
    print("G1 3D Temperature Dashboard - TEST MODE")
    print("="*60)
    print("Running with SIMULATED data (no robot connection needed)")
    print(f"Dashboard available at: http://localhost:8081")
    print("Press Ctrl+C to exit")
    print("="*60 + "\n")
    
    # Start update thread
    update_thread = Thread(target=update_loop, daemon=True)
    update_thread.start()
    
    # Generate initial data
    motor_data = generate_simulated_data()
    
    # Run Flask app
    socketio.run(app, host='0.0.0.0', port=8081, debug=False, allow_unsafe_werkzeug=True)
