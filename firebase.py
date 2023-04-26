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

# As an admin, the app has access to read and write all data, regradless of Security Rules
tomato_ref = db.reference("tomato/")
device_ref = db.reference("device/")
# Lắng nghe các sự kiện cập nhật giá trị trên Firebase
def on_update(event):
    event.data # Giá trị mới nhất của node device

listenertomato = tomato_ref.listen(on_update)
listenerdevice = device_ref.listen(on_update) # Bắt đầu lắng nghe các sự kiện

def getLastImg():
    imgLast = str(list(tomato_ref.get().keys())[-1])
    return imgLast
        
def updateInfo(option='', imgDetect='', quantity='', totalMass='', details={}):
    
    tomato_ref = db.reference("tomato/")
    child_ref = tomato_ref.child(option)
    child_ref.update ({
        'imgDetect': imgDetect,
        'quantity': quantity,
        'totalMass': totalMass,
        'details': details
    })
    
def add_img():
    if device_ref.get()['addPic'] == "YES":
        imgAdded = tomato_ref.get()[getLastImg()]['imgOri']
        imgAdded = decode(imgAdded)
        imgAdded.save("imgOri.jpg")
        result_detect = detect('imgOri.jpg')
        
        path_imgDetect = str(result_detect[0].dirimg).replace('\\', '/')
        path_txt = str(result_detect[0].dirtxt).replace('\\', '/')

        imgDetect = encodeImg(path_imgDetect)
        total, labels, lines = mass(path_txt, path_imgDetect)
        quantity = len(lines)
        count = 0
        details = {}
        for label in labels:
            count += 1
            detail = {
                'bbox': (f'{label.x} {label.y} {label.w} {label.h}'),
                'mass': label.m,
                'type': label.class_name,
                'conf': label.c
            }
            details[str(count)] = detail
        
        updateInfo(getLastImg(),imgDetect, quantity, total, details)
        device_ref.update({
            'addPic':'NO'
        })
      
def a():
    b=encodeImg('g.jpg')
    print(b)
    
a()
