import firebase_admin
import cv2
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


def getLastImg(tomato_ref=''):
    if(tomato_ref==''): tomato_ref = getRef('tomato')
    imgLast = str(list(tomato_ref.get().keys())[-1])
    return imgLast

def getLenTomato(tomato_ref=''):
    if(tomato_ref==''): tomato_ref = getRef('tomato')
    imgLast = len(list(tomato_ref.get().keys()))
    return imgLast


def getInfo(str=""):
    tomatoAll, device = getRef()
    a = tomatoAll.get()
    reversed_dict = reversed(list(a))
    tomatoall = []
    for x in reversed_dict:
        # img_take = a[x]
        tomatoall.append(x)
    if str == "":
        str = getLastImg(tomatoAll)
    obj = tomatoAll.get()[str]
    name_current = f'{str}'
    imgOri = obj["imgOri"]
    imgDetect = obj["imgDetect"]
    total = obj["totalMass"]
    total = int(total) / 1000

    img_root = do.decode(imgOri)
    img_detected = do.decode(imgDetect)

    details = obj["details"]
    finalDetails = []
    red = 0; green=0; half=0
    
    for x in details:
        if x != None:
            if(int(x['type'])==2): red +=1
            if(int(x['type'])==0): green +=1
            if(int(x['type'])==1): half +=1
                
            finalDetail = Details(
                valueTranfer(x["type"]),
                int(x["mass"]),
                x["bbox"],
                x["conf"],
                x["estimateDay"]
            )
            finalDetails.append(finalDetail)
    statusSetting = device.get()["status"]
    quantity = Quantity(obj["quantity"], red, green, half)

    return tomatoall,name_current, img_root, img_detected, total, quantity, finalDetails, statusSetting
    

def updateInfo(option="", imgOri="", imgDetect="", quantity="", totalMass="", details={}):
    tomato_ref = db.reference("tomato/")
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
    return time.hour, time.minute, time.second, formatted_date


def detectAndUpload(name=''):
    tomato_ref, device_ref = getRef()
    if device_ref.get()["addPic"] == "YES":
        cnt.takePhoto()
        result_detect = do.detect('imageOri.jpg')

        path_imgDetect = str(result_detect[0].dirimg).replace("\\", "/")
        path_txt = str(result_detect[0].dirtxt).replace("\\", "/")
        
        hour, minute, second, date = getTime()

        imgOri = do.encodeImg('imageOri.jpg')
        imgDetect = do.encodeImg(path_imgDetect)
        total, labels, lines = do.mass(path_txt, path_imgDetect)
        labels = do.harvested(labels)
        quantity = len(lines)
        count = 0
        details = {}
        for label in labels:
            count += 1
            detail = {
                "bbox": (f"{label.x} {label.y} {label.w} {label.h}"),
                "mass": label.m,
                "type": label.class_name,
                "conf": label.c,
                "estimateDay": label.d
            }
            details[str(count)] = detail
        stt = getLenTomato(tomato_ref)
        updateInfo(f'stt|{date}|{hour}:{minute}:{second}|{name}', imgOri,imgDetect, quantity, total, details)
        device_ref = db.reference("device/")
        device_ref.update({"addPic": "NO"})


def a():
    b = do.encodeImg("r.jpg")
    print(b)
    
