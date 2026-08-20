# Project Synopsis: Nayan AI (Telepathic Typing & Assistive OS)

## 1. Project Title
**Nayan AI**: A Multimodal Brain-Computer Interface (BCI) Alternative for Complete Hands-Free Operating System Control.

## 2. Problem Statement
Individuals suffering from severe motor neuron diseases like ALS (Amyotrophic Lateral Sclerosis) or Quadriplegia often experience "Locked-in Syndrome". They lose the ability to move their limbs and voice, making it impossible to use a standard computer or smartphone. Existing solutions like *Tobii Dynavox* are highly expensive (over $1,500) and require specialized infrared hardware, making them inaccessible to the masses in developing nations.

## 3. Proposed Solution
Nayan AI is a zero-cost, software-only assistive technology that runs on any standard 720p laptop webcam. It combines state-of-the-art Computer Vision (MediaPipe) and Natural Language Processing (SpeechRecognition) to allow users to completely operate a computer using only their eyes, facial expressions, and voice.

## 4. Key Features
1. **Eye-Tracking Cursor:** Maps the user's iris movements to the OS mouse cursor using dynamic padding to prevent neck strain.
2. **Face Gesture Clicks:** Uses 3D facial blendshapes. Opening the jaw slightly triggers a global mouse click. Raising eyebrows toggles the Virtual Keyboard.
3. **Swype-Style AI Typing:** Users can dwell on letters to type, or visually "Swype" across letters, and the AI will predict the intended word.
4. **Emergency SOS System:** Detects panic/fear expressions (Open mouth + Raised eyebrows) and triggers a high-frequency siren to alert caretakers.
5. **Direct Voice OS Control:** Background voice assistant that listens for the wake word ("Nayan"). Users can say *"Nayan, open WhatsApp"* or *"Nayan, type Hello"*.

## 5. Technology Stack
- **Programming Language:** Python 3.x
- **Computer Vision:** Google MediaPipe (FaceLandmarker), OpenCV (`cv2`)
- **UI Framework:** CustomTkinter (Glassmorphism & Dark Mode UI)
- **OS Automation:** PyAutoGUI, `webbrowser`, `winsound`
- **Audio Processing:** `SpeechRecognition`, PyAudio, `pyttsx3` (Offline Text-to-Speech)

## 6. Core Algorithms
- **Deep Neural Networks (TFLite):** Used by MediaPipe for real-time 478-point 3D face tracking and blendshape regression.
- **1-Euro Filter:** A real-time low-pass filter specifically designed for Human-Computer Interaction (HCI). It heavily smooths the cursor when the eyes are resting (removing jitter/noise) and reduces smoothing when eyes dart across the screen (eliminating lag).
- **Linear Interpolation:** Maps normalized camera coordinates [0, 1] to monitor resolution coordinates (e.g., 1920x1080).
- **Phonetic Matching:** The Voice Assistant uses phonetic string arrays to handle misrecognitions of the wake word (e.g., catching "nine" or "lion" when the user says "nayan").
