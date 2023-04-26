import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import HORIZONTAL
from firebase import *
from detect_object import *

root = tk.Tk()
       
imgOri = tomato_ref.get()[getLastImg()]['imgOri']
img_root = decode(imgOri)
imgDetect = tomato_ref.get()[getLastImg()]['imgDetect']
img_detected = decode(imgDetect)


# Define a function to update the value label when the scale changes
def update_value_label(event):
    scale_value_label.configure(text="Current value: {}".format(round(scale.get(), 2)))
    
def save_coordinates():
    x = float(x_entry.get())
    y = float(y_entry.get())
    coordinates_label.config(text=f"Coordinates: ({x}, {y})")    

    
# LABEL AND IMAGE ROOT
label_caption_root = ttk.Label(root, text="Root Image")
label_caption_root.pack()
label_caption_root.place(x=10, y=0)

img_Root = ImageTk.PhotoImage(
    img_root.resize((500, 300), Image.LANCZOS)
)
label_img_root = ttk.Label(root, text='')
label_img_root.configure(image = img_Root)
label_img_root.pack()
label_img_root.place(x=0, y=20, width=500)

# LABEL AND IMAGE RESULT
label_caption_detected = ttk.Label(root, text="Detected Image")
label_caption_detected.pack()
label_caption_detected.place(x=510, y=0)

img_Detected = ImageTk.PhotoImage(
    img_detected.resize((500, 300), Image.LANCZOS)
)
label_img_detected = ttk.Label(root, image=img_Detected)
label_img_detected.pack()
label_img_detected.place(x=500, y=20, width=500)

# SCALE AND INPUT COORDINATES
scale_input_label = ttk.Label(root, text='You can choose the coordinates')
scale_input_label.pack()
scale_input_label.place(x=400, y=340)

# SCALE
current_value = tk.DoubleVar()
scale = ttk.Scale(
    root,
    from_=0,
    to=100,
    orient=HORIZONTAL,
    command=update_value_label,
    variable=current_value,
)
scale_value_label = ttk.Label(root, text="Current value: {}".format(scale.get()))
scale.pack()
scale_value_label.pack()
scale.place(x=100, y=380, width=380)
scale_value_label.place(x=150, y=400)

# INPUT COORDINATES
x_label = tk.Label(root, text="x:")
x_label.pack()
x_label.place(x=540, y=380)
x_entry = tk.Entry(root)
x_entry.pack()
x_entry.place(x=560, y=380,width=50)

y_label = tk.Label(root, text="y:")
y_label.pack()
y_label.place(x=620, y=380)
y_entry = tk.Entry(root)
y_entry.pack()
y_entry.place(x=640, y=380,width=50)

save_button = tk.Button(root, text="Save", command=save_coordinates)
save_button.pack()
save_button.place(x=700, y=375)
coordinates_label = tk.Label(root, text="Coordinates:")
coordinates_label.pack()
coordinates_label.place(x=750, y=380)


def refresh_window():
    # code to refresh the window goes here
    if device_ref.get()['addPic'] == "YES":
        add_img()
    
        imgOri = tomato_ref.get()[getLastImg()]['imgOri']
        img_root = decode(imgOri)
        img_Root = ImageTk.PhotoImage(img_root.resize((500, 300), Image.LANCZOS))
        label_img_root.configure(image=img_Root)
        label_img_root.image = img_Root
        
        imgDetect = tomato_ref.get()[getLastImg()]['imgDetect']
        img_detected = decode(imgDetect)
        img_Detected = ImageTk.PhotoImage(img_detected.resize((500, 300), Image.LANCZOS))
        label_img_detected.config(image=img_Detected)
        label_img_detected.image = img_Detected
        
    root.after(1000, refresh_window) # refresh the window after 1000 milliseconds (1 second)

def on_closing():
    # Unhook all keyboard ev
    # Close the window
    root.destroy()
    print('close')
    listenertomato.close()
    print('a')
    listenerdevice.close()
    print('b')

root.after(1000, refresh_window)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.title("Detect and classify tomatos")
root.geometry("1000x700+200+50")
root.iconbitmap("")  # thay đổi biểu tượng
root.resizable(False, False)  # không cho thay đổi kích thước cửa s
root.mainloop()