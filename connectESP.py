import cv2

# import numpy as np

import requests

# import time
# ESP32 URL
URL = "http://192.168.1.5"
AWB = True
def takePhoto():
    cap = cv2.VideoCapture(URL + ":81/stream")
    if cap.isOpened():
        ret, frame = cap.read()
        cv2.imwrite("imageOri.jpg", frame)


# takePhoto()
