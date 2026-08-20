# Nayan AI 👁️🧠
**Advanced Eye-Tracking & Hands-Free OS Control**

---

## 🌍 ENGLISH DOCUMENTATION

### 1. The Vision: How it Helps People
Nayan AI is an assistive technology startup designed to give a voice and digital freedom to individuals suffering from severe physical disabilities.
It is primarily targeted toward:
- **ALS / Motor Neurone Disease (MND) Patients:** People (like the late Stephen Hawking) who are fully conscious but suffer from complete body paralysis. This software allows them to communicate using a Text-To-Speech engine.
- **Quadriplegics (Spinal Cord Injuries):** Individuals paralyzed from the neck down can use this software to regain independence. They can use WhatsApp, browse YouTube, or even work from home as coders using the Global OS Control features.
- **Locked-in Syndrome Patients:** It provides the only means of communication to the outside world by tracking the only muscles they can move: their eyes.
- **Hands-Free Professionals:** Useful for surgeons in sterile environments to scroll through medical records without touching a mouse.

### 2. Core Features ✨
- **Swype-for-Eyes:** Instead of manually typing letter by letter, users simply glance across letters (e.g., H -> E -> L -> O) and the AI Language Model predicts the correct word ("HELLO").
- **Dwell Clicking (No Blinking Required):** Prevents eye strain. Users just stare at a button or any part of the screen for 1 second, and the system automatically clicks it.
- **Text-To-Speech (TTS):** A "SPEAK" button reads the typed text out loud, acting as a vocal cord replacement for mute patients.
- **Floating Action Menu:** A transparent assistive menu that allows users to hide the keyboard and activate "Global Mouse Mode" to surf the internet.
- **1-Euro Smoothing Filter:** Butter-smooth mouse movement that filters out natural eye twitches and webcam jitter, preventing neck pain.

### 3. How to Use 📖
1. **Launch:** Run `Run_Telepathic_Typing_Pro.bat`.
2. **Calibration:** Look closely at the red dots that appear in the corners of your screen. Stare at them to calibrate the eye-tracker to your specific screen size.
3. **Keyboard Mode:** 
   - Look at a letter for 1 second to type it.
   - For Swyping, glance across multiple letters quickly, then stare at `SPACE`. The AI will decode your gaze trajectory.
   - Look at `SPEAK` to read your text out loud.
4. **OS Control Mode (Surfing the Web):**
   - Look at the `KBD` button on the right menu to hide the keyboard.
   - Look at the `CLICK OFF` button to turn it `CLICK ON`.
   - Now look anywhere on your screen (like a YouTube video) for 1 second, and a Left-Click will occur automatically!

### 4. Technologies Used & Why ⚙️
- **Python:** The core language, chosen for its vast AI and computer vision libraries.
- **Google MediaPipe (FaceLandmarker):** Used to extract 478 3D facial landmarks in real-time. It is incredibly fast and works on a standard CPU, negating the need for expensive hardware.
- **One Euro Filter:** A complex mathematical noise filter. Without it, the cursor would shake uncontrollably due to webcam noise. It makes the cursor move like honey.
- **NLTK & Regex (NLP):** Used to build the Swype Decoder. Regex parses the messy visual trajectory of the eyes to find the exact intended word from the NLTK English dictionary.
- **PyAutoGUI:** Allows Python to control the global Windows mouse and keyboard, letting the user break free from the app and control the whole OS.
- **Pyttsx3:** Offline Text-to-Speech engine. Selected because it works without an internet connection, ensuring privacy and reliability for patients.

---
<br><br>

## 🇮🇳 HINGLISH DOCUMENTATION

