import tkinter as tk
from tkinter import messagebox
import pyautogui
import cv2
import numpy as np
import threading
from PIL import ImageGrab

class ScreenRecorderApp: 
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Recorder") 
        self.root.geometry("400x200")
        self.recording = False
        self.filename = "output.mp4"

        # GUI elements
        self.label = tk.Label(root, text="Screen Recorder", font=("Arial", 20))
        self.label.pack(pady=10)

        self.start_button = tk.Button(root, text="Start Recording", width=20, command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Recording", width=20, state=tk.DISABLED, command=self.stop_recording)
        self.stop_button.pack(pady=10)

        # Status bar label at the bottom of the window
        self.status_label = tk.Label(root, text="Status: Not Recording", font=("Arial", 12), bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def update_status(self, message):
        """Helper method to update the status label."""
        self.status_label.config(text=f"Status: {message}")

    def start_recording(self):
        self.recording = True
        self.update_status("Recording in progress...")
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # Start the recording in a separate thread
        self.recording_thread = threading.Thread(target=self.record_screen)
        self.recording_thread.start()

    def stop_recording(self):
        self.recording = False
        self.update_status("Recording stopped. Saving file...")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        # Wait for the recording thread to finish
        self.recording_thread.join()

        messagebox.showinfo("Screen Recorder", f"Recording saved as {self.filename}")
        self.update_status("Not Recording")

    def record_screen(self):
        # Get screen resolution
        screen_size = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec for mp4 file
        out = cv2.VideoWriter(self.filename, fourcc, 20.0, screen_size)

        while self.recording:
            # Capture the screen
            img = ImageGrab.grab(bbox=(0, 0, screen_size[0], screen_size[1]))
            img_np = np.array(img)

            # Convert RGB to BGR (OpenCV uses BGR)
            frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
            out.write(frame)

        # Release the video writer
        out.release()

# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenRecorderApp(root)
    root.mainloop()
