import mediapipe as mp
import cv2

mp_pose = mp.solutions.pose

def init_pose(min_detection_confidence=0.5, min_tracking_confidence=0.5):
    return mp_pose.Pose(min_detection_confidence=min_detection_confidence,
                        min_tracking_confidence=min_tracking_confidence)

def get_pose_landmarks(frame, pose_model):
    results = pose_model.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    return results.pose_landmarks if results.pose_landmarks else None
