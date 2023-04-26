import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from tkinter import HORIZONTAL
from firebase import *

index = 0
def changeColor():
    b = Image.open('images.jpg')
    imageRoot2 = ImageTk.PhotoImage(b)
    print(imageRoot2)
    global index
    if index%2==0:
        label.config(image=imageRoot1)
    else:
        label.config(image=imageRoot2)
        label.image = imageRoot2
    index+=1
    label.after(1000, changeColor)

root = Tk()
label = Label(root, text="")
a = Image.open('R.jpg')

imageRoot1 = ImageTk.PhotoImage(a)
print(imageRoot1)

label.configure(image=imageRoot1)
label.pack(side=LEFT, ipadx=5, ipady=5)
label.pack()
label.after(1000, changeColor)
root.title("Timed event")
root.mainloop()