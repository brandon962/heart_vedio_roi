from tkinter import *

canvas = Canvas(width=200,height=200)
canvas.pack()

rec = canvas.create_rectangle(100,0,200,200,fill="red")#example object

def check_hand(e):#runs on mouse motion
    bbox= canvas.bbox(rec)
    if bbox[0] < e.x and bbox[2] > e.x and bbox[1] < e.y and bbox[3] > e.y:#checks whether the mouse is inside the boundrys
        canvas.config(cursor="hand1")
    else:
        canvas.config(cursor="")

canvas.bind("<Motion>",check_hand)#binding to motion