from tkinter import *
from tkinter import filedialog, ttk
import cv2 as cv
from PIL import Image, ImageTk
import time

# Video file and player variables
video_source = None
is_video_paused = True
video_fps = None
playback_speed = 1

# Function to retrieve screen resolution
def get_screen_resolution():
    root = Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    return screen_width, screen_height

# Function to convert OpenCV frame to PhotoImage
def convert_frame_to_photo(frame):
    if frame is not None:
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        resized_frame = cv.resize(rgb_frame, (1300, 450))
        photo = ImageTk.PhotoImage(Image.fromarray(resized_frame))
        return photo
    else:
        return None

# Function to set the initial frame of the video
def initialize_video_frame(video_cap):
    if video_cap.isOpened():
        global video_source
        global video_fps
        video_source = video_cap
        video_fps = video_source.get(cv.CAP_PROP_FPS)
        ret, frame = video_cap.read()
        photo = convert_frame_to_photo(frame)
        video_frame_label.config(image=photo)
        video_frame_label.image = photo
        return True
    else:
        return False

# Function to handle Browse button click event
def on_browse_clicked():
    selected_video_path = filedialog.askopenfilename(
        title="Select Video", filetypes=[("Video files", "*.mp4;*.avi;*.mkv;*.mov;*.wmv")]
    )
    video_cap = cv.VideoCapture(selected_video_path)

    if initialize_video_frame(video_cap):
        video_name_label.config(text=selected_video_path)
        print("Video file has been opened")
    else:
        print("Video file not opened!")

# Function to open the camera selection modal
def open_camera_modal():
    def open_camera(camera_index):
        video_cap = cv.VideoCapture(camera_index)
        if initialize_video_frame(video_cap):
            video_name_label.config(text=f"Camera {camera_index}")
            print("Video file has been opened")
            close_modal()

    def close_modal():
        modal_window.destroy()

    modal_window = Toplevel(root_window)
    modal_window.title("Choose Camera")

    btn_primary_cam = Button(modal_window, text="Primary", command=lambda: open_camera(0), bg="light green", font=("Times New Roman", 12), width=15)
    btn_primary_cam.pack(pady=5)

    btn_secondary_cam = Button(modal_window, text="Secondary", command=lambda: open_camera(1), bg="light green", font=("Times New Roman", 12), width=15)
    btn_secondary_cam.pack(pady=5)

    close_button = Button(modal_window, text="Close", font=("Times New Roman", 12), bg="light green", width=15, command=modal_window.destroy)
    close_button.pack(pady=10)

    modal_window.geometry("+{}+{}".format(
        root_window.winfo_screenwidth() // 2 - modal_window.winfo_reqwidth() // 2,
        root_window.winfo_screenheight() // 2 - modal_window.winfo_reqheight() // 2
    ))

    modal_window.transient(root_window)
    modal_window.grab_set()
    root_window.wait_window(modal_window)

# Function to set the color of the frame based on the selected option
def apply_frame_color(frame):
    if color_var.get() == "Color":
        return frame
    elif color_var.get() == "Gray Scale":
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        return cv.cvtColor(frame, cv.COLOR_GRAY2BGR)
    elif color_var.get() == "Black and White":
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        _, frame = cv.threshold(frame, 128, 255, cv.THRESH_BINARY)
        return cv.cvtColor(frame, cv.COLOR_GRAY2BGR)

    elif color_var.get() == "Blue Channel":
        frame[:, :, 1] = 0
        frame[:, :, 2] = 0
        return frame
    elif color_var.get() == "Green Channel":
        frame[:, :, 0] = 0
        frame[:, :, 2] = 0
        return frame
    elif color_var.get() == "Red Channel":
        frame[:, :, 0] = 0
        frame[:, :, 1] = 0
        return frame

# Function to play and pause the video
def play_pause_video():
    global is_video_paused
    if is_video_paused:
        is_video_paused = False
        global video_source

        while not is_video_paused:
            start_time = time.time()
            ret, frame = video_source.read()

            if not ret:
                video_source.set(cv.CAP_PROP_POS_FRAMES, 0)
                break

            frame = apply_frame_color(frame)
            photo = convert_frame_to_photo(frame)

            if photo:
                video_frame_label.config(image=photo)
                video_frame_label.image = photo
                root_window.update()

                elapsed_time = time.time() - start_time
                delay = max(0, 1 / (playback_speed * video_fps) - elapsed_time)
                time.sleep(delay)
    else:
        is_video_paused = True
        root_window.update()

