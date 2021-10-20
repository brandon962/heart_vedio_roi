from tkinter import *
# import tkMessageBox
import tkinter
 
top = tkinter.Tk()

top_frame = Frame(top, background='#282a36')
top_frame.pack(side=LEFT, pady=5)
CheckVar1 = IntVar()
CheckVar2 = IntVar()
C1 = Checkbutton(top_frame, text = "RUNOOB", variable = CheckVar1, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20)
C2 = Checkbutton(top_frame, text = "GOOGLE", variable = CheckVar2, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20)
# C1.pack()
# C2.pack()
C1.grid(row=0,column=0,padx=0,pady=0)
C2.grid(row=1,column=0,padx=0,pady=0)
top.mainloop()