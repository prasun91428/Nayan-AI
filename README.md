# Nayan AI - Hands-Free OS Control
Created by Prasun for Minor Project Evaluation.

This project is a software-based alternative to expensive hardware like Tobii Dynavox. It helps people with ALS or paralysis control their computers using just their eyes and facial expressions.

### What it does:
- **Eye Tracking:** Moves the mouse cursor using your iris. I used Mediapipe for this and added a 1-Euro filter so the cursor doesn't shake (took me forever to get the math right lol).
- **Face Clicks:** If you open your jaw, it clicks the mouse.
- **Virtual Keyboard:** You can type by just looking at letters.
- **SOS Alert:** If the patient is in pain or panic, it detects their facial expression and plays an alarm.
- **Voice Commands:** You can say "Open WhatsApp" or "Open Google" if you still have speech.

### Tech Stack used:
- Python 3.10
- OpenCV & Google MediaPipe (FaceLandmarker)
- CustomTkinter for the UI
- PyAutoGUI for mouse control

### How to run it:
1. Make sure your laptop camera is on and your face is well lit.
2. Install the requirements:
```
pip install -r requirements.txt
```
3. Run the main file:
```
python main.py
```

*Note: If the cursor feels laggy, try adjusting the beta value in gaze_tracker.py.*
