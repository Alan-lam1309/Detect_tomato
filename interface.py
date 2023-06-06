import tkinter as tk
from tkinter import ttk
from tkinter import font
from PIL import ImageTk, Image
import firebase as fb
import re

root = tk.Tk()

(
    tomatoAll,
    imgCurrent,
    imgRoot,
    imgDetected,
    totalMass,
    quantityTomato,
    details,
    statusSetting,
    time,
    step,
) = fb.getInfo()


def take_photo():  # function handle INPUT next to SCALE
    device_ref = fb.getRef("device")
    y = x_entry.get().replace(" ", "")
    if y.isdecimal():
        y = int(y) * 10
        if y > 0 and y <= 850:
            device_ref.update({"location": y, "run": 1})


def watering():  # function handle INPUT next to SCALE
    device_ref = fb.getRef("device")
    device_ref.update({"watering": 1})


def set_auto():  # function handle INPUT next to SCALE
    device_ref = fb.getRef("device")
    pattern = r"^\d{1,2}:\d{1,2}$"
    time1 = time1_entry.get().replace(" ", "")
    time2 = time2_entry.get().replace(" ", "")
    time3 = time3_entry.get().replace(" ", "")
    distance = distance_entry.get().replace(" ", "")
    step = step_entry.get().replace(" ", "")

    if time1 != "" and re.match(pattern, time1):
        time1_label.configure(text=f"Time1 ({time1})")
        device_ref.update({"time1": time1})
    if time2 != "" and re.match(pattern, time2):
        time2_label.configure(text=f"Time2 ({time2})")
        device_ref.update({"time2": time2})
    if time3 != "" and re.match(pattern, time3):
        time3_label.configure(text=f"Time3 ({time3})")
        device_ref.update({"time3": time3})
    if distance != "" and step != "":
        valid = int(distance) * int(step)
        if valid < 850:
            distance_label.configure(text=f"Distance ({distance})")
            step_label.configure(text=f"Step ({step})")
            device_ref.update({"distance": distance})
            device_ref.update({"step": step})


def handle_selection(event):  # handle selected of widget combobox
    selected_item = event.widget.get()
    print(selected_item)
    (
        tomatoAll,
        imgCurrent,
        imgRoot,
        imgDetected,
        totalMass,
        quantityTomato,
        details,
        statusSetting,
        time,
        step,
    ) = fb.getInfo(selected_item)
    reloadTK(
        tomatoAll, imgCurrent, imgRoot, imgDetected, totalMass, quantityTomato, details
    )


def reloadTK(
    tomatoAll, imgCurrent, imgRoot, imgDetected, totalMass, quantityTomato, details
):
    # label_caption_root.configure(text=imgCurrent)
    img_Root = ImageTk.PhotoImage(imgRoot.resize((340, 450)))
    label_img_root.configure(image=img_Root)
    label_img_root.image = img_Root

    img_Detected = ImageTk.PhotoImage(imgDetected.resize((340, 450)))
    label_img_detected.config(image=img_Detected)
    label_img_detected.image = img_Detected

    totalMass_label.configure(text=f"Total Quantity: {quantityTomato.total}")
    totalRed_label.configure(
        text=f"Red tomatoes: {quantityTomato.red}",
    )
    totalhalf_label.configure(
        text=f"Hal tomatoes: {quantityTomato.half}",
    )
    totalgreen_label.configure(
        text=f"Green tomatoes: {quantityTomato.green} ",
    )

    for widget in content_frame.winfo_children()[5:]:
        widget.grid_forget()

    combo_box.configure(values=tomatoAll)
    combo_box.set(imgCurrent)

    for i, x in enumerate(details):
        count = i + 1
        label1 = tk.Label(
            content_frame,
            text=f"{count}",
            padx=20,
            font=font.Font(size=20),
            bg="#b3dbf0",
        )
        label1.grid(row=count, column=0)
        label2 = tk.Label(
            content_frame,
            text=f"{x.class_name}",
            padx=20,
            font=font.Font(size=20),
            bg="#b3dbf0",
        )
        label2.grid(row=count, column=1)
        label3 = tk.Label(
            content_frame,
            text=f"{x.mass}",
            padx=20,
            font=font.Font(size=20),
            bg="#b3dbf0",
        )
        label3.grid(row=count, column=2)
        label4 = tk.Label(
            content_frame,
            text=f"{x.conf}",
            padx=20,
            font=font.Font(size=20),
            bg="#b3dbf0",
        )
        label4.grid(row=count, column=3)
        label5 = tk.Label(
            content_frame,
            text=f"{x.harvest}",
            padx=10,
            font=font.Font(size=20),
            bg="#b3dbf0",
        )
        label5.grid(row=count, column=4)
    canvas.update_idletasks()


