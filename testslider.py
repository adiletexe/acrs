import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def update_slider_value(slider, value):
    rounded_value = round(float(value))
    print(f"Slider {slider} Value: {rounded_value}")

# Create main window
root = tk.Tk()
root.title("Slider Application")
root.geometry("1000x1000")
root.resizable(False, False)

# Load and display the image
image = Image.open("acrsimage.JPG")
photo = ImageTk.PhotoImage(image)
label = tk.Label(root, image=photo)
label.image = photo
label.pack(pady=20, padx=20)

# Create sliders as circles, located under each other in a column
slider1 = ttk.Scale(root, from_=0, to=180, orient="horizontal", length=400, command=lambda val: update_slider_value(1, val))
slider1.pack(pady=10)
slider1.place(x=300, y=700)

slider2 = ttk.Scale(root, from_=180, to=0, orient="horizontal", length=400, command=lambda val: update_slider_value(2, val))
slider2.pack(pady=10)
slider2.place(x=300, y=750)

slider3 = ttk.Scale(root, from_=0, to=180, orient="horizontal", length=400, command=lambda val: update_slider_value(3, val))
slider3.pack(pady=10)
slider3.place(x=300, y=800)

# Start the main loop
root.mainloop()
