import tkinter as tk

class CalibrationWindow:
    def __init__(self, root, on_complete_callback):
        self.root = root
        self.on_complete = on_complete_callback
        
        self.top = tk.Toplevel(self.root)
        self.top.attributes("-fullscreen", True)
        self.top.attributes("-topmost", True)
        self.top.configure(bg='black')
        
        self.canvas = tk.Canvas(self.top, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        
        # 5 positions: Top-Left, Top-Right, Bottom-Left, Bottom-Right, Center
        margin = 100
        self.positions = [
            (margin, margin),
            (screen_w - margin, margin),
            (margin, screen_h - margin),
            (screen_w - margin, screen_h - margin),
            (screen_w // 2, screen_h // 2)
        ]
        
        self.current_idx = 0
        self.recorded_points = []
        
        self.dot = self.canvas.create_oval(0, 0, 0, 0, fill='red', outline='red')
        
        self.instruction_text = self.canvas.create_text(
            screen_w // 2, 50,
            text="Calibration: Stare at the RED DOT and BLINK.",
            fill="white", font=("Helvetica", 24, "bold")
        )
        
        self.is_active = True
        self.draw_dot()
        
    def draw_dot(self):
        if self.current_idx < len(self.positions):
            x, y = self.positions[self.current_idx]
            r = 30
            self.canvas.coords(self.dot, x-r, y-r, x+r, y+r)
            self.canvas.itemconfig(self.instruction_text, text=f"Calibration: Point {self.current_idx + 1} of 5. Stare & Blink.")
        else:
            self.is_active = False
            self.canvas.itemconfig(self.instruction_text, text="Calibration Complete! Loading UI...")
            self.canvas.delete(self.dot)
            self.top.after(1000, self.finish)
            
    def record_point(self, iris_x, iris_y):
        if self.is_active and self.current_idx < len(self.positions):
            self.recorded_points.append((iris_x, iris_y))
            self.current_idx += 1
            self.draw_dot()
            
    def finish(self):
        self.top.destroy()
        self.on_complete(self.recorded_points)