### 1. Vision: Yeh Logon Ki Madad Kaise Karega?
Nayan AI ek 'Assistive Technology' startup hai jiska main maqsad un logon ko aawaz aur azaadi dena hai jo physically disabled hain.
Yeh inke liye banaya gaya hai:
- **ALS / MND Patients:** Stephen Hawking jaise log jinka dimaag 100% zinda hota hai par body paralisys (lakwa) ka shikar hoti hai. Unke liye isme Text-to-Speech (Aawaz) feature hai.
- **Quadriplegics (Gardan se neeche Paralysis):** Jinke dono haath aur pair kaam nahi karte. Is software se woh WhatsApp chala sakte hain, YouTube dekh sakte hain, ya Work from home coding jobs kar sakte hain.
- **Locked-in Syndrome:** Aise log jo sirf apni aankhein hila sakte hain, unke liye duniya se baat karne ka yeh iklauta rasta hai.
- **Surgeons:** Operation theatre mein doctor bina mouse ko haath lagaye (sterile hands) sirf aankhon se X-rays zoom kar sakte hain.

### 2. Main Features ✨
- **Swype-for-Eyes AI:** Ek-ek letter type karne ki zaroorat nahi. Bas letters par nazar ghumaiye (jaise H -> E -> L -> O) aur AI khud word samajh jayega.
- **Dwell Clicking (No Blinking):** Aankhein thakne se bachane ke liye, ab blink ki zaroorat nahi. Aap sirf 1 second ke liye kahin ghooriye, aur automatic click ho jayega.
- **Text-To-Speech (TTS):** Keyboard par ek 'SPEAK' button hai jo aapke likhe hue text ko zor se bol kar sunata hai.
- **Floating Action Menu:** Ek chota menu jisse aap keyboard hide kar sakte hain aur Global Mouse Mode on karke poora laptop chala sakte hain.
- **1-Euro Filter:** Yeh maths ka ek complex filter hai jo webcam ke jhatkon ko rokta hai aur mouse ko bilkul smooth chalata hai taaki gardan mein dard na ho.

### 3. Ise Use Kaise Karein? 📖
1. **Start:** `Run_Telepathic_Typing_Pro.bat` par double click karein.
2. **Calibration:** Screen ke corners mein aane wale red dots ko ghooriye. Yeh software ko aapki aankhon aur screen size ke hisaab se set karta hai.
3. **Keyboard Mode:** 
   - Kisi letter par 1 second ghooriye, woh type ho jayega.
   - Swype karne ke liye jaldi-jaldi letters par dekhiye aur fir `SPACE` par ghooriye. AI khud word bana dega.
   - Apni baat bolne ke liye `SPEAK` par ghooriye.
4. **OS Control Mode (YouTube/WhatsApp Chalana):**
   - Right side menu par `KBD` icon ko ghoor kar keyboard chupaiye.
   - `CLICK` button ko ghoor kar `CLICK ON` kijiye.
   - Ab screen par kahin bhi (jaise Google Chrome) 1 second dekhiye, automatically Left-Click ho jayega!

### 4. Technologies Used & Why (Kaunsi Tech Aur Kyu?) ⚙️
- **Python:** Kyunki isme AI aur Computer Vision ka sabse best support hai.
- **Google MediaPipe:** Yeh real-time mein chehre ke 478 points padh leta hai. Ise isliye chuna gaya kyunki yeh bina GPU aur mehenge hardware ke normal laptop CPU par bhi fast chalta hai.
- **One Euro Filter:** Agar yeh nahi hota toh mouse screen par kaanpta (shake karta). Yeh filter noise hatata hai.
- **NLTK & Regex (AI NLP):** Swype feature ke liye use hua hai. Jab aankhein aade-tedhe raste se guzarti hain, toh Regex maths us raste ko NLTK dictionary se match karke sahi word nikalta hai.
- **PyAutoGUI:** Ise isliye use kiya gaya taaki aapka software sirf ek app tak seemit na rahe, balki poore Windows (jaise mouse aur real keyboard) ko control kar sake.
- **Pyttsx3 (Text to Speech):** Yeh aawaz nikalne wali library hai. Ise isliye chuna kyunki yeh offline chalti hai, toh patient ko internet ki zaroorat nahi padti aur speed fast rehti hai.

---
**Crafted for Accessibility. Powered by AI.**
