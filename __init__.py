import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image
from tkinter import HORIZONTAL
from firebase import * 
from detect_object import *

root = tk.Tk()


tomatoAll, imgRoot, imgDetected, totalMass, quantityTomato, details = getInfo()

def update_value_label(event):  # function handle SCALE LABLE
    scale_value_label.configure(text="Current value: {}".format(round(scale.get(), 2)))


def save_coordinates():  # function handle INPUT next to SCALE
    x = float(x_entry.get())
    y = float(y_entry.get())
    coordinates_label.config(text=f"Coordinates: ({x}, {y})")
    
def handle_click_grid(event):
    selected_row = event.widget.grid_info()['row']
    col_1_value = [label.cget('text') for label in event.widget.master.grid_slaves(row=selected_row, column=0)][0]
    print(col_1_value)
    tomatoAll,imgRoot, imgDetected, totalMass, quantityTomato, details = getInfo(col_1_value)

    img_Root = ImageTk.PhotoImage(imgRoot.resize((500, 300), Image.LANCZOS))
    label_img_root.configure(image=img_Root)
    label_img_root.image = img_Root

    img_Detected = ImageTk.PhotoImage(
        imgDetected.resize((500, 300), Image.LANCZOS)
    )
    label_img_detected.config(image=img_Detected)
    label_img_detected.image = img_Detected

    totalMass_label.configure(text=f"Mass Total: {totalMass}kg  ;")
    quantity_label.configure(text=f"Quantity: {quantityTomato} tomatoes")

    for widget in content_frame.winfo_children()[4:]:
        widget.grid_forget()
        
    for widget in content_frame2.winfo_children()[5:]:
        widget.grid_forget()

    for i, x in enumerate(details):
        count = i + 1
        label1 = tk.Label(content_frame, text=f"{count}", padx=20)
        label1.grid(row=count, column=0)
        label2 = tk.Label(content_frame, text=f"{x.class_name}", padx=20)
        label2.grid(row=count, column=1)
        label3 = tk.Label(content_frame, text=f"{x.mass}", padx=20)
        label3.grid(row=count, column=2)
        label4 = tk.Label(content_frame, text=f"{x.conf}", padx=20)
        label4.grid(row=count, column=3)
        canvas.update_idletasks()
    
    count = 0
    for x in tomatoAll.get():
        temp = tomatoAll.get()[x]
        count += 1
        label5 = tk.Label(content_frame2, text=f"{x}",width=10, pady=5, bd=0, bg="#f0f0f0")
        label5.grid(row=count, column=0, sticky="ew")
        label5.bind("<Button-1>", handle_click_grid)
        label6 = tk.Label(content_frame2, text=f"{temp['date']}",width=10)
        label6.grid(row=count, column=1)
        label6.bind("<Button-1>", handle_click_grid)
        label7 = tk.Label(content_frame2, text=f"{temp['time']}",width=10)
        label7.grid(row=count, column=2)
        label7.bind("<Button-1>", handle_click_grid)
        label8 = tk.Label(content_frame2, text=f"{temp['quantity']}",width=10)
        label8.grid(row=count, column=3)
        label8.bind("<Button-1>", handle_click_grid)
        label9 = tk.Label(content_frame2, text=f"{temp['totalMass']}",width=10)
        label9.grid(row=count, column=4)
        label9.bind("<Button-1>", handle_click_grid)
        canvas2.update_idletasks()


# LABEL AND IMAGE ROOT---------------------------------------------------------------------
label_caption_root = tk.Label(root, text=getLastImg(tomatoAll))
label_caption_root.pack()
label_caption_root.place(x=10, y=0)

img_Root = ImageTk.PhotoImage(imgRoot.resize((500, 300), Image.LANCZOS))
label_img_root = tk.Label(root, text="")
label_img_root.configure(image=img_Root)
label_img_root.pack()
label_img_root.place(x=0, y=20, width=500)

# LABEL AND IMAGE RESULT------------------------------------------
label_caption_detected = tk.Label(root, text="Detected Image")
label_caption_detected.pack()
label_caption_detected.place(x=510, y=0)

img_Detected = ImageTk.PhotoImage(imgDetected.resize((500, 300), Image.LANCZOS))
label_img_detected = tk.Label(root, image=img_Detected)
label_img_detected.pack()
label_img_detected.place(x=500, y=20, width=500)

# SCALE AND INPUT COORDINATES --------------------------------------------------------------
scale_input_label = tk.Label(
    root, text="You can choose the coordinates", borderwidth=1, relief="solid"
)
scale_input_label.pack()
scale_input_label.place(x=400, y=330)

