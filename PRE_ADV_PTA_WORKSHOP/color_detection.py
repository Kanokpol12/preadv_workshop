import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class ColorDetectionApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        # OpenCV video capture
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Cannot open camera")
            exit()
            
        # Default HSV range values
        self.lower_h = tk.IntVar(value=0)
        self.lower_s = tk.IntVar(value=50)
        self.lower_v = tk.IntVar(value=50)
        self.upper_h = tk.IntVar(value=10)
        self.upper_s = tk.IntVar(value=255)
        self.upper_v = tk.IntVar(value=255)
        
        # Create GUI components
        self.create_widgets()
        
        # Initialize display
        self.delay = 15
        self.update()
        
        self.window.mainloop()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Video frame
        self.video_frame = ttk.Frame(main_frame, borderwidth=2, relief="sunken")
        self.video_frame.grid(row=0, column=0, padx=5, pady=5)
        
        self.canvas = tk.Canvas(self.video_frame, width=640, height=480)
        self.canvas.pack()
        
        # Controls frame
        controls_frame = ttk.LabelFrame(main_frame, text="Color Detection Controls", padding="10")
        controls_frame.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.N, tk.S))
        
        # Lower HSV controls
        ttk.Label(controls_frame, text="Lower HSV Bounds").grid(row=0, column=0, columnspan=2, pady=5)
        
        ttk.Label(controls_frame, text="H:").grid(row=1, column=0, sticky=tk.E)
        lower_h_scale = ttk.Scale(controls_frame, from_=0, to=179, variable=self.lower_h, orient=tk.HORIZONTAL, length=200)
        lower_h_scale.grid(row=1, column=1, padx=5, pady=2)
        ttk.Label(controls_frame, textvariable=self.lower_h).grid(row=1, column=2, padx=5)
        
        ttk.Label(controls_frame, text="S:").grid(row=2, column=0, sticky=tk.E)
        lower_s_scale = ttk.Scale(controls_frame, from_=0, to=255, variable=self.lower_s, orient=tk.HORIZONTAL, length=200)
        lower_s_scale.grid(row=2, column=1, padx=5, pady=2)
        ttk.Label(controls_frame, textvariable=self.lower_s).grid(row=2, column=2, padx=5)
        
        ttk.Label(controls_frame, text="V:").grid(row=3, column=0, sticky=tk.E)
        lower_v_scale = ttk.Scale(controls_frame, from_=0, to=255, variable=self.lower_v, orient=tk.HORIZONTAL, length=200)
        lower_v_scale.grid(row=3, column=1, padx=5, pady=2)
        ttk.Label(controls_frame, textvariable=self.lower_v).grid(row=3, column=2, padx=5)
        
        # Upper HSV controls
        ttk.Label(controls_frame, text="Upper HSV Bounds").grid(row=4, column=0, columnspan=2, pady=5)
        
        ttk.Label(controls_frame, text="H:").grid(row=5, column=0, sticky=tk.E)
        upper_h_scale = ttk.Scale(controls_frame, from_=0, to=179, variable=self.upper_h, orient=tk.HORIZONTAL, length=200)
        upper_h_scale.grid(row=5, column=1, padx=5, pady=2)
        ttk.Label(controls_frame, textvariable=self.upper_h).grid(row=5, column=2, padx=5)
        
        ttk.Label(controls_frame, text="S:").grid(row=6, column=0, sticky=tk.E)
        upper_s_scale = ttk.Scale(controls_frame, from_=0, to=255, variable=self.upper_s, orient=tk.HORIZONTAL, length=200)
        upper_s_scale.grid(row=6, column=1, padx=5, pady=2)
        ttk.Label(controls_frame, textvariable=self.upper_s).grid(row=6, column=2, padx=5)
        
        ttk.Label(controls_frame, text="V:").grid(row=7, column=0, sticky=tk.E)
        upper_v_scale = ttk.Scale(controls_frame, from_=0, to=255, variable=self.upper_v, orient=tk.HORIZONTAL, length=200)
        upper_v_scale.grid(row=7, column=1, padx=5, pady=2)
        ttk.Label(controls_frame, textvariable=self.upper_v).grid(row=7, column=2, padx=5)
        
        # Preset buttons
        presets_frame = ttk.LabelFrame(controls_frame, text="Color Presets", padding="10")
        presets_frame.grid(row=8, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        ttk.Button(presets_frame, text="Red", command=lambda: self.set_preset("red")).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(presets_frame, text="Green", command=lambda: self.set_preset("green")).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(presets_frame, text="Blue", command=lambda: self.set_preset("blue")).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(presets_frame, text="Yellow", command=lambda: self.set_preset("yellow")).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(presets_frame, text="Orange", command=lambda: self.set_preset("orange")).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(presets_frame, text="Purple", command=lambda: self.set_preset("purple")).grid(row=1, column=2, padx=5, pady=5)
        
        # Quit button
        ttk.Button(controls_frame, text="Quit", command=self.window.quit).grid(row=9, column=0, columnspan=3, pady=10)
    
    def set_preset(self, color):
        presets = {
            "red": ([0, 100, 100], [10, 255, 255]), 
            "green": ([62.55, 39.76, 104.2], [97.2, 255, 255]),
            "blue": ([94.31, 45.24, 134.35], [158.8, 255, 255]),
            "yellow": ([20, 100, 100], [30, 255, 255]),
            "orange": ([10, 100, 20], [25, 255, 255]),
            "purple": ([125, 50, 50], [155, 255, 255])
        }
        
        lower, upper = presets[color]
        
        self.lower_h.set(lower[0])
        self.lower_s.set(lower[1])
        self.lower_v.set(lower[2])
        self.upper_h.set(upper[0])
        self.upper_s.set(upper[1])
        self.upper_v.set(upper[2])
    
    def update(self):
        ret, frame = self.cap.read()
        if ret:
            # Process the frame for color detection
            processed_frame = self.detect_color(frame)
            processed_frame = processed_frame[80:250, 150:440]
            
            # Convert from BGR to RGB 
            self.photo = self.convert_frame_to_photo(processed_frame)
            
            # Update the canvas
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        
        self.window.after(self.delay, self.update)
    
    def detect_color(self, frame):
        # Convert BGR to HSV 
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Get current HSV range values
        lower_color = np.array([self.lower_h.get(), self.lower_s.get(), self.lower_v.get()])
        upper_color = np.array([self.upper_h.get(), self.upper_s.get(), self.upper_v.get()])
        
        # Create mask for the specified color range
        mask = cv2.inRange(hsv, lower_color, upper_color)
        
        # Apply the mask to the original image
        result = cv2.bitwise_and(frame, frame, mask=mask)
        
        # Combine original and masked images for better visualization
        alpha = 0.7 
        combined = cv2.addWeighted(frame, alpha, result, 1 - alpha, 0)
        
        # Draw contours around detected areas
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(combined, contours, -1, (0, 255, 0), 2)
        
        return combined
    
    def convert_frame_to_photo(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_frame)
        photo = ImageTk.PhotoImage(image=pil_image)
        return photo
    
    def __del__(self):
        if hasattr(self, 'cap'):
            self.cap.release()

# Start the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ColorDetectionApp(root, "Real-time Color Detection")
    root.mainloop()