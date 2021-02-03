from PIL import Image
import tkinter as tk
from tkinter import filedialog

def select_image():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename()

def render_to_one_bit(img):
    return img

while True:

    print("Select an image to work with, or cancel to end program.")
    file_path = select_image()
    try:
        img = Image.open(file_path).convert('LA')
    except:
        print("No image selected. Exiting.")
        break
    img_width, img_height = img.size
    