# SCALE-----------------------
current_value = tk.DoubleVar()
scale = tk.Scale(
    root,
    from_=0,
    to=100,
    orient=HORIZONTAL,
    command=update_value_label,
    variable=current_value,
)
scale_value_label = tk.Label(root, text="Current value: {}".format(scale.get()))
scale.pack()
scale_value_label.pack()
scale.place(x=100, y=350, width=380)
scale_value_label.place(x=150, y=390)

# INPUT COORDINATES ------------------
x_label = tk.Label(root, text="x:")
x_label.pack()
x_label.place(x=540, y=370)
x_entry = tk.Entry(root)
x_entry.pack()
x_entry.place(x=560, y=370, width=50)

y_label = tk.Label(root, text="y:")
y_label.pack()
y_label.place(x=620, y=370)
y_entry = tk.Entry(root)
y_entry.pack()
y_entry.place(x=640, y=370, width=50)

save_button = tk.Button(root, text="Save", command=save_coordinates)
save_button.pack()
save_button.place(x=700, y=370)
coordinates_label = tk.Label(root, text="Coordinates:")
coordinates_label.pack()
coordinates_label.place(x=750, y=380)

# LABEL of mass total and quantity
totalMass_label = tk.Label(root, text=f"Mass Total: {totalMass}kg  ;  ")
totalMass_label.pack()
totalMass_label.place(x=80, y=440)

quantity_label = tk.Label(root, text=f"Quantity: {quantityTomato} tomatoes")
quantity_label.pack()
quantity_label.place(x=200, y=440)


# GRID thông tin ---------------------------------------------------------------
# Tạo một Frame để chứa Canvas và Scrollbar
canvas_frame = tk.Frame(root)
canvas_frame.place(x=50, y=470)

# Tạo Canvas và Scrollbar
canvas = tk.Canvas(canvas_frame, borderwidth=1, width=320, height=270, relief="solid")
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

scrollbar.config(command=canvas.yview)
canvas.config(yscrollcommand=scrollbar.set)

content_frame = tk.Frame(canvas)
col_1_label = tk.Label(content_frame, text="STT", padx=20, pady=5)
col_1_label.grid(row=0, column=0)
col_2_label = tk.Label(content_frame, text="Type", padx=20)
col_2_label.grid(row=0, column=1)
col_3_label = tk.Label(content_frame, text="Mass", padx=20)
col_3_label.grid(row=0, column=2)
col_4_label = tk.Label(content_frame, text="Conference")
col_4_label.grid(row=0, column=3)

count = 0
for x in details:
    count += 1
    label1 = tk.Label(content_frame, text=f"{count}", padx=20)
    label1.grid(row=count, column=0)
    label2 = tk.Label(content_frame, text=f"{x.class_name}", padx=20)
    label2.grid(row=count, column=1)
    label3 = tk.Label(content_frame, text=f"{x.mass}kg", padx=20)
    label3.grid(row=count, column=2)
    label4 = tk.Label(content_frame, text=f"{x.conf}")
    label4.grid(row=count, column=3)

canvas.create_window((0, 0), window=content_frame, anchor="nw")


