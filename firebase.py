import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from detect_object import *

# Fetch the service account key JSON file contents
cred = credentials.Certificate("detect-tomato-firebase-adminsdk-dkmtc-9d94023d4e.json")

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(
    cred, {"databaseURL": "https://detect-tomato-default-rtdb.firebaseio.com"}
)


class Details:
    def __init__(self, class_name, mass, bbox, conf):
        self.class_name = class_name
        self.mass = float(mass)
        self.bbox = bbox
        self.conf = float(conf)


# As an admin, the app has access to read and write all data, regradless of Security Rules
def getRef(str=''):
    tomato_ref = db.reference("tomato/")
    device_ref = db.reference("device/")
    if str == "tomato":
        return tomato_ref
    if str == "device":
        return device_ref
    return tomato_ref, device_ref

def valueTranfer(x):
    x= int(x)
    if(x == 0):
        x='Red'
        return x
    if(x == 1):
        x='Green'
        return x
    if(x==2):
        x='HalfRed'
        return x    

def getLastImg(tomato_ref):
    imgLast = str(list(tomato_ref.get().keys())[-1])
    return imgLast


def getInfoInit():
    tomato_ref = getRef("tomato")
    obj = tomato_ref.get()[getLastImg(tomato_ref)]

    imgOri = obj["imgOri"]
    imgDetect = obj["imgDetect"]
    total = obj["totalMass"]
    quantity = obj["quantity"]

    img_root = decode(imgOri)
    img_detected = decode(imgDetect)

    details = obj["details"]
    finalDetails = []
    for x in details:
        if(x!= None):
            finalDetail = Details(
                valueTranfer(x["type"]),
                x["mass"],
                x["bbox"],
                x["conf"],
            )
            finalDetails.append(finalDetail)
    return img_root, img_detected, total, quantity, finalDetails



def updateInfo(option="", imgDetect="", quantity="", totalMass="", details={}):
    tomato_ref = db.reference("tomato/")
    child_ref = tomato_ref.child(option)
    child_ref.update(
        {
            "imgDetect": imgDetect,
            "quantity": quantity,
            "totalMass": totalMass,
            "details": details,
        }
    )


def detectAndUpload():
    tomato_ref, device_ref = getRef()
    if device_ref.get()["addPic"] == "YES":
        imgAdded = tomato_ref.get()[getLastImg(tomato_ref)]["imgOri"]
        imgAdded = decode(imgAdded)
        imgAdded.save("imgOri.jpg")
        result_detect = detect("imgOri.jpg")

        path_imgDetect = str(result_detect[0].dirimg).replace("\\", "/")
        path_txt = str(result_detect[0].dirtxt).replace("\\", "/")

        imgDetect = encodeImg(path_imgDetect)
        total, labels, lines = mass(path_txt, path_imgDetect)
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
            }
            details[str(count)] = detail

        updateInfo(getLastImg(tomato_ref), imgDetect, quantity, total, details)
        device_ref.update({"addPic": "NO"})
        return quantity, total, labels


def a():
    b = encodeImg("g.jpg")
    print(b)
