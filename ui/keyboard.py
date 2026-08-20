import tkinter as tk
import customtkinter as ctk

class VirtualKeyboard:
    def __init__(self, root, on_keypress_callback, on_hover_callback):
        self.root = root
        self.root.title("Nayan AI - Smart Keyboard")
        
        self.root.attributes("-alpha", 0.95)
        self.root.attributes("-topmost", True)
        
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        
        self.root.geometry(f"{screen_w}x{int(screen_h/2)}+0+{int(screen_h/2)}")
        
        self.on_keypress = on_keypress_callback
        self.on_swype_hover = on_hover_callback
        
        self.buttons = {}
        self.prediction_buttons = []
        
        self.dwell_job = None
        self.dwell_time_ms = 1000 # 1 second dwell
        
        self.create_layout()

    def create_layout(self):
        self.display_frame = ctk.CTkFrame(self.root, fg_color="#111111", corner_radius=10)
        self.display_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        self.display_label = ctk.CTkLabel(self.display_frame, text="...", font=("Helvetica", 32, "bold"), text_color="white")
        self.display_label.pack(pady=10)

        self.pred_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.pred_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        
        for i in range(3):
            btn = ctk.CTkButton(self.pred_frame, text="", font=("Helvetica", 28, "bold"),
                                fg_color="#1a1a1a", text_color="#00ffcc", hover_color="#333333",
                                corner_radius=15, command=lambda idx=i: self.select_prediction(idx))
            btn.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)
            self.bind_dwell_events(btn, f"PREDICTION:{i}", lambda idx=i: self.select_prediction(idx))
            self.prediction_buttons.append(btn)

        self.kb_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.kb_frame.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        keys = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', 'BACKSPACE'],
            ['SPACE', 'SPEAK']
        ]

        for r, row in enumerate(keys):
            row_frame = ctk.CTkFrame(self.kb_frame, fg_color="transparent")
            row_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
            for key in row:
                btn = ctk.CTkButton(row_frame, text=key, font=("Helvetica", 24, "bold"),
                                    fg_color="#222222", text_color="white", hover_color="#444444",
                                    corner_radius=10, command=lambda k=key: self.on_keypress(k))
                btn.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=3, pady=3)
                self.bind_dwell_events(btn, key, lambda k=key: self.on_keypress(k))
                self.buttons[key] = btn

    def bind_dwell_events(self, button, key, action_callback):
        # CTkButton uses bindings on its internal canvas, but <Enter> and <Leave> work on the widget itself.
        def on_enter(e):
            button.configure(fg_color='#555555')
            # Swype: Record key hover
            if key not in ["SPACE", "BACKSPACE", "SPEAK"] and not key.startswith("PREDICTION:"):
                self.on_swype_hover(key)
                
            self.dwell_job = self.root.after(self.dwell_time_ms, lambda: self.execute_dwell(button, action_callback))
            
        def on_leave(e):
            button.configure(fg_color='#222222')
            if self.dwell_job:
                self.root.after_cancel(self.dwell_job)
                self.dwell_job = None
                
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)

    def execute_dwell(self, button, action_callback):
        button.configure(fg_color='#00ffcc', text_color='black') 
        action_callback()
        self.root.after(200, lambda: button.configure(fg_color='#555555', text_color='white'))
        self.dwell_job = None

    def update_predictions(self, predictions):
        for i in range(3):
            if i < len(predictions):
                self.prediction_buttons[i].configure(text=predictions[i])
            else:
                self.prediction_buttons[i].configure(text="")
                
    def update_display(self, text):
        if not text:
            self.display_label.configure(text="...")
        else:
            self.display_label.configure(text=text)

    def select_prediction(self, idx):
        word = self.prediction_buttons[idx].cget("text")
        if word:
            self.on_keypress("PREDICTION:" + word)