# Thiết lập canvas để tự điều chỉnh kích thước khi frame thay đổi
def configure_canvas(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

content_frame.bind("<Configure>", configure_canvas)


# GRID all tomato ---------------------------------------------------------------
# Tạo một Frame để chứa Canvas và Scrollbar
canvas_frame2 = tk.Frame(root)
canvas_frame2.place(x=500, y=470)

# Tạo Canvas và Scrollbar
canvas2 = tk.Canvas(canvas_frame2, borderwidth=1, width=430, height=270, relief="solid")
canvas2.pack(side="left", fill="both", expand=True)

scrollbar2 = tk.Scrollbar(canvas_frame2, orient="vertical", command=canvas2.yview)
scrollbar2.pack(side="right", fill="y")

scrollbar2.config(command=canvas2.yview)
canvas2.config(yscrollcommand=scrollbar2.set)

content_frame2 = tk.Frame(canvas2)
col_1_label = tk.Label(content_frame2, text="STT", pady=5)
col_1_label.grid(row=0, column=0)
col_2_label = tk.Label(content_frame2, text="Date")
col_2_label.grid(row=0, column=1)
col_3_label = tk.Label(content_frame2, text="Time")
col_3_label.grid(row=0, column=2)
col_4_label = tk.Label(content_frame2, text="Quantity")
col_4_label.grid(row=0, column=3)
col_5_label = tk.Label(content_frame2, text="Total Mass")
col_5_label.grid(row=0, column=4)

count = 0
for x in tomatoAll.get():
    temp = tomatoAll.get()[x]
    count += 1
    label5 = tk.Label(content_frame2, text=f"{x}",width=10, pady=5, bd=0, bg="#f0f0f0")
    label5.grid(row=count, column=0, sticky="ew")
    label5.bind("<Button-1>", handle_click_grid)
    label6 = tk.Label(content_frame2, text=f"{temp['date']}",width=10)
    label6.grid(row=count, column=1)
    label6.bind("<Button-1>", handle_click_grid)
    label7 = tk.Label(content_frame2, text=f"{temp['time']}",width=10)
    label7.grid(row=count, column=2)
    label7.bind("<Button-1>", handle_click_grid)
    label8 = tk.Label(content_frame2, text=f"{temp['quantity']}",width=10)
    label8.grid(row=count, column=3)
    label8.bind("<Button-1>", handle_click_grid)
    label9 = tk.Label(content_frame2, text=f"{temp['totalMass']}",width=10)
    label9.grid(row=count, column=4)
    label9.bind("<Button-1>", handle_click_grid)

canvas2.create_window((0, 0), window=content_frame2, anchor="nw")


# Thiết lập canvas để tự điều chỉnh kích thước khi frame thay đổi
def configure_canvas(event):
    canvas2.configure(scrollregion=canvas2.bbox("all"))

content_frame2.bind("<Configure>", configure_canvas)


def refresh_window():
    # code to refresh the window goes here
    device_ref = getRef("device")
    if device_ref.get()["addPic"] == "YES":
        quantit, totalMas, detail = detectAndUpload()
        tomatoAll,imgRoot, imgDetected, totalMass, quantityTomato, details = getInfo()
        # img_name = tomatoAll.key()

        img_Root = ImageTk.PhotoImage(imgRoot.resize((500, 300), Image.LANCZOS))
        label_img_root.configure(image=img_Root)
        label_img_root.image = img_Root

        img_Detected = ImageTk.PhotoImage(
            imgDetected.resize((500, 300), Image.LANCZOS)
        )
        label_img_detected.config(image=img_Detected)
        label_img_detected.image = img_Detected

        totalMass_label.configure(text=f"Mass Total: {totalMass}kg  ;")
        quantity_label.configure(text=f"Quantity: {quantityTomato} tomatoes")

        for widget in content_frame.winfo_children()[4:]:
            widget.grid_forget()
            
        for widget in content_frame2.winfo_children()[5:]:
            widget.grid_forget()

        for i, x in enumerate(details):
            count = i + 1
            label1 = tk.Label(content_frame, text=f"{count}", padx=20)
            label1.grid(row=count, column=0)
            label2 = tk.Label(content_frame, text=f"{x.class_name}", padx=20)
            label2.grid(row=count, column=1)
            label3 = tk.Label(content_frame, text=f"{x.mass}", padx=20)
            label3.grid(row=count, column=2)
            label4 = tk.Label(content_frame, text=f"{x.conf}", padx=20)
            label4.grid(row=count, column=3)
            canvas.update_idletasks()
        
        count = 0
        for x in tomatoAll.get():
            temp = tomatoAll.get()[x]
            count += 1
            label5 = tk.Label(content_frame2, text=f"{x}",width=10, pady=5, bd=0, bg="#f0f0f0")
            label5.grid(row=count, column=0, sticky="ew")
            label5.bind("<Button-1>", handle_click_grid)
            label6 = tk.Label(content_frame2, text=f"{temp['date']}",width=10)
            label6.grid(row=count, column=1)
            label6.bind("<Button-1>", handle_click_grid)
            label7 = tk.Label(content_frame2, text=f"{temp['time']}",width=10)
            label7.grid(row=count, column=2)
            label7.bind("<Button-1>", handle_click_grid)
            label8 = tk.Label(content_frame2, text=f"{temp['quantity']}",width=10)
            label8.grid(row=count, column=3)
            label8.bind("<Button-1>", handle_click_grid)
            label9 = tk.Label(content_frame2, text=f"{temp['totalMass']}",width=10)
            label9.grid(row=count, column=4)
            label9.bind("<Button-1>", handle_click_grid)
            canvas2.update_idletasks()


    root.after(
        1000, refresh_window
    )  # refresh the window after 1000 milliseconds (1 second)


root.after(1000, refresh_window)
root.title("Detect and classify tomatos")
root.geometry("1000x750+200+50")
root.iconbitmap("")  # thay đổi biểu tượng
root.resizable(False, False)  # không cho thay đổi kích thước cửa s
root.mainloop()
