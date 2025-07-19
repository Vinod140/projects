import cv2
import sys
import tkinter as tk
from tkinter import filedialog, Toplevel
from ultralytics import YOLO
from PIL import Image, ImageTk
import pygame
from tkinter import Canvas
import os



# Detect if running as EXE or script
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

# Define YOLO model path
model_path = os.path.join(base_path, "c:/Users/pankaj/Desktop/major/runs/detect/train4/weights/best.pt")
if not os.path.exists(model_path):
    print(f"ERROR: Model file not found at {model_path}")
    exit(1)

# Load trained YOLOv8 model
model = YOLO(model_path)

# Initialize Tkinter main window
root = tk.Tk()
root.title("Object Detection App")
root.attributes('-fullscreen', True)  # Fullscreen mode

# Get Screen Dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()



# Function to Set Background Image

def set_background(image_path):
    global bg_image
    img = Image.open(image_path)
    img = img.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(img)  # Store reference

    canvas = Canvas(root, width=screen_width, height=screen_height, highlightthickness=0)
    canvas.place(x=0, y=0)  # Cover full screen
    canvas.create_image(0, 0, anchor="nw", image=bg_image)

# Set Background Image
set_background("library/bk1.jpg")  # Ensure correct path

# Function to Add a Premium Title at the Top
def create_premium_title():
    title_text = "    Real-Time Object Detection          "  # Add spaces for better flow

    title_label = tk.Label(root, text=title_text, font=("Arial", 32, "bold"),
                           fg="white", bg="#2E86C1", bd=5, relief="groove", padx=10, pady=5)
    title_label.place(relx=0.5, rely=0.05, anchor="center")  # Top Center

    def marquee():
        current_text = title_label.cget("text")
        new_text = current_text[1:] + current_text[0]  # Rotate text
        title_label.config(text=new_text)
        root.after(250, marquee)  # Speed (milliseconds)

    marquee()

# Call the function after setting background
create_premium_title()

# Button Style (Transparent Background)
button_style = {
    "font": ("Arial", 14, "bold"),
    "fg": "white",
    "borderwidth": 0,  # Remove border
    "activebackground": "#000000",  # Dark on hover
    "activeforeground": "white",
    "relief": "flat",
    "bd": 0,
    "highlightthickness": 0,
    "width": 20,
    "height": 2,
    "cursor": "hand2",  # Hand cursor on hover
    "borderwidth": 0,
    "highlightthickness": 0,
    "padx": 10,
    "pady": 10,
    "font": ("Arial", 16, "bold")
}

# Function to Create Rounded Button with Hover Effect
def create_button(text, command, y_position, bg_color):
    btn = tk.Button(root, text=text, command=command, bg=bg_color, **button_style)
    btn.place(relx=0.5, rely=y_position, anchor="center", width=200, height=50)

    # Round the corners by using a canvas and adding the button on top of it
    btn.config(relief="solid", borderwidth=0, highlightthickness=0)
    btn.config(bg=bg_color, activebackground=bg_color, activeforeground="white")

    return btn

# Buttons
create_button("Start Webcam", lambda: open_detection_window("webcam"), 0.4, "#5DADE2")
create_button("Start Mobile Camera", lambda: get_mobile_url(), 0.47, "#AF7AC5")
create_button("Select Video", lambda: open_detection_window("video"), 0.54, "#F5B041")
create_button("Select Images", lambda: open_detection_window("image"), 0.61, "#52BE80")
create_button("Exit Application", root.destroy, 0.68, "#EC7063")

# Function to Process Images
def process_images(window, file_path):
    image = cv2.imread(file_path)
    if image is None:
        print("ERROR: Could not load image.")
        return
    results = model(image)
    annotated_image = results[0].plot()
    annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(annotated_image)
    img = img.resize((700, 500), Image.LANCZOS)
    imgtk = ImageTk.PhotoImage(image=img)
    lbl_video = tk.Label(window, bg="#F8F9FA")
    lbl_video.pack()
    lbl_video.imgtk = imgtk
    lbl_video.configure(image=imgtk)

    btn_exit = tk.Button(window, text="Exit", command=window.destroy, bg="red", **button_style)
    btn_exit.pack(side="bottom", pady=10)

# Function to Open Detection Window
def open_detection_window(source, mobile_url=None):
    global cap  
    file_path = None
    if source in ["video", "image"]:
        file_path = filedialog.askopenfilename(filetypes=[("Media Files", "*.mp4;*.avi;*.mov;*.jpg;*.jpeg;*.png")])
        if not file_path:
            return
    
    detection_window = Toplevel(root)
    detection_window.title(f"{source.capitalize()} Detection")
    detection_window.geometry("1000x700")  
    detection_window.configure(bg="#F8F9FA")  
    detection_window.grab_set()
    detection_window.attributes('-topmost', True)
    
    lbl_video = tk.Label(detection_window, bg="#F8F9FA")
    lbl_video.pack()

    cap = None
    running = True
    
    def update_frame():
        nonlocal running
        if not running or cap is None:
            return
        ret, frame = cap.read()
        if not ret:
            print("ERROR: Failed to grab frame")
            detection_window.destroy()
            return
        results = model(frame)
        annotated_frame = results[0].plot()
        frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = img.resize((950, 650), Image.LANCZOS)
        imgtk = ImageTk.PhotoImage(image=img)
        lbl_video.imgtk = imgtk
        lbl_video.configure(image=imgtk)
        lbl_video.after(10, update_frame)
    
    if source == "webcam":
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("ERROR: Could not open webcam")
            detection_window.destroy()
            return

    elif source == "mobile":
        if mobile_url:
            cap = cv2.VideoCapture(mobile_url)
            if not cap.isOpened():
                print("ERROR: Could not open mobile stream")
                detection_window.destroy()
                return
        else:
            print("ERROR: No URL provided for mobile stream")
            detection_window.destroy()
            return

    elif source == "video":
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            print("ERROR: Could not open video file")
            detection_window.destroy()
            return

    elif source == "image":
        process_images(detection_window, file_path)
        return

    update_frame()

    def stop_detection():
        nonlocal running
        running = False
        if cap:
            cap.release()
        detection_window.destroy()

    btn_exit = tk.Button(detection_window, text="Exit", command=stop_detection, bg="red", **button_style)
    btn_exit.pack(side="bottom", pady=10)

# Function to Get Mobile Camera URL from User
def get_mobile_url():
    # Create a window to get mobile URL dynamically
    url_window = Toplevel(root)
    url_window.title("Enter Mobile Camera URL")
    url_window.geometry("400x200")

    # Label for URL input
    url_label = tk.Label(url_window, text="Enter Mobile Camera URL:")
    url_label.pack(pady=10)

    # Input field for URL
    url_entry = tk.Entry(url_window, width=50)
    url_entry.pack(pady=10)

    def submit_url():
        # Get the entered URL and close the window
        mobile_url = url_entry.get()
        if mobile_url:
            # Proceed to open the detection window with the provided URL
            open_detection_window("mobile", mobile_url)
            url_window.destroy()  # Close the URL entry window
        else:
            print("ERROR: Please enter a valid URL")

    submit_button = tk.Button(url_window, text="Submit", command=submit_url)
    submit_button.pack(pady=20)

# Play Background Music
def play_background_music():
    pygame.mixer.init()
    pygame.mixer.music.load("library/bk_music.mp3")  # Ensure this file exists
    pygame.mixer.music.play(-1)

play_background_music()



root.mainloop()
