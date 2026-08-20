# Nayan AI 👁️🤖
> **A Zero-Cost, Multimodal Brain-Computer Interface (BCI) Alternative for Complete Hands-Free Operating System Control.**

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![TensorFlow Lite](https://img.shields.io/badge/MediaPipe-TFLite-orange.svg)
![Accessibility](https://img.shields.io/badge/Accessibility-100%25-brightgreen.svg)

Nayan AI is a revolutionary assistive technology designed for individuals suffering from severe neuromuscular diseases like **Amyotrophic Lateral Sclerosis (ALS), Quadriplegia**, and **Locked-in Syndrome**. 

It eliminates the need for expensive hardware (like $1,500+ infrared eye-trackers) by using state-of-the-art Deep Learning to track iris movements and facial micro-expressions directly from a standard 720p laptop webcam.

---

## ✨ Key Features
- **👀 Precision Eye-Tracking:** Maps iris movements to the OS cursor in real-time. Employs a mathematical `1-Euro Low-Pass Filter` to completely eliminate cursor jitter and lag.
- **😲 Facial Micro-expression Clicks:** Replace hardware mouse clicks with facial gestures. Opening your jaw triggers a left-click, and raising your eyebrows toggles the Virtual Keyboard.
- **⌨️ Predictive "Swype" AI Typing:** A custom-built, transparent virtual keyboard that predicts complete words as your eyes glide over the letters, saving significant physical effort.
- **🚨 Emergency SOS System:** Continuously monitors for micro-expressions of panic/pain (e.g., furrowed brows + squinting or mouth funneling). Triggers a high-frequency medical alert siren when the patient is in distress.
- **🎙️ Multimodal Voice Control:** A background daemon thread listens for phonetic wake-words to execute direct OS commands (e.g., *"Nayan, open WhatsApp"* or *"Nayan, turn on light"*).
- **🧠 Generative LLM Thought Expansion:** Type a single word like `"Water"`, click "SPEAK", and the AI automatically expands it into a full spoken sentence: *"I am feeling thirsty, please give me a glass of water."*

## 🛠️ Technology Stack
- **Core Logic & Concurrency:** Python 3 (Multi-threading)
- **Computer Vision:** Google MediaPipe (FaceLandmarker TFLite) & OpenCV
- **UI & OS Injection:** CustomTkinter (GPU-accelerated overlay) & PyAutoGUI
- **NLP & Audio:** SpeechRecognition, PyAudio, pyttsx3

---

## 🚀 How to Run Locally

### 1. Prerequisites
Ensure you have Python 3.10+ installed and a working webcam.

### 2. Installation
Clone the repository and install the dependencies:
```bash
git clone https://github.com/prasun91428/Nayan-AI.git
cd Nayan-AI
pip install -r requirements.txt
```

### 3. Execution
```bash
python main.py
```
*(Ensure you are in a well-lit environment for optimal iris tracking)*

---

## 💡 Future Scope (R&D)
- **Mobile Android App Integration:** Bringing this technology to smartphones via Android Accessibility Services.
- **IoT Smart Home:** Allowing paralyzed patients to telepathically control real-world appliances (Lights, Fans) via eye-dwell and voice commands.
- **Local LLaMa-3 Integration:** Generating complex conversational sentences completely offline.

---
*Developed as a sincere effort to bridge the digital accessibility gap and democratize technology for everyone.*
