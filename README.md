# Eye Tracker

A real-time eye tracking application that monitors focus and attention using computer vision and facial landmark detection.

## Features

- **Real-time Eye Tracking** - Uses MediaPipe Face Mesh to detect and track eye movements
- **Blink Detection** - Monitors blink frequency to detect eye closure
- **Head Pose Estimation** - Tracks head orientation (yaw and pitch)
- **Focus Monitoring** - Detects when the user is distracted (looking away, head turned, or eyes closed)
- **Calibration System** - Maps gaze position to screen coordinates for improved accuracy
- **Mouse Control** - Optionally control the mouse cursor with eye movements
- **Distraction Alerts** - Visual and audio alerts when user becomes distracted

## Requirements

```
opencv-python>=4.8.0
mediapipe>=0.10.0
numpy>=1.24.0
pyautogui>=0.9.54
customtkinter>=5.2.0
Pillow>=10.0.0
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the main eye tracking application:

```bash
python main.py
```

### Controls

- **ESC** - Exit the application
- **C** - Recalibrate the screen mapping
- **L** - Toggle landmark visibility

### Calibration

For best accuracy, calibrate the system by following the on-screen prompts. This maps your eye position to screen coordinates.

## Project Structure

- `main.py` - Main application entry point
- `eye_tracker.py` - Core eye tracking and gaze detection
- `blink_detector.py` - Blink detection logic
- `head_pose.py` - Head pose estimation
- `calibration.py` - Screen calibration system
- `mouse_controller.py` - Mouse control functionality
- `gui_app.py` - GUI interface (optional)
- `face_landmarker.task` - MediaPipe model file

## License

MIT