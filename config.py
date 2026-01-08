"""
Configuration file for G1 Temperature Monitor Dashboard
Contains motor mappings, constants, and configuration settings
"""

# Motor ID to name mapping for G1 robot (29 motors = 29 DOF)
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
}

# Motor ID to mesh link name mapping (based on URDF structure)
# Maps each of the 29 motors to their corresponding visual mesh link
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
}

# Temperature thresholds (in Celsius)
TEMP_MIN = 30
TEMP_MAX = 120
TEMP_WARM_THRESHOLD = 45
TEMP_HOT_THRESHOLD = 60

# URDF configuration
URDF_FILENAME = "g1_29dof_rev_1_0.urdf"  # 29DOF with rubber hands
URDF_PATH = "assets/g1"

# Network configuration
DEFAULT_PORT = 8081
DEFAULT_HOST = "0.0.0.0"
