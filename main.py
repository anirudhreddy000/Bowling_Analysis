import numpy as np
from collections import deque
import cv2
import mediapipe as mp
from modules.video_capture import load_video, resize_frame
from modules.pose_detector import init_pose, get_pose_landmarks
from modules.analytics import calculate_jump_height, calculate_arm_speed
from modules.visualization import draw_pose, draw_motion_trail, draw_info_box, draw_header, draw_border
from modules.effects import apply_vignette

mp_pose = mp.solutions.pose

# --- Setup ---
cap, fps, w, h = load_video("videos/archer .mp4")
pose_model = init_pose()
baseline_hip_y = None
max_elevation_px = 0
display_jump_height = 0
display_arm_speed = 0
prev_hip_y = None
WRIST_HISTORY = deque(maxlen=4)
ARM_MOVEMENT_THRESHOLD = 0.5
record_arm_speed = False
landing_detected = False
landing_frame = None
prev_ankle_y = None
arm_speeds = []

# --- Setup VideoWriter to save output ---
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(r'output\output.mp4', fourcc, fps, (w, h))

# --- Main Loop ---
frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = resize_frame(frame, w, h)
    frame_count += 1

    landmarks = get_pose_landmarks(frame, pose_model)
    if landmarks:
        # Hip
        left_hip_y = landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP.value].y
        right_hip_y = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP.value].y
        hip_y = (left_hip_y + right_hip_y) / 2
        if prev_hip_y is not None:
            hip_y = 0.2 * hip_y + 0.8 * prev_hip_y
        prev_hip_y = hip_y

        # Ankles
        left_ankle_y = landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE.value].y * h
        right_ankle_y = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y * h
        avg_ankle_y = (left_ankle_y + right_ankle_y) / 2

        # Scale factor
        pixel_height = abs(landmarks.landmark[mp_pose.PoseLandmark.NOSE.value].y -
                           landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE.value].y) * h
        scale_factor = 188 / pixel_height if pixel_height > 0 else 0.45

        # Baseline hip
        if baseline_hip_y is None:
            baseline_hip_y = hip_y

        # Jump height
        elevation_px = (baseline_hip_y - hip_y) * h
        if elevation_px > max_elevation_px:
            max_elevation_px = elevation_px
            display_jump_height = elevation_px * scale_factor

        # Landing detection
        if not landing_detected:
            if prev_ankle_y is not None and avg_ankle_y > prev_ankle_y - 3:
                landing_detected = True
                landing_frame = frame_count
        prev_ankle_y = avg_ankle_y

        # Wrist speed
        right_wrist = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        if right_wrist.visibility > 0.6:
            wrist_xy = np.array([right_wrist.x * w, right_wrist.y * h])
            WRIST_HISTORY.append(wrist_xy)

            if landing_detected and frame_count > landing_frame + 2 and len(WRIST_HISTORY) >= 2:
                speed = calculate_arm_speed(WRIST_HISTORY, scale_factor, fps)
                if speed > ARM_MOVEMENT_THRESHOLD:
                    record_arm_speed = True
                if record_arm_speed:
                    arm_speeds.append(speed)
                    display_arm_speed = max(arm_speeds)

        # Draw pose & trail
        frame = draw_pose(frame, landmarks)
        frame = draw_motion_trail(frame, list(WRIST_HISTORY))

    # Visual effects & info
    frame = apply_vignette(frame)
    frame = draw_header(frame)
    if display_jump_height > 1:
        draw_info_box(frame, "Peak Jump Height", display_jump_height, "cm", (30, 120), (0, 255, 255))
    if display_arm_speed > 0:
        draw_info_box(frame, "Peak Arm Speed", display_arm_speed * 3.6, "km/h", (30, 180), (0, 255, 0))
    frame = draw_border(frame)

    # --- Save processed frame ---
    out.write(frame)

    cv2.imshow("Bowler Analysis (Sports Broadcast)", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()  # release the video writer
cv2.destroyAllWindows()
