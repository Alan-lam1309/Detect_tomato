import cv2
from ultralytics import YOLO
from PIL import Image
import math
import base64
import io
import numpy as np


# Load YOLO model
def detect(src=""):
    model = YOLO("best.pt", "v8")
    results = model.predict(source=src, save=True, save_txt=True, conf=0.6)
    # print(results[0].dirtxt)
    return results


# detect('a.jpg')


class YOLODarknetLabel:
    def __init__(self, class_name, x, y, w, h, c, m, d):
        self.class_name = class_name
        self.x = float(x)
        self.y = float(y)
        self.w = float(w)
        self.h = float(h)
        self.c = float(c)
        self.m = ""
        self.d = ""


def read_yolo_darknet_labels_file(file_path):
    labels = []
    with open(file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            values = line.strip().split(" ")
            class_name, x, y, w, h, c = values
            label = YOLODarknetLabel(class_name, x, y, w, h, c, "", "")
            labels.append(label)
    return labels, lines


def mass(dirtxt, dirimg):
    labels, lines = read_yolo_darknet_labels_file(dirtxt)

    img = Image.open(dirimg)
    width, height = img.size
    total = 0
    P = 6.3 / 100
    count = 1
    for label in labels:
        # print(label.class_name, label.x, label.y, label.w, label.h)
        w = (label.w * width) * P
        h = (label.h * height) * P
        r = (w + h) / 4
        v = (4 / 3) * 3.14 * (r * r * r)
        label.m = math.floor(v * 1.05)
        total += label.m
        print(f"Trái {count} :" , label.m)
        count += 1

    return total, labels, lines



def harvested(labels):
    mass_average = 40  # g AVG 

    average_growing_time = 20  # days 20-30

    mass_growing_aday = math.floor(mass_average / average_growing_time)  # g

    time_to_ripen = 15  # days 15-20
    degree_of_ripeness = 2 / 5  # red/green 1/3-1/2

    time_to_harvest = time_to_ripen * degree_of_ripeness  # 6days

    level_growing_day = degree_of_ripeness / time_to_harvest # % 2/5 / 6 = 1/15
    count = 1
    for label in labels:
        if label.m < mass_average and int(label.class_name) == 0:
            difference = mass_average - label.m
            estimateDay = (
                math.floor(difference / mass_growing_aday) + 1 + time_to_harvest
            )
            label.d = f"{estimateDay} days left"
        if label.m >= mass_average and int(label.class_name) == 0:
            level = ripeness(label)
            difference = degree_of_ripeness - level
            estimateDay = math.floor(difference / level_growing_day) + 1
            label.d = f"{estimateDay} days left"
        if int(label.class_name) == 1 or int(label.class_name) == 2:
            label.d = f"Harvest"
        print(f'Trái {count} còn: {label.d}')
        count +=1
    return labels

# total, labels, lines = mass('imageOri1.txt','imageOri1.jpg')
# harvested(labels)


def ripeness(label):
    img = cv2.imread("image/r.jpg")
    height, width, c = img.shape
    x_on_image = label.x * width
    y_on_image = label.y * height
    w_on_image = label.w * width
    h_on_image = label.h * height
    x, y, r = (
        math.floor(x_on_image),
        math.floor(y_on_image),
        math.floor((w_on_image + h_on_image) / 4),
    )
    mask = np.zeros_like(img)
    cv2.circle(mask, (x, y), r, (255, 255, 255), -1)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    crop_img = cv2.bitwise_and(img, img, mask=mask)

    img_hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)

    lower_red = (0, 100, 100)
    upper_red = (10, 255, 255)

    lower_orange = (11, 100, 100)
    upper_orange = (20, 255, 255)

    lower_yellow = (21, 100, 100)
    upper_yellow = (30, 255, 255)

    lower_green = (45, 100, 100)
    upper_green = (75, 255, 255)

    mask_red = cv2.inRange(img_hsv, lower_red, upper_red)
    mask_orange = cv2.inRange(img_hsv, lower_orange, upper_orange)
    mask_yellow = cv2.inRange(img_hsv, lower_yellow, upper_yellow)
    mask_green = cv2.inRange(img_hsv, lower_green, upper_green)

    num_red = cv2.countNonZero(mask_red)
    num_orange = cv2.countNonZero(mask_orange)
    num_yellow = cv2.countNonZero(mask_yellow)
    num_green = cv2.countNonZero(mask_green)
    
    ripelevel = int(num_red) + int(num_orange) + int(num_yellow)

    if int(num_green) != 0:
        if (ripelevel) != 0:
            if (ripelevel / int(num_green)) < 2/5:
                level = float(
                    (ripelevel) / int(num_green)
                )
            else:
                level = 2/5
        else:
            level = 0
    else:
        level = 2/5
        
        
    print(level)
    return level


def encodeImg(path_img):
    with open(path_img, "rb") as image_file:
        image_bytes = image_file.read()
    base64_str = base64.b64encode(image_bytes).decode("utf-8")
    return base64_str


def decode(str):
    image_bytes = base64.b64decode(str)
    image = Image.open(io.BytesIO(image_bytes))
    # image.show()  # Hiển thị ảnh
    return image
