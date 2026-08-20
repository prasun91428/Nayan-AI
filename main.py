# ==========================================
# Nayan AI - Telepathic Typing & Assistive OS
# Developed for: Final Year Project / Presentation
# Note: Ensure camera has good lighting before running!
# ==========================================

import tkinter as tk
import customtkinter as ctk
import threading
import cv2
from core.gaze_tracker import GazeTracker
from core.predictor import Predictor
from core.speaker import Speaker
from ui.keyboard import VirtualKeyboard
from ui.calibration import CalibrationWindow
import pyautogui
import time
import math
import webbrowser
import winsound
from ui.floating_menu import FloatingMenu

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class TelepathicTypingApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.withdraw() 
        
        self.current_word = ""
        self.swype_sequence = "" 
        self.full_sentence = ""
        
        print("Initializing NLP Engine...")
        self.predictor = Predictor()
        
        print("Initializing Text-To-Speech...")
        self.speaker = Speaker()
        
        from core.voice_assistant import VoiceAssistant
        print("Initializing Voice Assistant...")
        self.voice_assistant = VoiceAssistant(self.handle_voice_command)
        self.voice_assistant.start()
        
        print("Initializing Gaze Tracker (Camera)...")
        self.gaze_tracker = GazeTracker()
        
        self.running = True
        self.calibration_active = True
        
        # Global OS Control states
        self.keyboard_visible = True
        self.global_click_active = False
        self.last_gaze_pos = (0, 0)
        self.gaze_stable_start = time.time()
        self.global_dwell_time = 1.0 # 1 second global click
        
        # Gesture tracking to prevent spam
        self.last_jaw_open = False
        self.last_brow_raised = False
        self.last_mouth_funnel = False
        
        self.calibration_window = CalibrationWindow(self.root, self.on_calibration_complete)

    def on_calibration_complete(self, points):
        print("Calibration Data Captured!")
        if len(points) == 5:
            self.gaze_tracker.set_calibration_bounds(points)
        
        self.calibration_active = False
        
        self.keyboard = VirtualKeyboard(ctk.CTkToplevel(self.root), self.handle_keypress, self.handle_hover)
        self.keyboard.update_predictions(self.predictor.predict(""))
        
        self.floating_menu = FloatingMenu(self.root, self.toggle_keyboard, self.toggle_global_click)
        
        # Bind ESC key to exit the app globally from any UI window
        self.root.bind("<Escape>", self.exit_app)
        self.keyboard.root.bind("<Escape>", self.exit_app)
        
    def exit_app(self, event=None):
        print("Exiting application...")
        self.running = False
        if hasattr(self, 'voice_assistant'):
            self.voice_assistant.stop()
        self.root.quit()

    def toggle_keyboard(self):
        if self.keyboard_visible:
            self.keyboard.root.withdraw()
            self.keyboard_visible = False
        else:
            self.keyboard.root.deiconify()
            self.keyboard_visible = True
            
    def toggle_global_click(self):
        self.global_click_active = not self.global_click_active
        self.floating_menu.update_click_btn(self.global_click_active)
        
    def handle_global_dwell(self, screen_x, screen_y):
        if not self.global_click_active or self.keyboard_visible:
            return
            
        dist = math.hypot(screen_x - self.last_gaze_pos[0], screen_y - self.last_gaze_pos[1])
        if dist > 30: # Moved more than 30 pixels, reset timer
            self.last_gaze_pos = (screen_x, screen_y)
            self.gaze_stable_start = time.time()
        else:
            if time.time() - self.gaze_stable_start >= self.global_dwell_time:
                # Dwell time reached!
                print("Global Dwell Click triggered!")
                pyautogui.click()
                self.gaze_stable_start = time.time() + 1.0 # Pause for 1s after clicking
                self.speaker.speak("Click")

    def handle_hover(self, key):
        """Called whenever the eyes pass over a letter (Swyping)."""
        # Collapse consecutive duplicates (e.g. H H E E -> H E)
        if not self.swype_sequence or self.swype_sequence[-1] != key.lower():
            self.swype_sequence += key.lower()
            
        # Update predictions LIVE while swyping
        preds = self.predictor.decode_swype(self.swype_sequence)
        if hasattr(self, 'keyboard'):
            self.keyboard.update_predictions(preds)

    def handle_keypress(self, key):
        """Called when a user DWELLS on a key for 1 second."""
        if key == "SPEAK":
            # --- LLM THOUGHT EXPANSION DEMO ---
            # If the user types a single word, the AI expands it into a full sentence to save typing effort!
            text_to_speak = self.full_sentence.strip().lower()
            expansion_dict = {
                "water": "I am feeling thirsty. Could you please give me a glass of water?",
                "pain": "I am in pain. Please call the doctor immediately.",
                "bathroom": "I need to use the washroom.",
                "hungry": "I am feeling hungry. Can I get something to eat?",
                "tired": "I am feeling very tired, I would like to sleep now."
            }
            
            if text_to_speak in expansion_dict:
                text_to_speak = expansion_dict[text_to_speak]
                self.full_sentence = text_to_speak + " "
                self.keyboard.update_display(self.full_sentence)
            
            if text_to_speak:
                self.speaker.speak(text_to_speak)
            else:
                try:
                    text = self.root.clipboard_get()
                    self.speaker.speak(text)
                except:
                    pass
                
        elif key.startswith("PREDICTION:"):
            word = key.split(":")[1]
            pyautogui.write(word + " ")
            self.full_sentence += word + " "
            self.current_word = ""
            self.swype_sequence = ""
            
        elif key == "BACKSPACE":
            pyautogui.press('backspace')
            if self.current_word:
                self.current_word = self.current_word[:-1]
            elif self.full_sentence:
                self.full_sentence = self.full_sentence[:-1]
            self.swype_sequence = ""
            
        elif key == "SPACE":
            if self.swype_sequence:
                preds = self.predictor.decode_swype(self.swype_sequence)
                if preds:
                    pyautogui.write(preds[0] + " ")
                    self.full_sentence += preds[0] + " "
                else:
                    pyautogui.press('space')
                    self.full_sentence += " "
            else:
                pyautogui.press('space')
                self.full_sentence += " "
                
            self.current_word = ""
            self.swype_sequence = ""
            
        else:
            pyautogui.write(key.lower())
            self.current_word += key.lower()
            self.full_sentence += key.lower()
            self.swype_sequence = ""
            
        if hasattr(self, 'keyboard'):
            self.keyboard.update_display(self.full_sentence)
            if not self.swype_sequence:
                preds = self.predictor.predict(self.current_word)
                self.keyboard.update_predictions(preds)

    def handle_voice_command(self, cmd, arg):
        if cmd == "CLICK":
            self.root.after(0, pyautogui.click)
            self.root.after(0, self.speaker.speak, "Click")
        elif cmd == "HIDE_KBD":
            if self.keyboard_visible:
                self.root.after(0, self.toggle_keyboard)
        elif cmd == "SHOW_KBD":
            if not self.keyboard_visible:
                self.root.after(0, self.toggle_keyboard)
        elif cmd == "SCROLL_DOWN":
            self.root.after(0, pyautogui.scroll, -500)
            self.root.after(0, self.speaker.speak, "Scrolling down")
        elif cmd == "SCROLL_UP":
            self.root.after(0, pyautogui.scroll, 500)
            self.root.after(0, self.speaker.speak, "Scrolling up")
        elif cmd == "OPEN_WHATSAPP":
            self.root.after(0, webbrowser.open, 'https://web.whatsapp.com')
            self.root.after(0, self.speaker.speak, "Opening WhatsApp")
        elif cmd == "OPEN_GOOGLE":
            self.root.after(0, webbrowser.open, 'https://www.google.com')
            self.root.after(0, self.speaker.speak, "Opening Google")
        elif cmd == "LIGHT_ON":
            self.root.after(0, self.speaker.speak, "Turning on the room lights via IoT")
        elif cmd == "LIGHT_OFF":
            self.root.after(0, self.speaker.speak, "Turning off the room lights")
        elif cmd == "TYPE":
            self.root.after(0, pyautogui.write, arg + " ")
            self.root.after(0, self.speaker.speak, f"Typed {arg}")

    def gaze_loop(self):
        # State tracking to avoid spamming gestures
        self.gesture_cooldown = 0
        
        while self.running:
            ret = self.gaze_tracker.process_frame(calibrate_mode=self.calibration_active)
            if len(ret) == 4: # Fallback just in case
                image, clicked, valid, raw_iris = ret
                gestures = {'jaw_open': False, 'brow_raised': False}
            else:
                image, clicked, valid, raw_iris, gestures = ret
                
            if not valid:
                break
            
            # Emergency SOS Feature (Fear/Panic Expression)
            if gestures.get('mouth_funnel', False) and gestures.get('brow_raised', False):
                if not self.last_mouth_funnel:
                    print("🚨 SOS TRIGGERED! 🚨")
                    # Play a loud beep (Frequency 2000Hz, Duration 1000ms)
                    threading.Thread(target=winsound.Beep, args=(2000, 1000), daemon=True).start()
                    self.last_mouth_funnel = True
            else:
                self.last_mouth_funnel = False
                
            # Silent Pain Detection (Micro-expressions)
            if gestures.get('pain_face', False):
                if not getattr(self, 'last_pain_face', False):
                    print("⚠️ SILENT PAIN DETECTED! ⚠️")
                    self.root.after(0, self.speaker.speak, "Medical Alert: Patient discomfort detected.")
                    self.last_pain_face = True
            else:
                self.last_pain_face = False
                
            # Handle Face Gestures (Click and UI)
            if gestures['jaw_open']:
                if not self.last_jaw_open: # Only click once per jaw open
                    print("😲 JAW OPEN DETECTED: Face Click!")
                    self.root.after(0, pyautogui.click)
                    self.root.after(0, self.speaker.speak, "Face Click")
                    self.last_jaw_open = True
            else:
                self.last_jaw_open = False
                
            if gestures['brow_raised']:
                if not self.last_brow_raised and not gestures.get('mouth_funnel', False):
                    print("🤨 BROWS RAISED DETECTED: Toggling Keyboard!")
                    self.root.after(0, self.toggle_keyboard)
                    self.root.after(0, self.speaker.speak, "Toggled")
                    self.last_brow_raised = True
            else:
                self.last_brow_raised = False
            
            # Handle Global Dwell Click (If menu mode is on)
            if not self.calibration_active:
                screen_x, screen_y = pyautogui.position()
                self.handle_global_dwell(screen_x, screen_y)
                
                # Auto Eye-Scrolling
                screen_h = self.root.winfo_screenheight()
                if not hasattr(self, 'scroll_cooldown'):
                    self.scroll_cooldown = 0
                    
                if time.time() > self.scroll_cooldown:
                    if screen_y > screen_h * 0.9:
                        self.root.after(0, pyautogui.scroll, -200) # Scroll down
                        self.scroll_cooldown = time.time() + 0.1
                    elif screen_y < screen_h * 0.1:
                        self.root.after(0, pyautogui.scroll, 200) # Scroll up
                        self.scroll_cooldown = time.time() + 0.1
            
            cv2.imshow("Gaze Debug (Press ESC to close)", cv2.flip(image, 1))
            
            if self.calibration_active and clicked and raw_iris is not None:
                self.root.after(0, self.calibration_window.record_point, raw_iris[0], raw_iris[1])
                
            if cv2.waitKey(5) & 0xFF == 27: 
                self.running = False
                if hasattr(self, 'voice_assistant'):
                    self.voice_assistant.stop()
                self.root.quit()
                break
                
        self.gaze_tracker.cleanup()
        cv2.destroyAllWindows()

    def run(self):
        gaze_thread = threading.Thread(target=self.gaze_loop)
        gaze_thread.daemon = True
        gaze_thread.start()
        
        self.root.mainloop()
        self.running = False

if __name__ == "__main__":
    app = TelepathicTypingApp()
    app.run()
