import firebase_admin
from PIL import Image
from firebase_admin import credentials
from firebase_admin import db
import detect_object as do
import connectESP as cnt
import os
import datetime


# Fetch the service account key JSON file contents
cred = credentials.Certificate("detect-tomato-firebase-adminsdk-dkmtc-9d94023d4e.json")

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(
    cred, {"databaseURL": "https://detect-tomato-default-rtdb.firebaseio.com"}
)


def getRef(str=""):
    tomato_ref = db.reference("tomato/")
    device_ref = db.reference("device/")
    if str == "tomato":
        return tomato_ref
    if str == "device":
        return device_ref
    return tomato_ref, device_ref


class Details:
    def __init__(self, class_name, mass, bbox, conf, harvest):
        self.class_name = class_name
        self.mass = float(mass)
        self.bbox = bbox
        self.conf = float(conf)
        self.harvest = harvest


class Quantity:
    def __init__(self, total, red, green, half):
        self.total = total
        self.red = red
        self.green = green
        self.half = half


class Time:
    def __init__(self, t1, t2, t3):
        self.t1 = t1
        self.t2 = t2
        self.t3 = t3


# As an admin, the app has access to read and write all data, regradless of Security Rules
def getRef(str=""):
    tomato_ref = db.reference("tomato/")
    device_ref = db.reference("device/")
    if str == "tomato":
        return tomato_ref
    if str == "device":
        return device_ref
    return tomato_ref, device_ref


def valueTranfer(x):
    x = int(x)
    if x == 0:
        x = "Green"
        return x
    if x == 1:
        x = "Half Red"
        return x
    if x == 2:
        x = "Red"
        return x


def getLastImg(tomato_ref=""):
    if tomato_ref == "":
        tomato_ref = getRef("tomato")
    items = list(tomato_ref.get().keys())
    sorted_items = sorted(items, key=lambda x: int(x.split("|")[0]))
    return sorted_items[-1]


def getLenTomato(tomato_ref=""):
    if tomato_ref == "":
        tomato_ref = getRef("tomato")
    imgLast = len(list(tomato_ref.get().keys()))
    return imgLast


def getInfo(str=""):
    tomatoAll, device = getRef()
    items = tomatoAll.get()
    sorted_items = sorted(items, key=lambda x: int(x.split("|")[0]))
    reversed_dict = reversed(list(sorted_items))
    tomatoall = []
    for x in reversed_dict:
        tomatoall.append(x)
    if str == "":
        str = getLastImg(tomatoAll)
    obj = tomatoAll.get()[str]
    print(obj)
    name_current = f"{str}"
    imgOri = obj["imgOri"]
    imgDetect = obj["imgDetect"]
    total = obj["totalMass"]
    total = int(total)

    img_root = do.decode(imgOri)
    img_detected = do.decode(imgDetect)

    details = obj["details"]
    finalDetails = []
    red = 0
    green = 0
    half = 0

    for x in details:
        if x != None:
            if(x["type"] == ''):
                break
            if int(x["type"]) == 2:
                red += 1
            if int(x["type"]) == 0:
                green += 1
            if int(x["type"]) == 1:
                half += 1

            finalDetail = Details(
                valueTranfer(x["type"]),
                int(x["mass"]),
                x["bbox"],
                x["conf"],
                x["estimateDay"],
            )
            finalDetails.append(finalDetail)
    statusSetting = device.get()["status"]
    quantity = Quantity(obj["quantity"], red, green, half)
    time = Time(device.get()["time1"], device.get()["time2"], device.get()["time3"])

    return (
        tomatoall,
        name_current,
        img_root,
        img_detected,
        total,
        quantity,
        finalDetails,
        statusSetting,
        time,
    )


def updateInfo(
    option="", imgOri="", imgDetect="", quantity="", totalMass="", details={}
):
    stt = getLenTomato()
    tomato_ref = db.reference(f"tomato/{stt}")
    child_ref = tomato_ref.child(option)
    child_ref.update(
        {
            "imgOri": imgOri,
            "imgDetect": imgDetect,
            "quantity": quantity,
            "totalMass": totalMass,
            "details": details,
        }
    )


def getTime():
    date = datetime.date.today()
    # Định dạng ngày tháng năm
    formatted_date = date.strftime("%d-%m-%Y")
    time = datetime.datetime.now()
    return int(time.hour), int(time.minute), int(time.second), formatted_date


def rotateImg(path="imageOri.jpg"):
    image_path = path
    image = Image.open(image_path)
    rotated_image = image.transpose(Image.ROTATE_90)  # xoay 90 độ ngược kim đồng hồ
    rotated_image.save("imageOri.jpg")


# rotateImg()


def detectAndUpload(name=""):
    tomato_ref, device_ref = getRef()
    if device_ref.get()["addPic"] == "YES":
        cnt.takePhoto()
        rotateImg("imageOri.jpg")
        result_detect = do.detect("imageOri.jpg")
        path_imgDetect = str(result_detect[0].dirimg).replace("\\", "/")
        imgDetect = do.encodeImg(path_imgDetect)
        imgOri = do.encodeImg("imageOri.jpg")
        details = {}
        if os.path.exists(result_detect[0].dirtxt):
            path_txt = str(result_detect[0].dirtxt).replace("\\", "/")
            total, labels, lines = do.mass(path_txt, path_imgDetect)
            labels = do.harvested(labels)
            quantity = len(lines)
            count = 0
            for label in labels:
                count += 1
                detail = {
                    "bbox": (f"{label.x} {label.y} {label.w} {label.h}"),
                    "mass": label.m,
                    "type": label.class_name,
                    "conf": label.c,
                    "estimateDay": label.d,
                }
                details[str(count)] = detail
        else:
            detail = {
                "bbox": "",
                "mass": "",
                "type": "",
                "conf": "",
                "estimateDay": "",
            }
            details["1"] = detail

        hour, minute, second, date = getTime()

        # stt = getLenTomato(tomato_ref)
        updateInfo(
            f"{date}|{hour}:{minute}:{second}|{name}",
            imgOri,
            imgDetect,
            quantity,
            total,
            details,
        )
        device_ref = db.reference("device/")
        device_ref.update({"addPic": "NO"})


def a():
    b = do.encodeImg("r.jpg")
    print(b)
