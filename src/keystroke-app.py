import tkinter as tk
from tkinter import ttk, messagebox
import keyboard
import time
import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Constants
BG_COLOR = "#f0f0f0"
BUTTON_COLOR = "#4a7a8c"
TEXT_COLOR = "#333333"
FONT = ("Segoe UI", 10)

reference_vectors = []
average_reference = None
password = "frappe123"
threshold = 1.5

class KeystrokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Keystroke Biometrics with DTW")
        self.root.geometry("500x400")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)
       
        self.setup_ui()
       
    def setup_ui(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg=BG_COLOR)
        header_frame.pack(pady=20)
       
        self.title_label = tk.Label(
            header_frame,
            text="Keystroke Biometrics Authentication",
            font=("Segoe UI", 14, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
        self.title_label.pack()
       
        self.subtitle_label = tk.Label(
            header_frame,
            text="Dynamic Time Warping for Keystroke Analysis",
            font=FONT,
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
        self.subtitle_label.pack(pady=5)
       
        # Button Frame
        button_frame = tk.Frame(self.root, bg=BG_COLOR)
        button_frame.pack(pady=20)
       
        style = ttk.Style()
        style.configure('TButton',
                       font=FONT,
                       padding=10,
                       background=BUTTON_COLOR,
                       foreground='white')
       
        self.enroll_btn = ttk.Button(
            button_frame,
            text="Enroll Typing Profile",
            command=self.enroll,
            style='TButton'
        )
        self.enroll_btn.pack(pady=10, fill=tk.X)
       
        self.verify_btn = ttk.Button(
            button_frame,
            text="Verify Identity",
            command=self.verify,
            style='TButton'
        )
        self.verify_btn.pack(pady=10, fill=tk.X)
       
        self.plot_btn = ttk.Button(
            button_frame,
            text="Show DTW Analysis",
            command=self.show_plot,
            style='TButton'
        )
        self.plot_btn.pack(pady=10, fill=tk.X)
       
        # Status Bar
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=FONT,
            bg='white',
            fg=TEXT_COLOR
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
   
    def update_status(self, message):
        self.status_bar.config(text=message)
        self.root.update_idletasks()
   
    def record_keystrokes(self, prompt="Type the password: "):
        events = []
        start = time.time()
        typed = ""

        messagebox.showinfo("Typing Prompt", prompt)
        self.update_status("Recording keystrokes...")

        while True:
            event = keyboard.read_event()
            if event.event_type in ("down", "up"):
                timestamp = time.time() - start
                events.append((event.name, event.event_type, timestamp))
           
            if event.event_type == "down":
                typed += event.name
                if typed.replace("space", " ") == password:
                    break

        return events
   
    def extract_features(self, events):
        hold_times = {}
        flight_times = []

        key_down_times = {}
        prev_down_time = None

        for key, event_type, timestamp in events:
            if event_type == "down":
                key_down_times[key] = timestamp
                if prev_down_time is not None:
                    flight_times.append(timestamp - prev_down_time)
                prev_down_time = timestamp
            elif event_type == "up" and key in key_down_times:
                hold_times[key] = timestamp - key_down_times[key]

        sorted_keys = sorted(hold_times.keys())
        hold_seq = [hold_times[k] for k in sorted_keys]
        features = hold_seq + flight_times
        return np.array(features).reshape(-1)
   
    def compare_features(self, ref, test):
        ref = ref.reshape(-1)
        test = test.reshape(-1)
        distance, _ = fastdtw(ref.reshape(-1, 1), test.reshape(-1, 1), dist=euclidean)
        return distance
   
    def enroll(self):
        global average_reference
        reference_vectors.clear()
        self.update_status("Enrolling new typing profile...")

        for i in range(3):
            events = self.record_keystrokes(f"Type sample {i+1}: {password}")
            features = self.extract_features(events)
            reference_vectors.append(features)

        average_reference = np.mean(reference_vectors, axis=0)
        messagebox.showinfo("Enrollment Complete", "✅ Typing profile successfully enrolled.")
        self.update_status("Ready - Profile enrolled")
   
    def verify(self):
        if average_reference is None:
            messagebox.showwarning("Error", "You must enroll first!")
            return

        events = self.record_keystrokes(f"Type to verify: {password}")
        test_features = self.extract_features(events)
        distance = self.compare_features(average_reference, test_features)

        if distance < threshold:
            result = f"✅ Authentication Successful!\nDTW distance: {distance:.3f}"
        else:
            result = f"❌ Authentication Failed!\nDTW distance: {distance:.3f}"
       
        messagebox.showinfo("Result", result)
        self.update_status("Ready - Verification complete")
   
    def show_plot(self):
        if not reference_vectors:
            messagebox.showinfo("No Data", "Please enroll first.")
            return

        distances = []
        for vec in reference_vectors:
            d = self.compare_features(average_reference, vec)
            distances.append(d)

        # Create plot window
        plot_window = tk.Toplevel(self.root)
        plot_window.title("DTW Distance Analysis")
        plot_window.geometry("600x500")
       
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(distances, marker='o', color=BUTTON_COLOR, linewidth=2)
        ax.axhline(y=threshold, color='r', linestyle='--', label='Threshold')
        ax.set_title("DTW Distance per Enrollment Sample", pad=20)
        ax.set_xlabel("Sample #")
        ax.set_ylabel("DTW Distance")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)
        fig.tight_layout()
       
        # Embed plot in Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
       
        # Add close button
        close_btn = ttk.Button(
            plot_window,
            text="Close",
            command=plot_window.destroy
        )
        close_btn.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = KeystrokeApp(root)
    root.mainloop()