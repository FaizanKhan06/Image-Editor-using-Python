import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2

# Global variable to store original image size
original_size = [0,0]
resized_size = [0,0]
undo_stack = []

# Function to open a new window for resizing the image
def open_resize_window():
    global original_size
    resize_window = tk.Toplevel(root)
    resize_window.title("Resize Image")
    
    # Width entry field
    width_label = tk.Label(resize_window, text="Width:")
    width_label.grid(row=0, column=0, padx=10, pady=10)
    width_entry = tk.Entry(resize_window)
    width_entry.grid(row=0, column=1, padx=10, pady=10)
    
    # Height entry field
    height_label = tk.Label(resize_window, text="Height:")
    height_label.grid(row=1, column=0, padx=10, pady=10)
    height_entry = tk.Entry(resize_window)
    height_entry.grid(row=1, column=1, padx=10, pady=10)
    
    # OK button to trigger image resizing
    ok_button = tk.Button(resize_window, text="OK", command=lambda: resize_image(width_entry.get(), height_entry.get()))
    ok_button.grid(row=2, column=0, columnspan=2, pady=10)
    
    
    # Revert button to restore the image to its original size
    def revert_image():
        width_entry.delete(0, tk.END)
        height_entry.delete(0, tk.END)
        width_entry.insert(0, str(original_size[0]))
        height_entry.insert(0, str(original_size[1]))
        resize_image(original_size[0], original_size[1])

    revert_button = tk.Button(resize_window, text="Revert", command=revert_image)
    revert_button.grid(row=3, column=0, columnspan=2, pady=10)            
    
    # Label to display error message
    error_label = tk.Label(resize_window, fg="red")
    error_label.grid(row=4, column=0, columnspan=2)

# Function to open a new window for Adding Text On image
def Open_Text_On_Image_window():
    resize_window = tk.Toplevel(root)
    resize_window.title("Text On Image")

    # Text entry field
    Text_label = tk.Label(resize_window, text="Text:")
    Text_label.grid(row=0, column=0, padx=10, pady=10)
    Text_entry = tk.Entry(resize_window)
    Text_entry.grid(row=0, column=1, padx=10, pady=10)
    
    # X entry field
    Position_x_label = tk.Label(resize_window, text="Position_x:")
    Position_x_label.grid(row=1, column=0, padx=10, pady=10)
    Position_x_entry = tk.Entry(resize_window)
    Position_x_entry.grid(row=1, column=1, padx=10, pady=10)
    
    # y entry field
    Position_y_label = tk.Label(resize_window, text="Position_y:")
    Position_y_label.grid(row=2, column=0, padx=10, pady=10)
    Position_y_entry = tk.Entry(resize_window)
    Position_y_entry.grid(row=2, column=1, padx=10, pady=10)
    
    # OK button to trigger image resizing
    ok_button = tk.Button(resize_window, text="OK", command=lambda: Add_Text(Text_entry.get(),int(Position_x_entry.get()),int(Position_y_entry.get())))
    ok_button.grid(row=3, column=0, columnspan=2, pady=10)           
    
    # Label to display error message
    error_label = tk.Label(resize_window, fg="red")
    error_label.grid(row=4, column=0, columnspan=2)

# Function to resize the image based on user input
def resize_image(width, height):
    global resized_size, original_image,undo_stack
    try:
        undo_stack.append(original_image)
        new_width = int(width)
        new_height = int(height)
        resized_image = cv2.resize(original_image, (new_width, new_height))
        resized_image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(resized_image_rgb))
        image_label.config(image=photo)
        image_label.image = photo
        resized_size=[new_width,new_height]
        original_image = resized_image
    except ValueError:
        print(text="Invalid input. Please enter valid width and height.")

# Function to load and display the selected image
def load_image():
    global original_image, original_size,undo_stack
    file_path = filedialog.askopenfilename()
    if file_path:
        # Load the image using OpenCV
        original_image = cv2.imread(file_path)
        # Get the maximum window height
        max_height = root.winfo_screenheight() - 100
        # Calculate the aspect ratio of the image
        aspect_ratio = original_image.shape[1] / original_image.shape[0]
        # Calculate the new width based on the maximum height and aspect ratio
        new_width = int(max_height * aspect_ratio)
        # Resize the image to fit the maximum window height without increasing the width
        resized_image = cv2.resize(original_image, (new_width, max_height))
        # Store the original size
        global original_size
        original_size = [new_width, max_height]
        global resized_size
        resized_size = [new_width, max_height]

        #resize the image
        resize_image(original_size[0], original_size[1])
        # Convert the image to RGB format for displaying in Tkinter
        resized_image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        # Create a PIL ImageTk object from the resized image
        photo = ImageTk.PhotoImage(image=Image.fromarray(resized_image_rgb))
        image_label.config(image=photo)
        image_label.image = photo

