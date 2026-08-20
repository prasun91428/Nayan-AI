import speech_recognition as sr
import threading

class VoiceAssistant:
    def __init__(self, command_callback):
        self.callback = command_callback
        self.recognizer = sr.Recognizer()
        self.running = False
        
    def start(self):
        self.running = True
        t = threading.Thread(target=self.listen_loop)
        t.daemon = True
        t.start()
        
    def stop(self):
        self.running = False
        
    def listen_loop(self):
        try:
            with sr.Microphone() as source:
                print("Calibrating Voice Assistant (Mic)...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Voice Assistant is LIVE! Say 'Click', 'Scroll Down', 'Type [message]'")
                
                while self.running:
                    try:
                        # Listen with longer timeouts so it doesn't cut off the user
                        audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=5)
                        text = self.recognizer.recognize_google(audio).lower()
                        print(f"🎤 Heard: '{text}'")
                        self.process_command(text)
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        pass
                    except sr.RequestError as e:
                        print(f"🎤 Network Error: {e}")
                    except Exception as e:
                        pass
        except Exception as e:
            print(f"🎤 Microphone initialization failed: {e}. Voice commands disabled.")

    def process_command(self, text):
        """Maps spoken English to OS Commands"""
        
        # Wake word check (Allows phonetic misinterpretations by English API)
        wake_words = ["nayan", "nayon", "nion", "ryan", "lion", "nine", "naman", "narayan", "mine", "line"]
        if not any(w in text for w in wake_words):
            return # Ignore if Wake Word is not said!
            
        print("🟢 Wake word detected! Processing command...")
            
        if "click" in text:
            self.callback("CLICK", None)
            
        elif "hide" in text or "close" in text:
            self.callback("HIDE_KBD", None)
            
        elif "light" in text:
            if "on" in text:
                self.callback("LIGHT_ON", None)
            elif "off" in text:
                self.callback("LIGHT_OFF", None)
                
        elif "open" in text or "show" in text:
            if "whatsapp" in text:
                self.callback("OPEN_WHATSAPP", None)
            elif "google" in text or "chrome" in text or "youtube" in text:
                self.callback("OPEN_GOOGLE", None)
            else:
                self.callback("SHOW_KBD", None)
            
        elif "scroll down" in text:
            self.callback("SCROLL_DOWN", None)
            
        elif "scroll up" in text:
            self.callback("SCROLL_UP", None)
            
        elif "type" in text:
            parts = text.split("type", 1)
            if len(parts) > 1 and parts[1].strip():
                self.callback("TYPE", parts[1].strip())
