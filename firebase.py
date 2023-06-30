import firebase_admin
from PIL import Image
from firebase_admin import credentials
from firebase_admin import db
import detect_object as do
import connectESP as cnt
import os
import shutil
import datetime


# Fetch the service account key JSON file contents
cred = credentials.Certificate("kltn-ae717-firebase-adminsdk-9zpl2-0567858f5a.json")

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(
    cred, {"databaseURL": "https://kltn-ae717-default-rtdb.firebaseio.com"}
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


class Step:
    def __init__(self, step, distance):
        self.step = step
        self.distance = distance


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

def getHumid():
    device_ref = getRef("device")
    humid = device_ref.get()["humid"]
    result = round((humid-821)/(207-821)*100)
    return result

def findRelatedImg(str="", arr=[]):
    ref_tomato = getRef("tomato")
    id_x = int(str.split("|")[0])
    id_next = id_x + 1
    id_prev = id_x - 1
    time = str[-2:]
    arr_result = []
    if time != "_1":
        while True:
            if id_prev > 0:
                print(time)
                time = arr[id_prev][-2:]
                if time == "L1" or time == "_1":
                    arr_result.append(arr[id_prev])
                    break
                arr_result.append(arr[id_prev])
                id_prev -= 1
            else:
                break
    while True:
        if id_next < len(arr):
            time = arr[id_next][-2:]
            if time == "L1" or time == "_1":
                break
            arr_result.append(arr[id_next])
            id_next += 1
        else:
            break

    print(arr_result)
    return arr_result


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

    name_current = f"{str}"
    imgOri = obj["imgOri"]
    imgDetect = obj["imgDetect"]
    total = obj["totalMass"]

    img_root = do.decode(imgOri)
    img_detected = do.decode(imgDetect)

    details = obj["details"]

    finalDetails = []
    quantityTotal = 0
    if(obj["quantity"] != "Nothings"):
        quantityTotal = int(obj["quantity"])    
    red = 0
    green = 0
    half = 0

    if str[-2:] != "L1":
        arrRel = findRelatedImg(str, sorted_items)
        for id in arrRel:
            objRel = tomatoAll.get()[id]
            detailRel = objRel["details"]
            if objRel["quantity"] != "Nothings":
                quantityTotal += int(objRel["quantity"])
            for x in detailRel:
                if x != None:
                    if x["type"] == "":
                        continue
                    if int(x["type"]) == 2:
                        red += 1
                    if int(x["type"]) == 0:
                        green += 1
                    if int(x["type"]) == 1:
                        half += 1
    for x in details:
        if x != None:
            if x["type"] == "":
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
    quantity = Quantity(quantityTotal, red, green, half)
    time = Time(device.get()["time1"], device.get()["time2"], device.get()["time3"])
    step = Step(device.get()["step"], device.get()["distance"])

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
        step,
    )


def updateInfo(
    option="", imgOri="", imgDetect="", quantity="", totalMass="", details={}
):
    tomato_ref = db.reference(f"tomato")
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
            quantity = "Nothings"
            total = 0

        hour, minute, second, date = getTime()
        stt = getLenTomato(tomato_ref)
        updateInfo(
            f"{stt}|{date}|{hour}:{minute}:{second}|{name}",
            imgOri,
            imgDetect,
            quantity,
            total,
            details,
        )
        shutil.rmtree("runs")
        device_ref = db.reference("device/")
        device_ref.update({"addPic": "NO"})
