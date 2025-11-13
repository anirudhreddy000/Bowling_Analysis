# 🏏 Bowling Analysis - Sports Motion Tracker

A **real-time sports motion analysis tool** to track bowling actions, measure jump height, and calculate arm speed using **MediaPipe** and **OpenCV**. This project visualizes player performance with **broadcast-style graphics**.

---

## 🚀 Features

* Detect and track **full-body pose** using MediaPipe.
* Calculate **peak jump height** during bowling.
* Calculate **peak arm speed** during ball release.
* Visual **motion trails** for bowling arm movement.
* **Broadcast-style overlays** and info panels.
* Apply visual effects like **vignette** for a polished display.
* **Modular structure** with reusable components.

---

## ⚙️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/anirudhreddy000/Bowling_Analysis.git](https://github.com/anirudhreddy000/Bowling_Analysis.git)
    cd Bowling_Analysis
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```
    * **Activate it (Linux / macOS):**
        ```bash
        source venv/bin/activate
        ```
    * **Activate it (Windows):**
        ```bash
        venv\Scripts\activate
        ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    Dependencies include: Python 3.8+, OpenCV (cv2), MediaPipe, NumPy

---

## ▶️ Usage

1.  **Run the main script:**
    ```bash
    python main.py
    ```
    Input video is loaded from the `videos/` folder.

2.  The program displays a window with live pose visualization, jump height, and arm speed.

3.  Press `q` to quit the video display.

4.  Output can optionally be saved to a video file (update `main.py` for `cv2.VideoWriter`).

---
## 📊 Output

* **Peak Jump Height:** measured in cm.
* **Peak Arm Speed:** measured in km/h.
* Motion trail showing arm movement.
* Broadcast-style info overlays.
