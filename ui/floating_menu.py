import tkinter as tk
import customtkinter as ctk

class FloatingMenu:
    def __init__(self, root, on_toggle_keyboard, on_toggle_click):
        self.root = root
        self.menu_win = ctk.CTkToplevel(self.root)
        self.menu_win.title("Nayan AI")
        self.menu_win.attributes("-topmost", True)
        self.menu_win.attributes("-alpha", 0.95)
        self.menu_win.overrideredirect(True) # No title bar
        
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        
        # Position on the right middle edge of the screen
        self.menu_win.geometry(f"120x250+{screen_w - 120}+{int(screen_h/3)}")
        self.menu_win.configure(fg_color='#111111')
        
        self.btn_kb = ctk.CTkButton(self.menu_win, text="⌨️\nKBD", font=("Helvetica", 18, "bold"), 
                                    fg_color='#333333', text_color='white', corner_radius=15,
                                    command=on_toggle_keyboard)
        self.btn_kb.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        self.btn_clk = ctk.CTkButton(self.menu_win, text="🖱️\nCLICK\nOFF", font=("Helvetica", 18, "bold"), 
                                     fg_color='#550000', text_color='white', corner_radius=15,
                                     command=on_toggle_click)
        self.btn_clk.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        self.dwell_job = None
        self.dwell_time_ms = 1000
        
        self.bind_dwell(self.btn_kb, on_toggle_keyboard)
        self.bind_dwell(self.btn_clk, on_toggle_click)
        
    def bind_dwell(self, button, callback):
        def on_enter(e):
            button.configure(fg_color='#777777')
            self.dwell_job = self.menu_win.after(self.dwell_time_ms, lambda: self.execute(button, callback))
            
        def on_leave(e):
            if button == self.btn_clk and "ON" in self.btn_clk.cget("text"):
                button.configure(fg_color='#005500')
            elif button == self.btn_clk:
                button.configure(fg_color='#550000')
            else:
                button.configure(fg_color='#333333')
            
            if self.dwell_job:
                self.menu_win.after_cancel(self.dwell_job)
                self.dwell_job = None
                
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
        
    def execute(self, button, callback):
        button.configure(fg_color='#00ffcc')
        callback()
        self.dwell_job = None
        
    def update_click_btn(self, is_on):
        if is_on:
            self.btn_clk.configure(text="🖱️\nCLICK\nON", fg_color='#005500')
        else:
            self.btn_clk.configure(text="🖱️\nCLICK\nOFF", fg_color='#550000')