def convert_to_grayscale():
    global original_image, original_size,undo_stack
    if original_image is not None:
        undo_stack.append(original_image)
        # Convert the image to grayscale using OpenCV
        grayscale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        # Convert grayscale image to RGB format for displaying in Tkinter
        grayscale_image_rgb = cv2.cvtColor(grayscale_image, cv2.COLOR_GRAY2RGB)
        # Create a PIL ImageTk object from the grayscale image
        photo = ImageTk.PhotoImage(image=Image.fromarray(grayscale_image_rgb))
        image_label.config(image=photo)
        image_label.image = photo
        original_image = grayscale_image
    else:
        # If no image is loaded, display an error message
        print(text="No image loaded. Please load an image first.")

def Add_Text(text, x, y):
    global original_image, original_size,undo_stack
    if original_image is not None:
        undo_stack.append(original_image)
        
        # Convert the image to grayscale using OpenCV
        Text_image = original_image
        
        # Place text on the image using OpenCV
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_color = (255, 255, 255)  # White color in BGR
        font_thickness = 2
        cv2.putText(Text_image, text, (x, y), font, font_scale, font_color, font_thickness)

        Text_image_rgb = cv2.cvtColor(Text_image, cv2.COLOR_BGR2RGB)
        
        # Create a PIL ImageTk object from the modified grayscale image
        photo = ImageTk.PhotoImage(image=Image.fromarray(Text_image_rgb))
        
        # Update the Tkinter label with the modified image
        image_label.config(image=photo)
        image_label.image = photo
        
        original_image = Text_image
    else:
        # If no image is loaded, display an error message
        print("No image loaded. Please load an image first.")

def convert_to_Negative_Image():
    global original_image, original_size,undo_stack
    if original_image is not None:
        undo_stack.append(original_image)
        # Convert the image to negative
        negative_image = cv2.bitwise_not(original_image)
        # Convert negative image to RGB format for displaying in Tkinter
        negative_image_rgb = cv2.cvtColor(negative_image, cv2.COLOR_BGR2RGB)
        # Create a PIL ImageTk object from the negative image
        photo = ImageTk.PhotoImage(image=Image.fromarray(negative_image_rgb))
        image_label.config(image=photo)
        image_label.image = photo
        original_image = negative_image
    else:
        # If no image is loaded, display an error message
        print(text="No image loaded. Please load an image first.")

def crop_image():
    global original_image, undo_stack
    undo_stack.append(original_image)
    r = cv2.selectROI(original_image)
    cropped = original_image[r[1]:r[1]+r[3], r[0]:r[0]+r[2]]

    cropped_image = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
    
    # Create a PIL ImageTk object from the modified grayscale image
    photo = ImageTk.PhotoImage(image=Image.fromarray(cropped_image))
        
        # Update the Tkinter label with the modified image
    image_label.config(image=photo)
    image_label.image = photo
        
    original_image = cropped_image

def rotate_image():
    global original_image, undo_stack
    undo_stack.append(original_image)

    # Rotate the image 90 degrees clockwise
    rotated_image = cv2.rotate(original_image, cv2.ROTATE_90_CLOCKWISE)

    # Convert the color space from BGR to RGB
    rotated_image_rgb = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2RGB)

    # Create a PIL ImageTk object from the modified RGB image
    photo = ImageTk.PhotoImage(image=Image.fromarray(rotated_image_rgb))

    # Update the Tkinter label with the modified image
    image_label.config(image=photo)
    image_label.image = photo

    # Update the original_image to the rotated image for further rotations
    original_image = rotated_image

def Flip_vertically_image():
    global original_image, undo_stack
    undo_stack.append(original_image)

    # Rotate the image 90 degrees clockwise
    rotated_image = cv2.flip(original_image, 0)

    # Convert the color space from BGR to RGB
    rotated_image_rgb = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2RGB)

    # Create a PIL ImageTk object from the modified RGB image
    photo = ImageTk.PhotoImage(image=Image.fromarray(rotated_image_rgb))

    # Update the Tkinter label with the modified image
    image_label.config(image=photo)
    image_label.image = photo

    # Update the original_image to the rotated image for further rotations
    original_image = rotated_image

def Flip_horizontally_image():
    global original_image, undo_stack
    undo_stack.append(original_image)

    # Rotate the image 90 degrees clockwise
    rotated_image = cv2.flip(original_image, 2)

    # Convert the color space from BGR to RGB
    rotated_image_rgb = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2RGB)

    # Create a PIL ImageTk object from the modified RGB image
    photo = ImageTk.PhotoImage(image=Image.fromarray(rotated_image_rgb))

    # Update the Tkinter label with the modified image
    image_label.config(image=photo)
    image_label.image = photo

    # Update the original_image to the rotated image for further rotations
    original_image = rotated_image

def sketch_effect_image():
    global original_image, undo_stack
    undo_stack.append(original_image)

    # Rotate the image 90 degrees clockwise
    pencil,colored = cv2.pencilSketch(original_image, 200, 0.1, shade_factor=0.1)

    # Convert the color space from BGR to RGB
    pencil_image_rgb = cv2.cvtColor(pencil, cv2.COLOR_BGR2RGB)

    # Create a PIL ImageTk object from the modified RGB image
    photo = ImageTk.PhotoImage(image=Image.fromarray(pencil_image_rgb))

    # Update the Tkinter label with the modified image
    image_label.config(image=photo)
    image_label.image = photo

    # Update the original_image to the rotated image for further rotations
    original_image = pencil