def on_radio_button_click():
    device_ref = fb.getRef("device")
    selected_option = var.get()
    device_ref.update({"status": selected_option})
    if selected_option == "auto":
        auto_frame.place(x=0, y=150)
        manual_frame.place_forget()
    if selected_option == "manual":
        auto_frame.place_forget()
        manual_frame.place(x=0, y=200)


# LABEL INFORMATION THESIS
image = Image.open("image/logo.png")
img = ImageTk.PhotoImage(image.resize((100, 100), Image.LANCZOS))
label_img_root = tk.Label(root, image=img)
label_img_root.pack()
label_img_root.place(x=100, y=20, width=100)

label_caption_detected = tk.Label(
    root, text="GRADUATION THESIS", font=font.Font(size=28, weight="bold"), fg="#125582"
)
label_caption_detected.pack()
label_caption_detected.place(x=750, y=10)
label_caption_detected = tk.Label(
    root,
    text="Tomato identification and classification system",
    font=font.Font(size=26, weight="bold"),
    fg="#5dafde",
)
label_caption_detected.pack()
label_caption_detected.place(x=550, y=80)

label_caption_detected = tk.Label(
    root, text="Lâm Quốc Phú - 3119411049", font=font.Font(size=16)
)
label_caption_detected.pack()
label_caption_detected.place(x=30, y=150)
label_caption_detected = tk.Label(
    root, text="Huỳnh Gia Hân - 3119411022", font=font.Font(size=16)
)
label_caption_detected.pack()
label_caption_detected.place(x=30, y=190)

# Label
label_caption_detected = tk.Label(
    root, text="History of photo shoots", font=font.Font(size=15)
)
label_caption_detected.pack()
label_caption_detected.place(x=70, y=290)

combo_box = ttk.Combobox(root, values=tomatoAll, font=font.Font(size=16))
combo_box.pack()
combo_box.place(x=70, y=330, width=400)
combo_box.set(imgCurrent)
combo_box.bind("<<ComboboxSelected>>", handle_selection)


# LABEL AND IMAGE ROOT
label_caption_root = tk.Label(root, text="Original Image", font=font.Font(size=18))
label_caption_root.pack()
label_caption_root.place(x=580, y=180)

img_Root = ImageTk.PhotoImage(imgRoot.resize((340, 450), Image.LANCZOS))
label_img_root = tk.Label(root, text="")
label_img_root.configure(image=img_Root)
label_img_root.pack()
label_img_root.place(x=800, y=160, width=340)


# LABEL AND IMAGE RESULT
label_caption_detected = tk.Label(root, text="Detected Image", font=font.Font(size=18))
label_caption_detected.pack()
label_caption_detected.place(x=1250, y=180)

img_Detected = ImageTk.PhotoImage(imgDetected.resize((340, 450), Image.LANCZOS))
label_img_detected = tk.Label(root, image=img_Detected)
label_img_detected.pack()
label_img_detected.place(x=1480, y=160, width=340)

# # SETTINGS

radio_frame = tk.Frame(root, border=2, relief="solid", bg="#b3dbf0")
radio_frame.pack()
radio_frame.place(x=70, y=580, width=500, height=420)

label_setting = tk.Label(root, text="Settings",border=2, relief="solid", font=font.Font(size=15))
label_setting.pack()
label_setting.place(x=90, y=560)

options = ["auto", "manual"]
var = tk.StringVar(value=statusSetting)

rb1 = tk.Radiobutton(
    radio_frame,
    text="Auto",
    variable=var,
    value=options[0],
    font=font.Font(size=20),
    bg="#b3dbf0",
)
rb2 = tk.Radiobutton(
    radio_frame,
    text="Manual",
    variable=var,
    value=options[1],
    font=font.Font(size=20),
    bg="#b3dbf0",
)

rb1.pack()
rb1.place(x=10, y=20)
rb2.pack()
rb2.place(x=10, y=80)

rb1.config(command=on_radio_button_click)
rb2.config(command=on_radio_button_click)

