import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkintertable import TableCanvas
from PIL import ImageTk, Image
from tkinter import HORIZONTAL
from tkinter.scrolledtext import ScrolledText
import firebase as fb

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
) = fb.getInfo()


def save_coordinates():  # function handle INPUT next to SCALE
    device_ref = fb.getRef("device")
    y = y_entry.get().replace(" ", "")
    if y.isdecimal():
        y = int(y)
        if y >= 0 and y <= 500:
            device_ref.update({"location": y})


def handle_selection(event):  # handle selected of widget combobox
    selected_item = event.widget.get()
    (
        tomatoAll,
        imgCurrent,
        imgRoot,
        imgDetected,
        totalMass,
        quantityTomato,
        details,
        statusSetting,
    ) = fb.getInfo(selected_item)
    reloadTK(
        tomatoAll, imgCurrent, imgRoot, imgDetected, totalMass, quantityTomato, details
    )


def reloadTK(
    tomatoAll, imgCurrent, imgRoot, imgDetected, totalMass, quantityTomato, details
):
    img_Root = ImageTk.PhotoImage(imgRoot.resize((500, 350)))
    label_img_root.configure(image=img_Root)
    label_img_root.image = img_Root

    img_Detected = ImageTk.PhotoImage(imgDetected.resize((500, 350)))
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
            content_frame, text=f"{count}", padx=20, font=font.Font(size=20)
        )
        label1.grid(row=count, column=0)
        label2 = tk.Label(
            content_frame, text=f"{x.class_name}", padx=20, font=font.Font(size=20)
        )
        label2.grid(row=count, column=1)
        label3 = tk.Label(
            content_frame, text=f"{x.mass}", padx=20, font=font.Font(size=20)
        )
        label3.grid(row=count, column=2)
        label4 = tk.Label(
            content_frame, text=f"{x.conf}", padx=20, font=font.Font(size=20)
        )
        label4.grid(row=count, column=3)
        label5 = tk.Label(
            content_frame, text=f"{x.harvest}", padx=10, font=font.Font(size=20)
        )
        label5.grid(row=count, column=4)
    canvas.update_idletasks()


def on_radio_button_click():
    device_ref = fb.getRef("device")
    selected_option = var.get()
    device_ref.update({"status": selected_option})
    if selected_option == "auto":
        manual_frame.place_forget()
    if selected_option == "manual":
        manual_frame.place(x=0, y=200)


# LABEL INFORMATION THESIS
image = Image.open("R.png")
img = ImageTk.PhotoImage(image.resize((100, 100), Image.LANCZOS))
label_img_root = tk.Label(root, image=img)
label_img_root.pack()
label_img_root.place(x=100, y=20, width=100)

label_caption_detected = tk.Label(
    root, text="GRADUATION THESIS", font=font.Font(size=28, weight="bold")
)
label_caption_detected.pack()
label_caption_detected.place(x=750, y=10)
label_caption_detected = tk.Label(
    root,
    text="Tomato identification and classification system",
    font=font.Font(size=26, weight="bold"),
)
label_caption_detected.pack()
label_caption_detected.place(x=550, y=80)

label_caption_detected = tk.Label(
    root, text="Lâm Quốc Phú - 3119411049", font=font.Font(size=16)
)
label_caption_detected.pack()
label_caption_detected.place(x=100, y=150)
label_caption_detected = tk.Label(
    root, text="Huỳnh Gia Hân - 3119411022", font=font.Font(size=16)
)
label_caption_detected.pack()
label_caption_detected.place(x=100, y=190)

# Label
label_caption_detected = tk.Label(
    root, text="Select the image you want to see ", font=font.Font(size=14)
)
label_caption_detected.pack()
label_caption_detected.place(x=70, y=290)

combo_box = ttk.Combobox(root, values=tomatoAll, font=font.Font(size=16))
combo_box.pack()
combo_box.place(x=70, y=330, width=400)
combo_box.set(imgCurrent)
combo_box.bind("<<ComboboxSelected>>", handle_selection)


# LABEL AND IMAGE ROOT
label_caption_root = tk.Label(root, text=fb.getLastImg(), font=font.Font(size=18))
label_caption_root.pack()
label_caption_root.place(x=600, y=180)

img_Root = ImageTk.PhotoImage(imgRoot.resize((500, 350), Image.LANCZOS))
label_img_root = tk.Label(root, text="")
label_img_root.configure(image=img_Root)
label_img_root.pack()
label_img_root.place(x=500, y=230, width=700)


# LABEL AND IMAGE RESULT
label_caption_detected = tk.Label(root, text="Detected Image", font=font.Font(size=18))
label_caption_detected.pack()
label_caption_detected.place(x=1250, y=180)

img_Detected = ImageTk.PhotoImage(imgDetected.resize((500, 350), Image.LANCZOS))
label_img_detected = tk.Label(root, image=img_Detected)
label_img_detected.pack()
label_img_detected.place(x=1150, y=230, width=700)

# # SETTINGS

radio_frame = tk.Frame(root, border=2, relief="solid")
radio_frame.pack()
radio_frame.place(x=70, y=620, width=500, height=350)

label_setting = tk.Label(root, text="Settings", font=font.Font(size=15))
label_setting.pack()
label_setting.place(x=90, y=600)

options = ["auto", "manual"]
var = tk.StringVar(value=statusSetting)

rb1 = tk.Radiobutton(
    radio_frame, text="Auto", variable=var, value=options[0], font=font.Font(size=20)
)
rb2 = tk.Radiobutton(
    radio_frame, text="Manual", variable=var, value=options[1], font=font.Font(size=20)
)

rb1.pack()
rb1.place(x=10, y=20)
rb2.pack()
rb2.place(x=10, y=80)

