from tkinter import *
from tkinter import messagebox
import tkinter
import PIL.Image
import PIL.ImageTk
import cv2
import os

total_filename = []
nowPath = os.getcwd()
filelist = []


def walk(path):
    for item in os.listdir(path):
        subpath = os.path.join(path, item)
        if os.path.isdir(subpath):
            walk(subpath)
        else:
            if subpath.find(".avi") != -1:
                filelist.append(subpath)


class videoGUI:

    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.configure(background='#282a36')
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.draw_flag = False
        self.roi_id = None
        self.file_ptr = 0
        self.init = True
        top_frame = Frame(self.window, background='#282a36')
        top_frame.pack(side=LEFT, pady=5)

        right_frame = Frame(self.window, background='#282a36')
        right_frame.pack(pady=5)

        bottom_frame = Frame(self.window, background='#282a36')
        bottom_frame.pack(side=BOTTOM, pady=5)

        # bottom_frame2 = Frame(self.window, background='#282a36')
        # bottom_frame2.pack(side=BOTTOM, pady=5)

        self.pause = False
        self.canvas = Canvas(
            top_frame, background='#282a36', highlightthickness=0)

        self.canvas.bind("<ButtonPress-1>", self.btn1_func)
        self.canvas.bind("<ButtonRelease-1>", self.btn1_func)
        self.canvas.bind('<Motion>', self.btn1_motion)
        self.canvas.pack()

        # type button
        self.btn_a2c = Button(right_frame, text="A2C",
                              width=15, command=self.heart_a2c, background='#23252f', foreground='white')
        self.btn_a2c.grid(row=0, column=0, padx=10, pady=10)
        self.btn_a3c = Button(right_frame, text="A3C",
                              width=15, command=self.heart_a3c, background='#23252f', foreground='white')
        self.btn_a3c.grid(row=1, column=0, padx=10, pady=10)
        self.btn_tA = Button(right_frame, text="typeA",
                             width=15, command=self.heart_typeA, background='#23252f', foreground='white')
        self.btn_tA.grid(row=2, column=0, padx=10, pady=10)
        self.btn_tB = Button(right_frame, text="typeB",
                             width=15, command=self.heart_typeB, background='#23252f', foreground='white')
        self.btn_tB.grid(row=3, column=0, padx=10, pady=10)
        self.btn_tC = Button(right_frame, text="typeC",
                             width=15, command=self.heart_typeC, background='#23252f', foreground='white')
        self.btn_tC.grid(row=4, column=0, padx=10, pady=10)

        # has done
        self.label_done = Label(bottom_frame, text='Done',
                                width=5, background='#282a36', foreground='white')
        self.label_done.grid(row=0, column=0, padx=5, pady=5)

        # pre Button
        self.btn_pre = Button(bottom_frame, text='pre',
                              width=10, command=self.pre_file, background='#23252f', foreground='white')
        self.btn_pre.grid(row=1, column=0, padx=5, pady=5)

        # next Button
        self.btn_next = Button(bottom_frame, text='next',
                               width=10, command=self.next_file, background='#23252f', foreground='white')
        self.btn_next.grid(row=1, column=1, padx=5, pady=5)

        # Play Button
        self.btn_play = Button(bottom_frame, text="Play",
                               width=10, command=self.play_video, background='#23252f', foreground='white')
        self.btn_play.grid(row=2, column=0, padx=5, pady=5)
        self.btn_play['state'] = tkinter.DISABLED

        # Pause Button
        self.btn_pause = Button(
            bottom_frame, text="Pause", width=10, command=self.pause_video, background='#23252f', foreground='white')
        self.btn_pause.grid(row=2, column=1, padx=5, pady=5)

        self.delay = 15  # ms

        if self.init:
            self.init = False
            self.open_file()
            self.play_video()
        self.window.mainloop()

    def draw_roi(self):
        self.canvas.delete(self.roi_id)
        self.roi_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.end_x, self.end_y, outline="#F00", width=2)

    def btn1_func(self, event):
        if str(event.type) == 'ButtonPress':
            print("start at", event.x, event.y)
            self.start_x = event.x
            self.start_y = event.y
            self.draw_flag = True
        elif str(event.type) == 'ButtonRelease':
            print("end at", event.x, event.y)
            print()
            self.draw_flag = False

    def btn1_motion(self, event):
        if self.draw_flag == True:
            self.end_x = event.x
            self.end_y = event.y
            self.draw_roi()

    def open_file(self):
        self.pause = False
        self.filename = filelist[self.file_ptr]
        print(self.filename)
        self.cap = cv2.VideoCapture(self.filename)
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.canvas.config(
            width=self.width, height=self.height, background='#282a36')

    def get_frame(self):   # get only one frame
        try:
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        # replay the video
        except:
            self.cap = cv2.VideoCapture(self.filename)
            self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            self.canvas.config(width=self.width, height=self.height)
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    def play_video(self):
        ret, frame = self.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(
                image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
            self.draw_roi()

        file_path = str("roi\\"+self.filename.split('\\')
                        [-1].split('.')[0]+".txt")
        if os.path.isfile(file_path):
            fp = open(file_path)
            try:
                type = fp.readline()
                x, y = fp.readline().split(" ")
                x2, y2 = fp.readline().split(" ")
                x = int(x)
                y = int(y)
                x2 = int(x2)
                y2 = int(y2)
                print(type, x, y, x2, y2)
                self.start_x = x
                self.start_y = y
                self.end_x = x2
                self.end_y = y2
                self.label_done.grid()
                if x == 0 and y == 0 and x2 == 0 and y2 == 0:
                    self.label_done.grid_remove()
            except:
                self.label_done.grid_remove()
        else:
            self.label_done.grid_remove()

        if not self.pause:
            self.btn_play['state'] = tkinter.DISABLED
            self.btn_pause['state'] = tkinter.NORMAL
            self.window.after(self.delay, self.play_video)
        else:
            self.pause = False
            self.btn_play['state'] = tkinter.NORMAL
            self.btn_pause['state'] = tkinter.DISABLED

    def pause_video(self):
        self.pause = True

    def next_file(self):
        self.file_ptr += 1
        if self.file_ptr >= len(filelist):
            messagebox.showerror(
                title='Video file not found', message='This is end.')
            self.file_ptr = len(filelist)-1
            return
        self.open_file()

    def pre_file(self):
        self.file_ptr -= 1
        if self.file_ptr < 0:
            messagebox.showerror(
                title='Video file not found', message='This is first.')
            self.file_ptr = 0
            return
        self.start_x=self.start_y=self.end_x=self.end_y=0
        self.open_file()

    def write_roi(self, heart_type):
        fp = open("roi\\"+self.filename.split('\\')
                  [-1].split('.')[0]+".txt", "w")
        fp.write(heart_type + "\n")
        fp.write(str(self.start_x)+" "+str(self.start_y) + "\n")
        fp.write(str(self.end_x)+" "+str(self.end_y))
        fp.close()
        self.start_x=self.start_y=self.end_x=self.end_y=0
        self.next_file()

    def heart_a2c(self):
        self.write_roi("A2C")

    def heart_a3c(self):
        self.write_roi("A3C")

    def heart_typeA(self):
        self.write_roi("typeA")

    def heart_typeB(self):
        self.write_roi("typeB")

    def heart_typeC(self):
        self.write_roi("typeC")

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

##### End Class #####


walk(nowPath)
try:
    os.mkdir("roi")
except:
    None
videoGUI(Tk(), "Heart Roi")
