import numpy as np
from collections import deque

def calculate_jump_height(baseline_hip_y, hip_y, frame_height, scale_factor):
    elevation_px = (baseline_hip_y - hip_y) * frame_height
    return elevation_px * scale_factor

def calculate_arm_speed(wrist_history: deque, scale_factor, fps):
    if len(wrist_history) < 2:
        return 0
    speeds = []
    for i in range(len(wrist_history)-1):
        dist_px = np.linalg.norm(wrist_history[i+1] - wrist_history[i])
        dist_m = dist_px * scale_factor / 100
        speeds.append(dist_m * fps)
    return max(speeds) if speeds else 0