rb1.config(command=on_radio_button_click)
rb2.config(command=on_radio_button_click)


# MANUAL SETTING DISPLAY
manual_frame = tk.Frame(radio_frame, width=400, height=50)
if statusSetting == "manual":
    manual_frame.pack()
    manual_frame.place(x=0, y=200)

y_label = tk.Label(manual_frame, text="Location(1-500): ", font=font.Font(size=17))
y_label.pack()
y_label.place(x=0, y=10)

y_entry = tk.Entry(manual_frame, font=font.Font(size=16))
y_entry.pack()
y_entry.place(x=240, y=10, width=70)

save_button = tk.Button(manual_frame, text="Take Photo", command=save_coordinates)
save_button.pack()
save_button.place(x=320, y=10)


# LABEL of quantity
quantity_frame = tk.Frame(root, width=300, height=350, border=2, relief="solid")
quantity_frame.pack()
quantity_frame.place(x=620, y=620)

label_setting = tk.Label(root, text="Infomation quantity", font=font.Font(size=15))
label_setting.pack()
label_setting.place(x=640, y=600)

totalMass_label = tk.Label(
    quantity_frame,
    text=f"Total Quantity: {quantityTomato.total} ",
    font=font.Font(size=20, weight="bold"),
)
totalMass_label.pack()
totalMass_label.place(x=5, y=30)

totalRed_label = tk.Label(
    quantity_frame,
    text=f"Tomatoes Red: {quantityTomato.red}",
    font=font.Font(size=16),
)
totalhalf_label = tk.Label(
    quantity_frame,
    text=f" Tomatoes Half: {quantityTomato.half}",
    font=font.Font(size=16),
)
totalgreen_label = tk.Label(
    quantity_frame,
    text=f"Tomatoes Green: {quantityTomato.green}",
    font=font.Font(size=16),
)
totalRed_label.pack()
totalRed_label.place(x=10, y=100)
totalhalf_label.pack()
totalhalf_label.place(x=10, y=170)
totalgreen_label.pack()
totalgreen_label.place(x=10, y=240)


# TABLE DISPLAY INFO IMAGE DETECTED
canvas_frame = tk.Frame(root, borderwidth=2, relief="solid")
canvas_frame.place(x=970, y=620, width=900)

label_setting = tk.Label(root, text="Infomations Detail Image", font=font.Font(size=15))
label_setting.pack()
label_setting.place(x=1100, y=600)

canvas = tk.Canvas(canvas_frame, width=700, height=340)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

scrollbar.config(command=canvas.yview)
canvas.config(yscrollcommand=scrollbar.set)

content_frame = tk.Frame(canvas)
col_1_label = tk.Label(
    content_frame, text="STT", padx=20, pady=10, font=font.Font(size=20, weight="bold")
)
col_1_label.grid(row=0, column=0)
col_2_label = tk.Label(
    content_frame, text="Type", padx=20, font=font.Font(size=20, weight="bold")
)
col_2_label.grid(row=0, column=1)
col_3_label = tk.Label(
    content_frame, text="Mass(g)", padx=20, font=font.Font(size=20, weight="bold")
)
col_3_label.grid(row=0, column=2)
col_3_label = tk.Label(
    content_frame, text="Conference", padx=20, font=font.Font(size=20, weight="bold")
)
col_3_label.grid(row=0, column=3)
col_4_label = tk.Label(
    content_frame, text="Estimate", padx=10, font=font.Font(size=20, weight="bold")
)
col_4_label.grid(row=0, column=4)

count = 0
for x in details:
    count += 1
    label1 = tk.Label(content_frame, text=f"{count}", padx=20, font=font.Font(size=20))
    label1.grid(row=count, column=0)
    label2 = tk.Label(
        content_frame, text=f"{x.class_name}", padx=20, font=font.Font(size=20)
    )
    label2.grid(row=count, column=1)
    label3 = tk.Label(content_frame, text=f"{x.mass}", padx=20, font=font.Font(size=20))
    label3.grid(row=count, column=2)
    label4 = tk.Label(content_frame, text=f"{x.conf}", padx=20, font=font.Font(size=20))
    label4.grid(row=count, column=3)

    label5 = tk.Label(
        content_frame, text=f"{x.harvest}", padx=10, font=font.Font(size=20)
    )
    label5.grid(row=count, column=4)

canvas.create_window((0, 0), window=content_frame, anchor="nw")


def configure_canvas(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


content_frame.bind("<Configure>", configure_canvas)


def refresh_window():
    device_ref = fb.getRef("device")
    hour, min, sec, date = fb.getTime()
    if device_ref.get()["addPic"] == "YES":
        if device_ref.get()["status"] == "manual":
            fb.detectAndUpload("L1")
            (
                tomatoAll,
                imgCurrent,
                imgRoot,
                imgDetected,
                totalMass,
                quantityTomato,
                details,
                statusSetting,
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
        else:
            count = 0
            i = 0
            while count < 4:
                if device_ref.get()["addPic"] == "YES":
                    count += 1
                    if hour == "9":
                        i = 1
                    if hour == "13":
                        i = 2
                    if hour == "17":
                        i = 3
                    fb.detectAndUpload(f"L{i}_{count}")
                    (
                        tomatoAll,
                        imgCurrent,
                        imgRoot,
                        imgDetected,
                        totalMass,
                        quantityTomato,
                        details,
                        statusSetting,
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

    root.after(2000, refresh_window)


root.after(2000, refresh_window)
root.title("Detect and classify tomatos")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry("%dx%d+0+0" % (screen_width, screen_height))

root.iconbitmap("")  # thay đổi biểu tượng
root.resizable(False, False)  # không cho thay đổi kích thước cửa s
root.mainloop()
