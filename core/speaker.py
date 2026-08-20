import pyttsx3
import threading

class Speaker:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150) # Slower, clearer speech
        except Exception as e:
            print(f"Error initializing TTS: {e}")
            self.engine = None
            
    def speak(self, text):
        if not self.engine or not text.strip():
            return
            
        def run_speech():
            try:
                # pyttsx3 runAndWait must be run carefully in threads. 
                # Re-initializing per thread sometimes works better on Windows,
                # but we'll try standard thread usage first.
                local_engine = pyttsx3.init()
                local_engine.setProperty('rate', 150)
                local_engine.say(text)
                local_engine.runAndWait()
            except Exception as e:
                print(f"Speech error: {e}")
                
        # Run speech in a separate thread so it doesn't freeze the camera/UI
        t = threading.Thread(target=run_speech)
        t.daemon = True
        t.start()
