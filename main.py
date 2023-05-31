import firebase as fb
import datetime


while True:
    device_ref = fb.getRef("device")
    hour, min, sec, date = fb.getTime()
    time = f"{hour}:{min}"
    if device_ref.get()["runauto"] == 0 and (
        device_ref.get()["time1"] == time
        or device_ref.get()["time2"] == time
        or device_ref.get()["time3"] == time
    ):
        device_ref.update({"runauto": 1})
        print("run auto", time)
    if "7:0" == time :
        device_ref.update({"watering": 1})
        print("watering", time)

    if device_ref.get()["addPic"] == "YES":
        if device_ref.get()["status"] == "manual":
            fb.detectAndUpload("L1")
            print("run man")
            device_ref.update({"done": 1})
        if device_ref.get()["runauto"] == 1:
            count = 0
            i = 0
            time1 = device_ref.get()["time1"]
            time2 = device_ref.get()["time2"]
            time3 = device_ref.get()["time3"]
            while count < 4:
                if device_ref.get()["addPic"] == "YES":
                    count += 1
                    if str(hour) == time1.split(":")[0]:
                        i = 1
                    if str(hour) == time2.split(":")[0]:
                        i = 2
                    if str(hour) == time3.split(":")[0]:
                        i = 3
                    fb.detectAndUpload(f"L{i}_{count}")
            device_ref.update({"done": 1})


# import cv2
# import numpy as np
# import math
# import detect_object as do
# # Load image
# img = cv2.imread("r.jpg")

# labels, lines = do.read_yolo_darknet_labels_file("runs/detect/predict44/labels/r.txt")
# height, width, c = img.shape

# x_on_image = labels[0].x * width
# y_on_image = labels[0].y * height
# w_on_image = labels[0].w * width
# h_on_image = labels[0].h * height

# x, y, r = (
#     math.floor(x_on_image),
#     math.floor(y_on_image),
#     math.floor((w_on_image + h_on_image ) / 4),
# )
# print(x,y,r)

# mask = np.zeros_like(img)
# cv2.circle(mask, (x, y), r, (255, 255, 255), -1)
# mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

# crop_img = cv2.bitwise_and(img, img, mask=mask)

# img_hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)

# lower_red = (0, 100, 100)
# upper_red = (10, 255, 255)

# lower_orange = (11, 100, 100)
# upper_orange = (20, 255, 255)

# lower_yellow = (21, 100, 100)
# upper_yellow = (30, 255, 255)

# lower_green = (45, 100, 100)
# upper_green = (75, 255, 255)

# mask_red = cv2.inRange(img_hsv, lower_red, upper_red)
# mask_orange = cv2.inRange(img_hsv, lower_orange, upper_orange)
# mask_yellow = cv2.inRange(img_hsv, lower_yellow, upper_yellow)
# mask_green = cv2.inRange(img_hsv, lower_green, upper_green)

# num_red = cv2.countNonZero(mask_red)
# num_orange = cv2.countNonZero(mask_orange)
# num_yellow = cv2.countNonZero(mask_yellow)
# num_green = cv2.countNonZero(mask_green)

# print("Số lượng pixel màu đỏ: ", num_red)
# print("Số lượng pixel màu cam: ", num_orange)
# print("Số lượng pixel màu vàng: ", num_yellow)
# print("Số lượng pixel màu xanh: ", num_green)

# cv2.imshow("Cropped Image", crop_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
