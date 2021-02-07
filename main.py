from PIL import Image
import tkinter as tk
from tkinter import filedialog

def select_image():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename()

def shrink_image(img, target_width):
    # Code found at https://stackoverflow.com/questions/273946/how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio
    max_width = target_width
    wpercent = (max_width/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((max_width,hsize), Image.ANTIALIAS)
    return img

def floyd_steinberg(img, img_width, img_height):
    for y in range(img_height):
        for x in range(img_width):
            old_pixel = img[x, y][0]
            new_pixel = (find_closest(old_pixel), 255)
            img[x, y] = new_pixel
            quant_error = old_pixel - new_pixel[0]
            if (x != img_width - 1): img[x + 1, y] = (int(img[x + 1, y][0] + quant_error * 7 / 16), 255)
            if (x != 0 and y != img_height - 1): img[x - 1, y + 1] = (int(img[x - 1, y + 1][0] + quant_error * 3 / 16), 255)
            if (y != img_height - 1): img[x, y + 1] = (int(img[x, y + 1][0] + quant_error * 5 / 16), 255)
            if (x != img_width - 1 and y != img_height - 1): img[x + 1, y + 1] = (int(img[x + 1, y + 1][0] + quant_error * 1 / 16), 255)
    return img

def find_closest(old_pixel):
    palette = [0, 63, 127, 191, 254]
    distance = 99999
    best = 100
    for i in range(len(palette)):
        if abs(old_pixel - palette[i]) < distance:
            distance = abs(palette[i] - old_pixel)
            best = i
    return int(palette[best])

def apply_hue(target_hue, img, img_width, img_height):
    for y in range(img_height):
        for x in range(img_width):
            img[x, y] = (target_hue, 255 - img[x, y][2], img[x, y][2])
    return img

img_count = 0
while True:
    print("Select an image to work with, or cancel to end program.")
    file_path = select_image()
    try:
        img = Image.open(file_path).convert('LA')
    except:
        print("No image selected. Exiting.")
        break
    target_width = int(input("Max width of output image in pixels: "))
    img = shrink_image(img, target_width)
    img_width, img_height = img.size
    img_px = img.load()
    floyd_steinberg(img_px, img_width, img_height)
    target_hue = int(input("Target hue for image: "))
    if not (isinstance(target_hue, int)) or not (0 <= target_hue <= 255):
        print("Bad hue value given, saving image as processed.png.")
        img.save("processed" + str(img_count) + ".png")
        break
    img = img.convert('HSV')
    img_width, img_height = img.size
    img_px = img.load()
    apply_hue(target_hue, img_px, img_width, img_height)
    img = img.convert('RGB')
    img.save("processed" + str(img_count) + ".png")
    img_count += 1