# Function to handle speed change event
def on_speed_change(event):
    global playback_speed
    playback_speed = int(speed_var.get())

# Initializing the root window
root_window = Tk()
root_window.configure(bg="light green")
screen_width, screen_height = get_screen_resolution()
root_window.geometry(f"{screen_width}x{screen_height}")
root_window.columnconfigure(0, weight=1)

# Container for video name and browse Button
frame_header = Frame(root_window, padx=5, pady=5, bd=2)
frame_header.grid(row=0, column=0, pady=20)

# Label that displays video name
video_name_frame = Frame(frame_header, padx=5, pady=20, bd=10, relief=SOLID, bg="sea green")
video_name_frame.pack(side="top")
video_name_label = Label(video_name_frame, text="My Video Player", width=60, font=("Times New Roman", 18))
video_name_label.pack()

def resize_image(image_path, new_width, new_height):
    image = Image.open(image_path)
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(resized_image)

# Camera Icon Button
camera_icon = PhotoImage(file='D:\CVIP\Week3\Assignments\Assignment 2\camera_icon.png')
camera_icon = resize_image('D:\CVIP\Week3\Assignments\Assignment 2\camera_icon.png', 50, 50)
camera_button = Button(frame_header, bd=0.5, image=camera_icon, command=open_camera_modal)
camera_button.pack(side="left", padx=170, pady=10)

# Label that displays video name
video_name_frame = Frame(frame_header, padx=5, pady=5, bd=2, relief=SOLID)
video_name_frame.pack(side="left")
video_name_label = Label(video_name_frame, text="Video File Name", width=80, bg="light green", font=("Times New Roman", 12))
video_name_label.pack()

# Browse Button
browse_button = Button(frame_header, text="Browse Files", command=on_browse_clicked, bg="light green", font=("Times New Roman", 12), width=15)
browse_button.pack(side="left", padx=120)

# Video Player
video_frame = Frame(root_window, height=450, width=1300, padx=5, pady=5, bd=2, relief=SOLID)
video_frame.grid(row=1, column=0)
video_frame.pack_propagate(False)
video_frame_label = Label(video_frame)
video_frame_label.pack()

# Video Options Panel
video_option_frame = Frame(root_window, padx=5, pady=5, bd=2)
video_option_frame.grid(row=2, column=0)

# Combobox for changing speed
speed_var = StringVar()

# Create a label before the Combobox
speed_label = Label(video_option_frame, text="Select Speed:", font=("Times New Roman", 12))
speed_label.pack(side=LEFT, padx=10)

speed_combobox = ttk.Combobox(video_option_frame, textvariable=speed_var, values=["1", "2", "3"], state="readonly", font=("Times New Roman", 12))
speed_combobox.set("1")
speed_combobox.bind("<<ComboboxSelected>>", on_speed_change)
speed_combobox.pack(side=LEFT, padx=20)

# Combobox for changing colors
color_var = StringVar()

# Create a label before the Combobox
color_label = Label(video_option_frame, text="Select Color:", font=("Times New Roman", 12))
color_label.pack(side=LEFT, padx=10)

color_combobox = ttk.Combobox(video_option_frame, textvariable=color_var,
                          values=["Color", "Gray Scale", "Black and White", "Blue Channel", "Red Channel", "Green Channel"],
                          state="readonly", font=("Times New Roman", 12))
color_combobox.set("Color")
color_combobox.pack(side=LEFT, padx=20)

# Play and pause icon
play_pause_icon = PhotoImage(file='D:\CVIP\Week3\Assignments\Assignment 2\play_pause_icon.png')
play_pause_icon = resize_image('D:\CVIP\Week3\Assignments\Assignment 2\play_pause_icon.png', 60, 50)

# Play and pause button
play_pause_button = Button(video_option_frame, bd=0.5, image=play_pause_icon, command=play_pause_video)
play_pause_button.pack(side="left", padx=25, pady=10)

# Running Program
root_window.mainloop()
