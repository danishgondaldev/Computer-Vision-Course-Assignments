from tkinter import *
from tkinter import filedialog, ttk
import cv2 as cv
from PIL import Image, ImageTk
import numpy as np
from tkinter.simpledialog import askstring

selected_image_path = None

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
        # Ensure that the frame is of type uint8
        frame = frame.astype(np.uint8)
        
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        resized_frame = cv.resize(rgb_frame, (600, 500))
        photo = ImageTk.PhotoImage(Image.fromarray(resized_frame))
        return photo
    else:
        return None


# Function to handle Browse button click event
def on_browse_clicked():
    global selected_image_path
    selected_image_path = filedialog.askopenfilename(
        title="Select Image", filetypes=[("image files", "*.jfif;*.jpg;*.png;*.svg;*.webp")]
    )
    frame = cv.imread(selected_image_path)
    frame = cv.normalize(frame, None, 0, 255, cv.NORM_MINMAX)
    frame = apply_frame_filter(frame)
    photo = convert_frame_to_photo(frame)

    if photo:
        image_frame_label.config(image=photo)
        image_frame_label.image = photo
        image_name_label.config(text=selected_image_path)
        print("Image file has been opened")
    else:
        print("Image file has not been opened")

# Function to set the filter of the frame based on the selected option
def apply_frame_filter(frame):
        if filter_var.get() == "Original Image":
            return frame
        elif filter_var.get() == "Negative":
            frame = cv.bitwise_not(frame)
            return frame
        elif filter_var.get() == "Log Transformation":
            scaling_factor = 20
            frame = cv.LUT(frame, scaling_factor * np.log1p(np.arange(256)))
            return frame
        elif filter_var.get() == "Gamma Transformation":
            frame = apply_gamma_transformation(frame)
            return frame
        elif filter_var.get() == "Contrast Sketch":
            frame = apply_contrast_sketch(frame)
            return frame
        elif filter_var.get() == "Intensity Level Sketch":
            intensity_sketch_type = ask_intensity_sketch_type()
            frame = apply_intensity_level_sketch(frame, intensity_sketch_type)
            return frame
        elif filter_var.get() == "Image Sharpening":
            frame = apply_laplacian_sharpening(frame)
            return frame

# Function to perform image sharpening using Laplacian filter without blur
def apply_laplacian_sharpening(frame):
    # Apply Laplacian filter for edge detection
    laplacian = cv.Laplacian(frame, cv.CV_64F)

    # Convert the data type of laplacian to match the data type of frame
    laplacian = np.uint8(np.absolute(laplacian))

    # Add the Laplacian to the original image to sharpen it
    sharpened = cv.addWeighted(frame, 1.5, laplacian, -0.5, 0)

    return sharpened



def ask_intensity_sketch_type():
    # Pop-up dialog to ask the user to choose the intensity sketch type
    intensity_sketch_type = askstring("Intensity Sketch Type", "Choose intensity sketch type:\n1. Binary\n2. Brighten/Darken")
    
    # Check the user's choice and return the appropriate value
    if intensity_sketch_type == "1":
        return "Binary"
    elif intensity_sketch_type == "2":
        return "BrightenDarken"
    else:
        # Default to Binary if an invalid choice is made
        return "Binary"

def apply_intensity_level_sketch(frame, intensity_sketch_type):
    # Convert to grayscale
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Apply the selected intensity sketch type
    if intensity_sketch_type == "Binary":
        _, binary_frame = cv.threshold(gray_frame, 128, 255, cv.THRESH_BINARY)
        intensity_sketch = cv.cvtColor(binary_frame, cv.COLOR_GRAY2BGR)
    elif intensity_sketch_type == "BrightenDarken":
        # Adjust the intensity levels based on your chosen approach
        # You can modify this part according to the chosen approach
        intensity_sketch = gray_frame  # Placeholder, modify this line

    return intensity_sketch

def apply_contrast_sketch(frame):
    # Convert to grayscale
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Apply Gaussian blur to the grayscale image
    blurred_frame = cv.GaussianBlur(gray_frame, (0, 0), 3)

    # Apply the high-pass filter to enhance edges
    contrast_sketch = gray_frame - blurred_frame

    # Invert the image for better visualization
    contrast_sketch = 255 - contrast_sketch

    # Convert back to BGR for display
    contrast_sketch = cv.cvtColor(contrast_sketch, cv.COLOR_GRAY2BGR)

    return contrast_sketch

