import cv2
from ultralytics import YOLO
from PIL import Image
import math
import base64
import io

# Load YOLO model
def detect(src):
    model = YOLO('last.pt',"v8") 
    results = model.predict(source = src, save = True, save_txt = True)
    # print(results[0].dirtxt)
    
    return results

class YOLODarknetLabel:
    def __init__(self, class_name, x, y, w, h, c, m):
        self.class_name = class_name
        self.x = float(x)
        self.y = float(y)
        self.w = float(w)
        self.h = float(h)
        self.c = float(c)
        self.m = ''

def read_yolo_darknet_labels_file(file_path):
    labels = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            values = line.strip().split(' ')
            class_name, x, y, w, h, c = values
            label = YOLODarknetLabel(class_name, x, y, w, h, c, '')
            labels.append(label)
    return labels, lines

def mass(dirtxt, dirimg):
    labels, lines = read_yolo_darknet_labels_file(dirtxt)
    
    img = Image.open(dirimg)
    width, height = img.size
    
    total = 0
    P=7/100
    count=1
    for label in labels:
        # print(label.class_name, label.x, label.y, label.w, label.h)
        w = (label.w * width) * P 
        h = (label.h * height) * P
        r=(w+h)/4
        v=(4/3)*3.14*(r*r*r)
        label.m = math.floor(v * 1.05)
        total += label.m
        count += 1
    
    return total, labels, lines    

def encodeImg(path_img):
    with open(path_img, "rb") as image_file:
        image_bytes = image_file.read()
    base64_str = base64.b64encode(image_bytes).decode('utf-8')
    return base64_str

def decode(str):
    image_bytes = base64.b64decode(str)
    image = Image.open(io.BytesIO(image_bytes))
    # image.show()  # Hiển thị ảnh
    return image