# AUTO SETTING DISPLAY
auto_frame = tk.Frame(radio_frame, width=400, height=250, bg="#b3dbf0")
if statusSetting == "auto":
    auto_frame.pack()
    auto_frame.place(x=0, y=150)

time1_label = tk.Label(
    auto_frame, text=f"Time1 ({time.t1}): ", font=font.Font(size=17), bg="#b3dbf0"
)
time1_label.pack()
time1_label.place(x=0, y=10)

time1_entry = tk.Entry(auto_frame, font=font.Font(size=16))
time1_entry.pack()
time1_entry.place(x=220, y=10, width=70)

time2_label = tk.Label(
    auto_frame, text=f"Time2 ({time.t2}): ", font=font.Font(size=17), bg="#b3dbf0"
)
time2_label.pack()
time2_label.place(x=0, y=60)

time2_entry = tk.Entry(auto_frame, font=font.Font(size=16))
time2_entry.pack()
time2_entry.place(x=220, y=60, width=70)

time3_label = tk.Label(
    auto_frame, text=f"Time3 ({time.t3}): ", font=font.Font(size=17), bg="#b3dbf0"
)
time3_label.pack()
time3_label.place(x=0, y=110)

time3_entry = tk.Entry(auto_frame, font=font.Font(size=16))
time3_entry.pack()
time3_entry.place(x=220, y=110, width=70)

distance_label = tk.Label(
    auto_frame,
    text=f"Distance ({step.distance}): ",
    font=font.Font(size=17),
    bg="#b3dbf0",
)
distance_label.pack()
distance_label.place(x=0, y=160)

distance_entry = tk.Entry(auto_frame, font=font.Font(size=16))
distance_entry.pack()
distance_entry.place(x=220, y=160, width=70)

step_label = tk.Label(
    auto_frame, text=f"Step ({step.step}): ", font=font.Font(size=17), bg="#b3dbf0"
)
step_label.pack()
step_label.place(x=0, y=210)

step_entry = tk.Entry(auto_frame, font=font.Font(size=16))
step_entry.pack()
step_entry.place(x=220, y=210, width=70)

save_button = tk.Button(auto_frame, text="Save", command=set_auto)
save_button.pack()
save_button.place(x=320, y=10)


# MANUAL SETTING DISPLAY
manual_frame = tk.Frame(radio_frame, width=400, height=130, bg="#b3dbf0")
if statusSetting == "manual":
    manual_frame.pack()
    manual_frame.place(x=0, y=150)

x_label = tk.Label(
    manual_frame, text="Location(1-85)cm: ", font=font.Font(size=17), bg="#b3dbf0"
)
x_label.pack()
x_label.place(x=0, y=10)

x_entry = tk.Entry(manual_frame, font=font.Font(size=16))
x_entry.pack()
x_entry.place(x=240, y=10, width=70)

save_button = tk.Button(manual_frame, text="Take Photo", command=take_photo)
save_button.pack()
save_button.place(x=320, y=10)

y_label = tk.Label(
    manual_frame, text="Watering now ", font=font.Font(size=17), bg="#b3dbf0"
)
y_label.pack()
y_label.place(x=0, y=70)

save_button = tk.Button(manual_frame, text="Watering", command=watering)
save_button.pack()
save_button.place(x=210, y=70)


# LABEL of quantity
quantity_frame = tk.Frame(
    root, width=300, height=350, border=2, relief="solid", bg="#b3dbf0"
)
quantity_frame.pack()
quantity_frame.place(x=620, y=650)

label_setting = tk.Label(root, text="Infomation quantity",border=2, relief="solid", font=font.Font(size=15))
label_setting.pack()
label_setting.place(x=640, y=630)

totalMass_label = tk.Label(
    quantity_frame,
    text=f"Total Quantity: {quantityTomato.total} ",
    font=font.Font(size=20, weight="bold"),
    bg="#b3dbf0",
)
totalMass_label.pack()
totalMass_label.place(x=5, y=30)