def color_sketch_effect_image():
    global original_image, undo_stack
    undo_stack.append(original_image)

    # Rotate the image 90 degrees clockwise
    pencil,colored = cv2.pencilSketch(original_image, 200, 0.1, shade_factor=0.1)

    # Convert the color space from BGR to RGB
    colored_image_rgb = cv2.cvtColor(colored, cv2.COLOR_BGR2RGB)

    # Create a PIL ImageTk object from the modified RGB image
    photo = ImageTk.PhotoImage(image=Image.fromarray(colored_image_rgb))

    # Update the Tkinter label with the modified image
    image_label.config(image=photo)
    image_label.image = photo

    # Update the original_image to the rotated image for further rotations
    original_image = colored

def Undo():
    global original_image, original_size,undo_stack
    if original_image is not None:
        # Convert the image to negative
        image = undo_stack.pop()
        # Convert negative image to RGB format for displaying in Tkinter
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Create a PIL ImageTk object from the negative image
        photo = ImageTk.PhotoImage(image=Image.fromarray(image_rgb))
        image_label.config(image=photo)
        image_label.image = photo
        original_image = image
    else:
        # If no image is loaded, display an error message
        print(text="No image loaded. Please load an image first.")

def adding_buttons():
    global button_size_array
    # Create a button to load an image
    undo_button = tk.Button(root, text="Undo", command=Undo)
    undo_button.place(x=0,y=0)
    button_size_array.append(undo_button.winfo_reqwidth())

    # Create a button to load an image
    load_button = tk.Button(root, text="Load Image", command=load_image)
    load_button.place(x=sum(button_size_array[0:2]),y=0)
    button_size_array.append(load_button.winfo_reqwidth())

    # Button to open resize window
    resize_button = tk.Button(root, text="Resize Image", command=open_resize_window)
    resize_button.place(x=sum(button_size_array[0:3]),y=0)
    button_size_array.append(resize_button.winfo_reqwidth())

    # Button to Convert to Grayscale
    grayscale_button = tk.Button(root, text="Grayscale", command=convert_to_grayscale)
    grayscale_button.place(x=sum(button_size_array[0:4]),y=0)
    button_size_array.append(grayscale_button.winfo_reqwidth())

    # Button to Convert to Negative
    Negative_Image_button = tk.Button(root, text="Negative Image", command=convert_to_Negative_Image)
    Negative_Image_button.place(x=sum(button_size_array[0:5]),y=0)
    button_size_array.append(Negative_Image_button.winfo_reqwidth())

    # Button to Write Text on Image
    Text_on_Image_button = tk.Button(root, text="Text", command=Open_Text_On_Image_window)
    Text_on_Image_button.place(x=sum(button_size_array[0:6]),y=0)
    button_size_array.append(Text_on_Image_button.winfo_reqwidth())

    # Button to Crop an Image
    Crop_Image_button = tk.Button(root, text="Crop", command=crop_image)
    Crop_Image_button.place(x=sum(button_size_array[0:7]),y=0)
    button_size_array.append(Crop_Image_button.winfo_reqwidth())

    # Button to Rotate an Image
    rotate_Image_button = tk.Button(root, text="Rotate", command=rotate_image)
    rotate_Image_button.place(x=sum(button_size_array[0:8]),y=0)
    button_size_array.append(rotate_Image_button.winfo_reqwidth())

    # Button to Flip an Image
    Flip_vertically_Image_button = tk.Button(root, text="Flip Vertically", command=Flip_vertically_image)
    Flip_vertically_Image_button.place(x=sum(button_size_array[0:9]),y=0)
    button_size_array.append(Flip_vertically_Image_button.winfo_reqwidth())

    # Button to Flip an Image
    Flip_horizontally_Image_button = tk.Button(root, text="Flip Horizontally", command=Flip_horizontally_image)
    Flip_horizontally_Image_button.place(x=sum(button_size_array[0:9]),y=0)
    button_size_array.append(Flip_horizontally_Image_button.winfo_reqwidth())

    # Button to sketch_effect an Image
    sketch_effect_Image_button = tk.Button(root, text="Sketch Effect", command=sketch_effect_image)
    sketch_effect_Image_button.place(x=sum(button_size_array[0:10]),y=0)
    button_size_array.append(sketch_effect_Image_button.winfo_reqwidth())

    # Button to color sketch_effect an Image
    color_sketch_effect_Image_button = tk.Button(root, text="Color Sketch Effect", command=color_sketch_effect_image)
    color_sketch_effect_Image_button.place(x=sum(button_size_array[0:11]),y=0)
    button_size_array.append(color_sketch_effect_Image_button.winfo_reqwidth())

# Create the main window
root = tk.Tk()
root.title("Image Viewer")

# Set window attributes to maximize the window by default and prevent resizing
root.state('zoomed')

button_size_array = []
adding_buttons()
# Label to display the loaded image
image_label = tk.Label(root)
image_label.place(x=550, y=30)

# Run the Tkinter main loop
root.mainloop()