def apply_gamma_transformation(frame, gamma=2.0):
    return cv.pow(frame/255.0, gamma) * 255.0 if frame is not None else None

# Function to handle filter_size change event
def on_filter_size_change(event):
    global playback_filter_size
    playback_filter_size = int(filter_size_var.get())

# Function to handle filter change event
def on_filter_change(event):
    update_displayed_frame()

# Function to update displayed frame
def update_displayed_frame():
    global selected_image_path
    if selected_image_path:
        frame = cv.imread(selected_image_path)
        frame = apply_frame_filter(frame)
        photo = convert_frame_to_photo(frame)

        if photo:
            image_frame_label.config(image=photo)
            image_frame_label.image = photo
            print("Frame has been updated with new filter")
        else:
            print("Frame has not been updated")

# Initializing the root window
root_window = Tk()
root_window.title("Filters Application") 
root_window.configure(bg="light green")
screen_width, screen_height = get_screen_resolution()
root_window.geometry(f"{screen_width}x{screen_height}")
root_window.columnconfigure(0, weight=1)

# Container for image name and browse Button
frame_header = Frame(root_window, padx=5, pady=5, bd=2)
frame_header.grid(row=0, column=0, pady=20)

# Label that displays image name
image_name_frame = Frame(frame_header, padx=5, pady=20, bd=10, relief=SOLID, bg="sea green")
image_name_frame.pack(side="top")
image_name_label = Label(image_name_frame, text="Filters Application", width=60, font=("Times New Roman", 18))
image_name_label.pack()

def resize_image(image_path, new_width, new_height):
    image = Image.open(image_path)
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(resized_image)

# Label that displays image name
image_name_frame = Frame(frame_header, padx=5, pady=5, bd=2, relief=SOLID)
image_name_frame.pack(side="left", pady=(10, 0))  # Add a top margin of 10 pixels
image_name_label = Label(image_name_frame, text="Image File Name", width=80, bg="light green", font=("Times New Roman", 12))
image_name_label.pack()

# Browse Button
browse_button = Button(frame_header, text="Browse Files", command=on_browse_clicked, bg="light green", font=("Times New Roman", 12), width=15)
browse_button.pack(side="left", padx=10, pady=(10, 0))

# Image Display
image_frame = Frame(root_window, height=500, width=600, padx=5, pady=5, bd=2, relief=SOLID)
image_frame.grid(row=1, column=0)
image_frame.pack_propagate(False)
image_frame_label = Label(image_frame)
image_frame_label.pack()

# image Options Panel
image_option_frame = Frame(root_window, padx=5, pady=5, bd=2)
image_option_frame.grid(row=2, column=0)

# Combobox for changing filter_size
filter_size_var = StringVar()

# Create a label before the Combobox
filter_size_label = Label(image_option_frame, text="Select Filter Size:", font=("Times New Roman", 12))
filter_size_label.pack(side=LEFT, padx=1.5)

filter_size_combobox = ttk.Combobox(image_option_frame, textvariable=filter_size_var, values=["1", "3", "5"], state="readonly", font=("Times New Roman", 12))
filter_size_combobox.set("1")
filter_size_combobox.bind("<<ComboboxSelected>>", on_filter_size_change)
filter_size_combobox.pack(side=LEFT, padx=10)

# Combobox for changing filters
filter_var = StringVar()

# Create a label before the Combobox
filter_label = Label(image_option_frame, text="Select Filter:", font=("Times New Roman", 12))
filter_label.pack(side=LEFT, padx=1.5)

filter_combobox = ttk.Combobox(image_option_frame, textvariable=filter_var,
                          values=["Original Image", "Negative", "Log Transformation", "Gamma Transformation", "Contrast Sketch", "Intensity Level Sketch", "Image Sharpening"],
                          state="readonly", font=("Times New Roman", 12))
filter_combobox.set("Original Image")
filter_combobox.bind("<<ComboboxSelected>>", on_filter_change)
filter_combobox.pack(side=LEFT, padx=10)

# Running Program
root_window.mainloop()
