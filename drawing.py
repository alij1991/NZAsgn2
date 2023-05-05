import tkinter as tk
from tkinter import colorchooser, filedialog
from PIL import ImageGrab
import numpy as np
import tensorflow.keras as keras
from keras.models import load_model
from processing import AlphabetRecognition

class PaintApp():

    # Initialize brush size
    brush_size = 5

    # Initialize brush color
    brush_color = "black"

    last_x = None
    last_y = None
    canvas = None
    result_text_id = None

    

    def __init__(self, root):
        # Create the main window
        self.root = root
        self.root.title("Paint App")
        
        #Buttons details
        number_of_buttons = 8
        buttons_width = 15
        buttons_height = 2
        # Create a canvas to draw on
        canvas_width = 600
        canvas_height = 400
        self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES, padx=10, pady=10)

        # Create a frame for the buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=tk.YES, padx=10, pady=10)

        # Bind brush draw function to left mouse button
        self.canvas.bind("<B1-Motion>", self.brush_draw)
        self.canvas.bind("<ButtonRelease-1>", lambda event: self.reset_position())
        # Create brush size buttons
        brush_size_button_1 = tk.Button(button_frame, text="Small Brush", width= buttons_width, height= buttons_height, command=lambda: self.set_brush_size(8))
        brush_size_button_2 = tk.Button(button_frame, text="Medium Brush", width= buttons_width, height= buttons_height, command=lambda: self.set_brush_size(12))
        brush_size_button_3 = tk.Button(button_frame, text="Large Brush", width= buttons_width, height= buttons_height, command=lambda: self.set_brush_size(16))

        # Create brush color button
        brush_color_button = tk.Button(button_frame, text="Choose Color", width= buttons_width, height= buttons_height, command=self.set_brush_color)

        # Create save drawing button
        save_button = tk.Button(button_frame, text="Save", width= buttons_width, height= buttons_height, command=self.save_drawing)

        # Create load drawing button
        load_button = tk.Button(button_frame, text="Load", width= buttons_width, height= buttons_height, command=self.load_drawing)

        # Create clear drawing button
        clear_button = tk.Button(button_frame, text="Clear", width= buttons_width, height= buttons_height, command=self.clear_drawing)

        # Create processing drawing button for multiple letters
        process_multiple_letters_button = tk.Button(button_frame, text="Multiple letters process", width= buttons_width, height= buttons_height, command=self.process_drawing_multiple_letter)

        # Create processing drawing button for single letter
        process_single_letters_button = tk.Button(button_frame, text="Single letter process", width= buttons_width, height= buttons_height, command=self.process_drawing_single_letter)


        brush_size_button_1.pack(pady=number_of_buttons)
        brush_size_button_2.pack(pady=number_of_buttons)
        brush_size_button_3.pack(pady=number_of_buttons)
        brush_color_button.pack(pady=number_of_buttons)
        save_button.pack(pady=number_of_buttons)
        load_button.pack(pady=number_of_buttons)
        clear_button.pack(pady=number_of_buttons)
        process_single_letters_button.pack(pady=number_of_buttons)
        process_multiple_letters_button.pack(pady=number_of_buttons)
        
        
    # Define brush size
    def set_brush_size(self,new_size):
        self.brush_size = new_size

    # Define brush color
    def set_brush_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.brush_color = color


    def brush_draw(self,event=None):
    
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, width=self.brush_size, fill=self.brush_color, capstyle=tk.ROUND, smooth=True)
        self.last_x, self.last_y = event.x, event.y


    def reset_position(self):
        self.last_x = None
        self.last_y = None
    # Define clear canvas function
    def clear_canvas(self):
        self.canvas.delete("all")
        self.canvas.config(bg="white")

    # Define save drawing function
    def save_drawing(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                for item in self.canvas.find_all():
                    coords = self.canvas.coords(item)
                    color = self.canvas.itemcget(item, "fill")
                    file.write(f"{coords[0]},{coords[1]},{coords[2]},{coords[3]},{color}\n")



    def load_drawing(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.clear_canvas()
            with open(file_path, "r") as file:
                for line in file:
                    item_data = line.strip().split(",")
                    coords = [(float)(coord) for coord in item_data[:4]]
                    color = item_data[4]
                    if len(coords) == 4:
                        self.canvas.create_line(coords, fill=color, width=self.brush_size, capstyle=tk.ROUND, smooth=True)


    def clear_drawing(self):
        self.canvas.delete("all")
        self.canvas.config(bg="white")
    
    def process_drawing_single_letter(self):
        treshhold = 15
        if self.result_text_id is not None:
            self.canvas.delete(self.result_text_id)

        # Get the DPI scaling factor
        dpi_scaling = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
        # Adjust the bounding box based on the DPI scaling factor
        bbox = (
            int((self.canvas.winfo_rootx() + treshhold) * dpi_scaling),
            int((self.canvas.winfo_rooty() + treshhold * 2) * dpi_scaling),
            int((self.canvas.winfo_rootx() + self.canvas.winfo_width() - treshhold) * dpi_scaling),
            int((self.canvas.winfo_rooty() + self.canvas.winfo_height() - treshhold) * dpi_scaling)
        )

        # Grab the contents of the canvas as an image
        img = ImageGrab.grab(bbox=bbox)
        img = img.convert('L')
        alphabetRecognition = AlphabetRecognition()
        result = alphabetRecognition.process_image_single_letter(img)
        self.result_text_id = self.canvas.create_text(10, 2, text="result: " + result, font=("Arial", 18), fill="grey", anchor="nw")
    def process_drawing_multiple_letter(self):
        treshhold = 15  
        if self.result_text_id is not None:
            self.canvas.delete(self.result_text_id)
        # grab the contents of the canvas as an image
        # Get the DPI scaling factor
        dpi_scaling = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
        # Adjust the bounding box based on the DPI scaling factor
        bbox = (
            int((self.canvas.winfo_rootx() + treshhold) * dpi_scaling),
            int((self.canvas.winfo_rooty() + treshhold * 2) * dpi_scaling),
            int((self.canvas.winfo_rootx() + self.canvas.winfo_width() - treshhold) * dpi_scaling),
            int((self.canvas.winfo_rooty() + self.canvas.winfo_height() - treshhold) * dpi_scaling)
        )

        # Grab the contents of the canvas as an image
        img = ImageGrab.grab(bbox=bbox)
        img = img.convert('L')
        # img.save("testgray.png")
        # print(img.size, img.mode)
        alphabetRecognition = AlphabetRecognition()
        result = alphabetRecognition.process_image_multiple_letters(img)
        # print the predicted labels
        self.result_text_id = self.canvas.create_text(10, 2, text="result: "+result, font=("Arial", 18),fill= "grey", anchor="nw")
