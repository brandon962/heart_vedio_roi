from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import tkinter
import PIL.Image
import PIL.ImageTk
import cv2
import os

now_filename = ""
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
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.draw_flag = False
        self.roi_id = None
        self.file_ptr = 0
        self.playing = 0
        self.init = True
        top_frame = Frame(self.window)
        top_frame.pack(side=LEFT, pady=5)

        right_frame = Frame(self.window)
        right_frame.pack(pady=5)

        bottom_frame = Frame(self.window)
        bottom_frame.pack(side=BOTTOM, pady=5)

        self.pause = False   # Parameter that controls pause button

        self.canvas = Canvas(top_frame)

        self.canvas.bind("<ButtonPress-1>", self.callback)
        self.canvas.bind("<ButtonRelease-1>", self.callback)
        self.canvas.bind('<Motion>', self.myfunction)
        self.canvas.pack()

        self.btn_a2c = Button(right_frame, text="A2C", width=15, command=self.heart_a2c)
        self.btn_a2c.grid(row=0, column=0)
        self.btn_a3c = Button(right_frame, text="A3C", width=15)
        self.btn_a3c.grid(row=1, column=0)

        # Select Button
        # self.btn_select = Button(
        #     bottom_frame, text="Select video file", width=15, command=self.open_file)
        # self.btn_select.grid(row=0, column=0)

        # pre Button
        self.btn_pre = Button(bottom_frame, text='pre',
                              width=15, command=self.pre_file)
        self.btn_pre.grid(row=0, column=0)

        # next Button
        self.btn_next = Button(bottom_frame, text='next',
                               width=15, command=self.next_file)
        self.btn_next.grid(row=0, column=1)

        # Play Button
        self.btn_play = Button(bottom_frame, text="Play",
                               width=15, command=self.play_video)
        self.btn_play.grid(row=1, column=0)
        self.btn_play['state'] = tkinter.DISABLED
        # Pause Button
        self.btn_pause = Button(
            bottom_frame, text="Pause", width=15, command=self.pause_video)
        self.btn_pause.grid(row=1, column=1)

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

    def callback(self, event):
        if str(event.type) == 'ButtonPress':
            print("start at", event.x, event.y)
            self.start_x = event.x
            self.start_y = event.y
            self.draw_flag = True
        elif str(event.type) == 'ButtonRelease':
            print("end at", event.x, event.y)
            print()
            self.draw_flag = False

    def myfunction(self, event):
        if self.draw_flag == True:
            self.end_x = event.x
            self.end_y = event.y
            self.draw_roi()

    def open_file(self):

        self.pause = False

        # self.filename = filedialog.askopenfilename(title="Select file", filetypes=(("AVI files", "*.avi"), ("MP4 files", "*.mp4"),
        #                                                                            ("WMV files", "*.wmv")))
        self.filename = filelist[self.file_ptr]
        # self.file_ptr+=1
        print(self.filename)

        # Open the video file
        self.cap = cv2.VideoCapture(self.filename)

        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.canvas.config(width=self.width, height=self.height)
        # self.btn_play['state'] = tkinter.DISABLED

        # self.play()

    def get_frame(self):   # get only one frame

        try:

            if self.cap.isOpened():
                ret, frame = self.cap.read()
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        except:
            # messagebox.showerror(title='Video file not found', message='Please select a video file.')
            self.cap = cv2.VideoCapture(self.filename)

            self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

            self.canvas.config(width=self.width, height=self.height)
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    def play_video(self):

        # Get a frame from the video source, and go to the next frame automatically
        ret, frame = self.get_frame()
        # self.btn_play['state'] = tkinter.DISABLED
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(
                image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
            self.draw_roi()

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
        self.open_file()

    def write_roi(self, heart_type):
        fp = open("roi\\"+self.filename.split('\\')[-1].split('.')[0]+".txt", "w")
        fp.write(heart_type + "\n")
        fp.write(str(self.start_x)+" "+str(self.start_y) + "\n")
        fp.write(str(self.end_x)+" "+str(self.end_y))
        fp.close()
        self.next_file()
    
    def heart_a2c(self):
        self.write_roi("A2C")

    def heart_a3c(self):
        self.write_roi("A3C")

    def heart_typeA(self):
        self.write_roi("typeA")
    

    # Release the video source when the object is destroyed

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

##### End Class #####


# Create a window and pass it to videoGUI Class
walk(nowPath)
try:
    os.mkdir("roi")
except:
    None
videoGUI(Tk(), "EnJapan")
