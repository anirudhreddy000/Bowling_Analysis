import cv2

def load_video(path, width=1280, height=720):
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    return cap, fps, width, height

def resize_frame(frame, width, height):
    return cv2.resize(frame, (width, height))