totalRed_label = tk.Label(
    quantity_frame,
    text=f"Tomatoes Red: {quantityTomato.red}",
    font=font.Font(size=16),
    bg="#b3dbf0",
)
totalhalf_label = tk.Label(
    quantity_frame,
    text=f" Tomatoes Half: {quantityTomato.half}",
    font=font.Font(size=16),
    bg="#b3dbf0",
)
totalgreen_label = tk.Label(
    quantity_frame,
    text=f"Tomatoes Green: {quantityTomato.green}",
    font=font.Font(size=16),
    bg="#b3dbf0",
)
totalRed_label.pack()
totalRed_label.place(x=10, y=100)
totalhalf_label.pack()
totalhalf_label.place(x=10, y=170)
totalgreen_label.pack()
totalgreen_label.place(x=10, y=240)


# TABLE DISPLAY INFO IMAGE DETECTED
canvas_frame = tk.Frame(root, borderwidth=2, relief="solid", bg="#b3dbf0")
canvas_frame.place(x=970, y=650, width=900)

label_setting = tk.Label(root, text="Infomations Detail Image",border=2, relief="solid", font=font.Font(size=15))
label_setting.pack()
label_setting.place(x=1050, y=630)

canvas = tk.Canvas(canvas_frame, width=700, height=340, bg="#b3dbf0")
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

scrollbar.config(command=canvas.yview)
canvas.config(yscrollcommand=scrollbar.set)

content_frame = tk.Frame(canvas, bg="#b3dbf0")
col_1_label = tk.Label(
    content_frame,
    text="Num",
    padx=20,
    pady=10,
    font=font.Font(size=20, weight="bold"),
    bg="#b3dbf0",
)
col_1_label.grid(row=0, column=0)
col_2_label = tk.Label(
    content_frame,
    text="Type",
    padx=20,
    font=font.Font(size=20, weight="bold"),
    bg="#b3dbf0",
)
col_2_label.grid(row=0, column=1)
col_3_label = tk.Label(
    content_frame,
    text="Mass(g)",
    padx=20,
    font=font.Font(size=20, weight="bold"),
    bg="#b3dbf0",
)
col_3_label.grid(row=0, column=2)
col_3_label = tk.Label(
    content_frame,
    text="Conference",
    padx=20,
    font=font.Font(size=20, weight="bold"),
    bg="#b3dbf0",
)
col_3_label.grid(row=0, column=3)
col_4_label = tk.Label(
    content_frame,
    text="Estimate",
    padx=10,
    font=font.Font(size=20, weight="bold"),
    bg="#b3dbf0",
)
col_4_label.grid(row=0, column=4)

count = 0
for x in details:
    count += 1
    label1 = tk.Label(
        content_frame, text=f"{count}", padx=20, font=font.Font(size=20), bg="#b3dbf0"
    )
    label1.grid(row=count, column=0)
    label2 = tk.Label(
        content_frame,
        text=f"{x.class_name}",
        padx=20,
        font=font.Font(size=20),
        bg="#b3dbf0",
    )
    label2.grid(row=count, column=1)
    label3 = tk.Label(
        content_frame, text=f"{x.mass}", padx=20, font=font.Font(size=20), bg="#b3dbf0"
    )
    label3.grid(row=count, column=2)
    label4 = tk.Label(
        content_frame, text=f"{x.conf}", padx=20, font=font.Font(size=20), bg="#b3dbf0"
    )
    label4.grid(row=count, column=3)

    label5 = tk.Label(
        content_frame,
        text=f"{x.harvest}",
        padx=10,
        font=font.Font(size=20),
        bg="#b3dbf0",
    )
    label5.grid(row=count, column=4)

canvas.create_window((0, 0), window=content_frame, anchor="nw")


def configure_canvas(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


content_frame.bind("<Configure>", configure_canvas)


def refresh_window():
    device_ref = fb.getRef("device")
    if device_ref.get()["done"] == 1:
        (
            tomatoAll,
            imgCurrent,
            imgRoot,
            imgDetected,
            totalMass,
            quantityTomato,
            details,
            statusSetting,
            time,
            step,
        ) = fb.getInfo()
        reloadTK(
            tomatoAll,
            imgCurrent,
            imgRoot,
            imgDetected,
            totalMass,
            quantityTomato,
            details,
        )
        device_ref.update({"done": 0})

    root.after(1000, refresh_window)


root.after(1000, refresh_window)
root.title("Detect and classify tomatos")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry("%dx%d+0+0" % (screen_width, screen_height))

root.iconphoto(False, tk.PhotoImage(file="image/logo.png"))  # thay đổi biểu tượng
root.resizable(False, False)  # không cho thay đổi kích thước cửa s
root.mainloop()
