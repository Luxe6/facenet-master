from tkinter.messagebox import showinfo

import face
import cv2
import time
import argparse
import _thread
import threading
import sys
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

global i
i = 0

li = []

class Class:
    def __init__(self):
        self.id = None
        self.name = None
        self.num = None
        self.checktime = None
        self.flag = 0

def refreshText():
    global i
    i += 1
    text1.delete(0.0, tk.END)
    text1.insert(tk.INSERT, time.asctime(time.localtime(time.time())))
    text1.update()
    root.after(1000, refreshText)

def refreshListb():
    global i
    i += 1
    if class1[0].flag == 1:
        # li.append(Class.name)
        # li.append(Class.num)
        # li.append(Class.checktime)
        #li.append(i)
        li.append(class1[0].name)
        li.append(class1[0].num)
        li.append(class1[0].checktime)
        for item in li:
            listb.insert(0, item)
    else:
        #li.append(i)
        None

    listb.delete(0, tk.END)
    listb.insert(tk.END, li)
    listb.update()
    li.clear()
    root.after(1000, refreshListb)

def print_info():
    def refresh_data():
        listb.delete(0, "end")
        listb.insert("end", li)
        listb.update()
        window.after(1000, refresh_data())

    window = Tk()
    window.geometry('320x240')
    window.update()
    class1 = add_class()
    listb = Listbox(window)
    li = []
    if class1[0].flag == 1:
        # li.append(Class.name)
        # li.append(Class.num)
        # li.append(Class.checktime)
        li.append(class1[0].name)
        li.append(class1[0].num)
        li.append(class1[0].checktime)
        for item in li:
            listb.insert(0, item)
    else:
        None
    listb.pack(fill=BOTH, expand=YES)
    window.after(100, refresh_data())
    window.mainloop()


def add_class():
    class1 = []
    class1.append(Class())
    class1[0].id = 'chen'
    class1[0].name = '陈星羽'
    class1[0].num = '20203202304'
    class1[0].checktime = time.asctime(time.localtime(time.time()))
    class1[0].flag = 0
    return class1


def add_overlays(frame, faces, frame_rate):
    if faces is not None:
        for face in faces:
            face_bb = face.bounding_box.astype(int)
            cv2.rectangle(frame,
                          (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]),
                          (0, 255, 0), 2)
            if face.name is not None:
                cv2.putText(frame, face.name, (face_bb[0], face_bb[3]),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                            thickness=2, lineType=2)

    cv2.putText(frame, str(frame_rate) + " fps", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                thickness=2, lineType=2)


def facecheck(args):
    frame_interval = 3  # Number of frames after which to run face detection
    fps_display_interval = 5  # seconds
    frame_rate = 0
    frame_count = 0

    video_capture = cv2.VideoCapture(0)
    face_recognition = face.Recognition()
    start_time = time.time()

    if args.debug:
        print("Debug enabled")
        face.debug = True

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        if (frame_count % frame_interval) == 0:
            faces = face_recognition.identify(frame)

            # Check our current fps
            end_time = time.time()
            if (end_time - start_time) > fps_display_interval:
                frame_rate = int(frame_count / (end_time - start_time))
                start_time = time.time()
                frame_count = 0

        add_overlays(frame, faces, frame_rate)

        frame_count += 1
        cv2.imshow('Video', frame)

        if len(faces) == 1:
            facetemp = faces[0]
            for i in class1:
                if facetemp.name == i.id and i.flag == 0:
                    print(i.name)
                    print(i.num)
                    print(i.checktime)
                    print('打卡成功')
                    # print(facetemp.name)
                    # time.sleep(100)
                    # gui(i)
                    i.flag = 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()


def parse_arguments(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('--debug', action='store_true',
                        help='Enable some debug outputs.')
    return parser.parse_args(argv)


if __name__ == '__main__':
    # facecheck(parse_arguments(sys.argv[1:]))
    root = Tk()
    root.geometry('640x480')
    class1 = add_class()
    Button1 = Button(root, text="人脸识别", command=lambda: facecheck(parse_arguments(sys.argv[1:])))
    #Button2 = Button(root, text="打卡信息", command=lambda: print_info())

    #Button2.pack()
    listb = Listbox(root)
    text1 = Text(root, width=25, height=1)
    text1.pack()
    listb.pack(fill=BOTH, expand=YES)
    Button1.pack()
    root.after(1000, refreshText)
    root.after(1000, refreshListb)
    root.mainloop()
