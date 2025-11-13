import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def draw_pose(frame, landmarks):
    if landmarks:
        mp_drawing.draw_landmarks(
            frame, landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=3),
            mp_drawing.DrawingSpec(color=(0, 180, 255), thickness=2))
    return frame

def draw_motion_trail(frame, wrist_history, color=(0,255,0)):
    for i in range(1, len(wrist_history)):
        cv2.line(frame, tuple(wrist_history[i-1].astype(int)),
                 tuple(wrist_history[i].astype(int)),
                 color, 2)
    return frame

def draw_info_box(frame, label, value, unit, pos, color):
    x, y = pos
    overlay = frame.copy()
    cv2.rectangle(overlay, (x - 10, y - 35), (x + 380, y + 10), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
    text = f"{label}: {value:.1f} {unit}"
    cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 3, cv2.LINE_AA)

def draw_header(frame, text="Bowler Motion Tracker"):
    h, w, _ = frame.shape
    cv2.rectangle(frame, (0, 0), (w, 60), (0, 0, 0), -1)
    cv2.putText(frame, text, (30, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 255), 3, cv2.LINE_AA)
    return frame

def draw_border(frame):
    h, w, _ = frame.shape
    cv2.rectangle(frame, (5, 5), (w - 5, h - 5), (255, 255, 255), 2)
    return frame
