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

humid = fb.getHumid()

def take_photo():  # function handle INPUT next to SCALE
    device_ref = fb.getRef("device")
    y = x_entry.get().replace(" ", "")
    if y.isdecimal():
        y = int(y) * 10
        if y > 0 and y <= 850:
            device_ref.update({"location": y, "run": 1})


def watering():  # function handle INPUT next to SCALE
    device_ref = fb.getRef("device")
    device_ref.update({"watering": int(1)})


def set_auto():  # function handle INPUT next to SCALE
    device_ref = fb.getRef("device")
    pattern = r"^\d{1,2}:\d{1,2}$"
    time1 = time1_entry.get().replace(" ", "")
    time2 = time2_entry.get().replace(" ", "")
    time3 = time3_entry.get().replace(" ", "")
    distance = distance_entry.get().replace(" ", "")
    step = step_entry.get().replace(" ", "")

    if time1 != "" and re.match(pattern, time1) and 0<=int(time1.split(":")[0])<25 and 0<=int(time1.split(":")[1])<59:
        time1_label.configure(text=f"Time1 ({time1})")
        device_ref.update({"time1": time1})
    if time2 != "" and re.match(pattern, time2)and 0<=int(time2.split(":")[0])<25 and 0<=int(time2.split(":")[1])<59:
        time2_label.configure(text=f"Time2 ({time2})")
        device_ref.update({"time2": time2})
    if time3 != "" and re.match(pattern, time3)and 0<=int(time3.split(":")[0])<25 and 0<=int(time3.split(":")[1])<59:
        time3_label.configure(text=f"Time3 ({time3})")
        device_ref.update({"time3": time3})
    if distance != "" and step != "":
        valid = int(distance) * int(step)
        if valid < 850:
            distance_label.configure(text=f"Distance ({distance})")
            step_label.configure(text=f"Step ({step})")
            device_ref.update({"distance": int(distance)})
            device_ref.update({"step": int(step)})


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
    img_Root = ImageTk.PhotoImage(imgRoot.resize((280, 370)))
    label_img_root.configure(image=img_Root)
    label_img_root.image = img_Root

    img_Detected = ImageTk.PhotoImage(imgDetected.resize((280, 370)))
    label_img_detected.config(image=img_Detected)
    label_img_detected.image = img_Detected

    totalMass_label.configure(text=f"Total Quantity: {quantityTomato.total}")
    totalRed_label.configure(
        text=f"Red tomatoes: {quantityTomato.red}",
    )
    totalhalf_label.configure(
        text=f"Half tomatoes: {quantityTomato.half}",
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
            padx=15,
            font=font.Font(size=20),
            bg="#b3dbf0",
        )
        label1.grid(row=count, column=0)
        label2 = tk.Label(
            content_frame,
            text=f"{x.class_name}",
            padx=15,
            font=font.Font(size=20),
            bg="#b3dbf0",
        )
        label2.grid(row=count, column=1)
        label3 = tk.Label(
            content_frame,
            text=f"{x.mass}",
            padx=15,
            font=font.Font(size=20),
            bg="#b3dbf0",
        )
        label3.grid(row=count, column=2)
        label4 = tk.Label(
            content_frame,
            text=f"{x.conf}",
            padx=15,
            font=font.Font(size=20),
            bg="#b3dbf0",
        )
        label4.grid(row=count, column=3)
        label5 = tk.Label(
            content_frame,
            text=f"{x.harvest}",
            padx=15,
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
        auto_frame.place(x=10, y=100)
        manual_frame.place_forget()
    if selected_option == "manual":
        auto_frame.place_forget()
        manual_frame.place(x=10, y=120)


# LABEL INFORMATION PERSONAL
personinfo_frame = tk.Frame(root)
personinfo_frame.pack()
personinfo_frame.place(x=0, y=0, width=400, height=230)
image = Image.open("image/logo.png")
img = ImageTk.PhotoImage(image.resize((100, 100), Image.LANCZOS))
label_img_root = tk.Label(personinfo_frame, image=img)
label_img_root.pack()
label_img_root.place(x=70, y=20, width=100)
label_caption_detected = tk.Label(
    personinfo_frame, text="Lâm Quốc Phú - 3119411049", font=font.Font(size=16)
)
label_caption_detected.pack()
label_caption_detected.place(x=30, y=150)
label_caption_detected = tk.Label(
    personinfo_frame, text="Huỳnh Gia Hân - 3119411022", font=font.Font(size=16)
)
label_caption_detected.pack()
label_caption_detected.place(x=30, y=190)


# LABEL INFO THESIS
thesistitle_frame = tk.Frame(root)
thesistitle_frame.pack()
thesistitle_frame.place(x=400, y=10, width=1000, height=150)
label_caption_detected = tk.Label(
    thesistitle_frame,
    text="GRADUATION THESIS",
    font=font.Font(size=28, weight="bold"),
    fg="#125582",
)
label_caption_detected.pack()
label_caption_detected.place(x=300, y=10)
label_caption_detected = tk.Label(
    thesistitle_frame,
    text="Tomato identification and classification system",
    font=font.Font(size=26, weight="bold"),
    fg="#5dafde",
)
label_caption_detected.pack()
label_caption_detected.place(x=100, y=70)


# Label history
label_caption_detected = tk.Label(
    root, text="History of photo shoots", font=font.Font(size=16)
)
label_caption_detected.pack()
label_caption_detected.place(x=50, y=290)

combo_box = ttk.Combobox(root, values=tomatoAll, font=font.Font(size=16), state='readonly')
combo_box.pack()
combo_box.place(x=50, y=330, width=400)
combo_box.set(imgCurrent)
combo_box.bind("<<ComboboxSelected>>", handle_selection)


# LABEL CAPTION AND IMAGE
cap_img_frame = tk.Frame(root)
cap_img_frame.pack()
cap_img_frame.place(x=520, y=140, width=900, height=370)
label_caption_root = tk.Label(
    cap_img_frame, text="Original Image", font=font.Font(size=16)
)
label_caption_root.pack()
label_caption_root.place(x=0, y=0)

# img_Root = ImageTk.PhotoImage(imgRoot.resize((340, 450), Image.LANCZOS))
img_Root = ImageTk.PhotoImage(imgRoot.resize((280, 370), Image.LANCZOS))
label_img_root = tk.Label(cap_img_frame, text="")
label_img_root.configure(image=img_Root)
label_img_root.pack()
label_img_root.place(x=140, y=0, width=270)

label_caption_detected = tk.Label(
    cap_img_frame, text="Detected Image", font=font.Font(size=16)
)
label_caption_detected.pack()
label_caption_detected.place(x=470, y=0)

img_Detected = ImageTk.PhotoImage(imgDetected.resize((280, 370), Image.LANCZOS))
label_img_detected = tk.Label(cap_img_frame, image=img_Detected)
label_img_detected.pack()
label_img_detected.place(x=625, y=0, width=270)

# SETTINGS
radio_frame = tk.Frame(root, border=2, relief="solid", bg="#b3dbf0")
radio_frame.pack()
radio_frame.place(x=30, y=500, width=430, height=320)

label_setting = tk.Label(
    root, text="Settings", border=2, relief="solid", font=font.Font(size=14)
)
label_setting.pack()
label_setting.place(x=90, y=485)

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
rb1.place(x=10, y=10)
rb2.pack()
rb2.place(x=10, y=50)

rb1.config(command=on_radio_button_click)
rb2.config(command=on_radio_button_click)

# AUTO SETTING DISPLAY
auto_frame = tk.Frame(radio_frame, width=380, height=200, bg="#b3dbf0")
if statusSetting == "auto":
    auto_frame.pack()
    auto_frame.place(x=10, y=100)

time1_label = tk.Label(
    auto_frame, text=f"Time1 ({time.t1}): ", font=font.Font(size=17), bg="#b3dbf0"
)
time1_label.pack()
time1_label.place(x=0, y=10)

time1_entry = tk.Entry(auto_frame, font=font.Font(size=16))
time1_entry.pack()
time1_entry.place(x=180, y=10, width=70)

time2_label = tk.Label(
    auto_frame, text=f"Time2 ({time.t2}): ", font=font.Font(size=17), bg="#b3dbf0"
)
time2_label.pack()
time2_label.place(x=0, y=50)

time2_entry = tk.Entry(auto_frame, font=font.Font(size=16))
time2_entry.pack()
time2_entry.place(x=180, y=50, width=70)

time3_label = tk.Label(
    auto_frame, text=f"Time3 ({time.t3}): ", font=font.Font(size=18), bg="#b3dbf0"
)
time3_label.pack()
time3_label.place(x=0, y=90)

time3_entry = tk.Entry(auto_frame, font=font.Font(size=16))
time3_entry.pack()
time3_entry.place(x=180, y=90, width=70)

distance_label = tk.Label(
    auto_frame,
    text=f"Distance ({step.distance}): ",
    font=font.Font(size=18),
    bg="#b3dbf0",
)
distance_label.pack()
distance_label.place(x=0, y=130)

distance_entry = tk.Entry(auto_frame, font=font.Font(size=18))
distance_entry.pack()
distance_entry.place(x=180, y=130, width=70)

step_label = tk.Label(
    auto_frame, text=f"Step ({step.step}): ", font=font.Font(size=18), bg="#b3dbf0"
)
step_label.pack()
step_label.place(x=0, y=170)

step_entry = tk.Entry(auto_frame, font=font.Font(size=16))
step_entry.pack()
step_entry.place(x=180, y=170, width=70)

save_button = tk.Button(
    auto_frame, text="Save", command=set_auto, font=font.Font(size=13)
)
save_button.pack()
save_button.place(x=280, y=10)


# MANUAL SETTING DISPLAY
manual_frame = tk.Frame(radio_frame, width=400, height=130, bg="#b3dbf0")
if statusSetting == "manual":
    manual_frame.pack()
    manual_frame.place(x=10, y=120)

x_label = tk.Label(
    manual_frame, text="Location(1-85)cm: ", font=font.Font(size=18), bg="#b3dbf0"
)
x_label.pack()
x_label.place(x=0, y=10)

x_entry = tk.Entry(manual_frame, font=font.Font(size=16))
x_entry.pack()
x_entry.place(x=210, y=10, width=70)

save_button = tk.Button(
    manual_frame, text="Take Photo", font=font.Font(size=13), command=take_photo
)
save_button.pack()
save_button.place(x=295, y=8)

y_label = tk.Label(
    manual_frame, text="Watering ({humid}%): ", font=font.Font(size=18), bg="#b3dbf0"
)
y_label.pack()
y_label.place(x=0, y=70)

save_button = tk.Button(
    manual_frame, text="Watering", font=font.Font(size=13), command=watering
)
save_button.pack()
save_button.place(x=210, y=70)


# LABEL of quantity
quantity_frame = tk.Frame(
    root, width=300, height=280, border=2, relief="solid", bg="#b3dbf0"
)
quantity_frame.pack()
quantity_frame.place(x=480, y=540)

label_setting = tk.Label(
    root, text="Infomation quantity", border=2, relief="solid", font=font.Font(size=14)
)
label_setting.pack()
label_setting.place(x=540, y=525)

totalMass_label = tk.Label(
    quantity_frame,
    text=f"Total Quantity: {quantityTomato.total} ",
    font=font.Font(size=18, weight="bold"),
    bg="#b3dbf0",
)
totalMass_label.pack()
totalMass_label.place(x=10, y=30)

totalRed_label = tk.Label(
    quantity_frame,
    text=f"Tomatoes Red: {quantityTomato.red}",
    font=font.Font(size=18),
    bg="#b3dbf0",
)
totalhalf_label = tk.Label(
    quantity_frame,
    text=f"Tomatoes Half: {quantityTomato.half}",
    font=font.Font(size=18),
    bg="#b3dbf0",
)
totalgreen_label = tk.Label(
    quantity_frame,
    text=f"Tomatoes Green: {quantityTomato.green}",
    font=font.Font(size=18),
    bg="#b3dbf0",
)
totalRed_label.pack()
totalRed_label.place(x=10, y=80)
totalhalf_label.pack()
totalhalf_label.place(x=10, y=130)
totalgreen_label.pack()
totalgreen_label.place(x=10, y=180)


# TABLE DISPLAY INFO IMAGE DETECTED
canvas_frame = tk.Frame(root, borderwidth=2, relief="solid", bg="#b3dbf0")
canvas_frame.place(x=800, y=540, width=700, height=280)

label_setting = tk.Label(
    root,
    text="Infomations Detail Image",
    border=2,
    relief="solid",
    font=font.Font(size=14),
)
label_setting.pack()
label_setting.place(x=860, y=525)

canvas = tk.Canvas(canvas_frame, bg="#b3dbf0")
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

scrollbar.config(command=canvas.yview)
canvas.config(yscrollcommand=scrollbar.set)

content_frame = tk.Frame(canvas, bg="#b3dbf0")
col_1_label = tk.Label(
    content_frame,
    text="Num",
    padx=15,
    pady=10,
    font=font.Font(size=18, weight="bold"),
    bg="#b3dbf0",
)
col_1_label.grid(row=0, column=0)
col_2_label = tk.Label(
    content_frame,
    text="Type",
    padx=15,
    font=font.Font(size=18, weight="bold"),
    bg="#b3dbf0",
)
col_2_label.grid(row=0, column=1)
col_3_label = tk.Label(
    content_frame,
    text="Mass(g)",
    padx=15,
    font=font.Font(size=18, weight="bold"),
    bg="#b3dbf0",
)
col_3_label.grid(row=0, column=2)
col_3_label = tk.Label(
    content_frame,
    text="Conference",
    padx=15,
    font=font.Font(size=18, weight="bold"),
    bg="#b3dbf0",
)
col_3_label.grid(row=0, column=3)
col_4_label = tk.Label(
    content_frame,
    text="Estimate",
    padx=15,
    font=font.Font(size=18, weight="bold"),
    bg="#b3dbf0",
)
col_4_label.grid(row=0, column=4)

count = 0
for x in details:
    count += 1
    label1 = tk.Label(
        content_frame, text=f"{count}", padx=15, font=font.Font(size=18), bg="#b3dbf0"
    )
    label1.grid(row=count, column=0)
    label2 = tk.Label(
        content_frame,
        text=f"{x.class_name}",
        padx=15,
        font=font.Font(size=18),
        bg="#b3dbf0",
    )
    label2.grid(row=count, column=1)
    label3 = tk.Label(
        content_frame, text=f"{x.mass}", padx=15, font=font.Font(size=18), bg="#b3dbf0"
    )
    label3.grid(row=count, column=2)
    label4 = tk.Label(
        content_frame, text=f"{x.conf}", padx=15, font=font.Font(size=18), bg="#b3dbf0"
    )
    label4.grid(row=count, column=3)

    label5 = tk.Label(
        content_frame,
        text=f"{x.harvest}",
        padx=15,
        font=font.Font(size=18),
        bg="#b3dbf0",
    )
    label5.grid(row=count, column=4)

canvas.create_window((0, 0), window=content_frame, anchor="nw")


def configure_canvas(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


content_frame.bind("<Configure>", configure_canvas)


def refresh_window():
    device_ref = fb.getRef("device")
    humid = fb.getHumid()
    y_label.configure(text=f"Watering ({humid}%)")
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

    root.after(500, refresh_window)


root.after(500, refresh_window)
root.title("Detect and classify tomatos")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry("%dx%d+0+0" % (screen_width, screen_height))

root.iconphoto(False, tk.PhotoImage(file="image/logo.png"))  # thay đổi biểu tượng
root.resizable(False, False)  # không cho thay đổi kích thước cửa s
root.mainloop()
