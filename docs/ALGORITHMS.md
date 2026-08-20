# Nayan AI 2.0 - Technical Architecture & Algorithms

This document details the programming languages, libraries, and core algorithms used to build the Nayan AI Telepathic Typing platform.

## 1. Programming Language
- **Python (3.x):** The entire system is written in Python. Python was chosen for its unparalleled ecosystem in Artificial Intelligence, Machine Learning, Computer Vision, and rapid prototyping capabilities.

## 2. Core Libraries & Frameworks
- **MediaPipe (by Google):** The backbone for real-time Computer Vision. We use the `FaceLandmarker` task to extract 478 3D facial landmarks, iris positions, and facial expressions (blendshapes).
- **OpenCV (`cv2`):** Used for capturing the webcam video feed, flipping images (for a mirror effect), and drawing debug visualizations.
- **PyAutoGUI:** Acts as the bridge between the AI and the Operating System. It programmatically controls the mouse cursor (move, click) and scrolling based on AI outputs.
- **CustomTkinter (`customtkinter`):** Used to build the modern, dark-mode, "glassmorphism" User Interface (Virtual Keyboard and Floating Menu).
- **SpeechRecognition & PyAudio:** Used for capturing raw microphone audio and converting it into text using Google's speech recognition engine.
- **pyttsx3:** An offline Text-to-Speech (TTS) engine that allows the AI to speak back to the user without needing an internet connection.

---

## 3. Core Algorithms

### A. Deep Neural Networks for Landmark Detection
We utilize a pre-trained **TensorFlow Lite (TFLite)** model via MediaPipe. This neural network processes each video frame and outputs:
1. **3D Coordinates:** (x, y, z) for 478 points on the face.
2. **Iris Tracking:** Pinpoints the exact center of the left and right irises.
3. **Blendshapes:** A regression output scoring 52 different facial muscle movements from 0.0 to 1.0 (e.g., `jawOpen` = 0.85).

### B. The 1-Euro Filter (Jitter Removal)
Human eyes naturally twitch (microsaccades) even when staring at a fixed point. If we mapped raw eye coordinates directly to the mouse, the cursor would vibrate violently.
- **The Algorithm:** We implemented the **1-Euro Filter**, an HCI (Human-Computer Interaction) algorithm. 
- **How it works:** It acts as a dynamic low-pass filter. When the eye moves slowly (trying to focus), it applies heavy smoothing to kill jitter. When the eye moves fast (looking across the screen), it reduces smoothing to eliminate lag.

### C. Linear Interpolation & Boundary Padding
To translate the iris position to the computer monitor:
- We extract the normalized coordinates `(x, y)` of the iris where `0.0` is the top-left of the camera and `1.0` is the bottom-right.
- We map this to the screen resolution (e.g., 1920x1080) using **Linear Interpolation**.
- **Padding Algorithm:** We apply a mathematical padding (e.g., 50%) to the camera frame. This means the user only needs to move their eyes slightly off-center to reach the absolute edge of their computer screen, preventing neck strain.

### D. EAR (Eye Aspect Ratio) for Blink Detection
Before Face Gestures, blinks were used for clicks.
- **Algorithm:** $EAR = \frac{||P_2 - P_6|| + ||P_3 - P_5||}{2 \times ||P_1 - P_4||}$
- It calculates the distance between the vertical landmarks of the eye and divides it by the horizontal distance. If this ratio drops below a threshold (e.g., 0.2) rapidly, a blink is registered.

### E. Dwell Time Algorithm
Used for selecting keys on the Virtual Keyboard.
- **Logic:** The UI tracks when the cursor enters a button's bounding box and starts a timer. If the cursor stays within the box for a continuous `Dwell Time` (e.g., 1.0 seconds) without leaving, a `click` event is fired.

### F. Phonetic Matching (Wake-Word Fallback)
Voice recognition can struggle with Indian accents or background noise.
- **Logic:** Instead of strictly looking for the string `"nayan"`, the system looks for an array of phonetic equivalents and common misinterpretations (e.g., `"nine"`, `"lion"`, `"ryan"`, `"maya"`). If the recognized text contains any of these, the Assistant activates.

### G. Concurrency (Multi-Threading)
The system runs multiple asynchronous loops simultaneously:
1. **Main Thread (Tkinter):** Handles the UI and rendering.
2. **Vision Thread:** Captures video and runs the heavy ML model.
3. **Audio Thread (Daemon):** Constantly listens to the microphone in the background without freezing the video feed. Safe communication back to the UI is handled using Tkinter's thread-safe `.after()` queue.
