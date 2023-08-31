import face
import cv2
import time
import argparse
import _thread
import threading
import sys
from tkinter import *
from PIL import Image, ImageTk


class Class:
    def __init__(self):
        self.id = None
        self.name = None
        self.num = None
        self.checktime = None
        self.flag = 0

def take_snapshot():
    print("有人给你点赞啦！")

def video_loop():
    success, img = camera.read()  # 从摄像头读取照片
    if success:
        cv2.waitKey(100)
        cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)#转换颜色从BGR到RGBA
        current_image = Image.fromarray(cv2image)#将图像转换成Image对象
        imgtk = ImageTk.PhotoImage(image=current_image)
        panel.imgtk = imgtk
        panel.config(image=imgtk)
        root.after(1, video_loop)

def gui():
    root = Tk()
    root.geometry('180x100')
    class1 = add_class()
    li = []
    # li.append(Class.name)
    # li.append(Class.num)
    # li.append(Class.checktime)
    li.append(class1[0].name)
    li.append(class1[0].num)
    li.append(class1[0].checktime)
    listb = Listbox(root)
    for item in li:
        listb.insert(0, item)
    listb.pack(fill=BOTH, expand=YES)
    root.mainloop()


def add_class():
    class1 = []
    class1.append(Class())
    class1[0].id = 'chen'
    class1[0].name = '陈星羽'
    class1[0].num = '20203202304'
    class1[0].checktime = time.asctime(time.localtime(time.time()))

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

    flag = 0

    class1 = add_class()

    if args.debug:
        print("Debug enabled")
        face.debug = True

    # gui()

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
    #cv2.imshow('Video', frame)

    root = Tk()
    root.title("opencv + tkinter")
    # root.protocol('WM_DELETE_WINDOW', detector)

    panel = Label(root)  # initialize image panel
    panel.pack(padx=10, pady=10)
    root.config(cursor="arrow")
    btn = Button(root, text="点赞!", command=take_snapshot)
    btn.pack(fill="both", expand=True, padx=10, pady=10)

    video_loop(ret,frame)

    root.mainloop()

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()


def parse_arguments(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('--debug', action='store_true',
                        help='Enable some debug outputs.')
    return parser.parse_args(argv)


if __name__ == '__main__':
    facecheck(parse_arguments(sys.argv[1:]))

    camera = cv2.VideoCapture(0)  # 摄像头

    root = Tk()
    root.title("opencv + tkinter")
    # root.protocol('WM_DELETE_WINDOW', detector)

    panel = Label(root)  # initialize image panel
    panel.pack(padx=10, pady=10)
    root.config(cursor="arrow")
    btn = Button(root, text="点赞!", command=take_snapshot)
    btn.pack(fill="both", expand=True, padx=10, pady=10)

    video_loop()

    root.mainloop()

    # When everything is done, release the capture
    camera.release()
    cv2.destroyAllWindows()
