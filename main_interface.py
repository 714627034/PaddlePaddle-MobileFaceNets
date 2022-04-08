
import tkinter as tk
import numpy as np
from infer import Predictor
import cv2
import time

class basedesk():
    def __init__(self,master):
        self.root = master
        self.root.config()
        self.root.title('人脸识别')
        self.root.geometry('400x400')
        # l = tk.Label(self.root, text='你好！this is AI', bg='green', font=('Arial', 12), width=30, height=2)
        l = tk.Label(self.root, text='你好！this is AI', bg='green', font=('Arial', 12), width=30, height=2)
        l.pack()
        initface(self.root)

class initface():
    def __init__(self,master):

        self.master = master
        self.master.config(bg='white')
        #基准界面initface
        self.initface = tk.Frame(self.master,)
        self.initface.pack()
        btn = tk.Button(self.initface,text='图片识别',command=self.picture)
        btn.pack()
        atn = tk.Button(self.initface,text='摄像机识别',command=self.video)
        atn.pack()
        db_qt = tk.Button(self.initface,text='数据库',command=self.db)
        db_qt.pack()

    def picture(self,):
        self.initface.destroy()
        face1(self.master)

    def video(self,):
        self.initface.destroy()
        face3(self.master)

    def db(self,):
        self.initface.destroy()
        DB(self.master)

class DB():
    def __init__(self,master):
        self.master = master
        # self.master.config(bg='blue')
        self.DB = tk.Frame(self.master,)
        self.DB.pack()
        db_back = tk.Button(self.DB,text='退出',command=self.back)
        db_back.pack()
    def back(self):
        self.DB.destroy()
        initface(self.master)

class face1():
    def __init__(self,master):
        self.master = master
        # self.master.config(bg='blue')
        self.face1 = tk.Frame(self.master,)
        self.face1.pack()
        self.predictor = Predictor(mtcnn_model_path='models/mtcnn',
                                    mobilefacenet_model_path='models/infer/model',
                                    face_db_path='face_db',
                                    threshold=0.6)
        atn_infer = tk.Button(self.face1,text='预测',command=self.infer)
        atn_infer.pack()
        atn_back = tk.Button(self.face1,text='退出',command=self.back)
        atn_back.pack()
    def infer(self):
        start = time.time()
        boxes, names =self.predictor.recognition('dataset/mimi.jpg')
        print('预测的人脸位置：', boxes.astype(np.int_).tolist())
        print('识别的人脸名称：', names)
        print('总识别时间：%dms' % int((time.time() - start) * 1000))
        # self.predictor.draw_face('dataset/mimi.jpg', boxes, names)
    def back(self):
        self.face1.destroy()
        initface(self.master)


class face2():
    def __init__(self,master):
        self.master = master
        # self.master.config(bg='yellow')
        self.face2 = tk.Frame(self.master,)
        self.face2.pack()
        btn_back = tk.Button(self.face2,text='退出',command=self.back)
        btn_back.pack()

    def back(self):
        self.face2.destroy()
        initface(self.master)


class face3(): ##获取视频，对视频进行甄别。
    def __init__(self,master):
        self.master = master
        # self.master.config(bg='blue')
        self.face3 = tk.Frame(self.master,)
        self.face3.pack()
        self.predictor = Predictor(mtcnn_model_path='models/mtcnn',
                                   mobilefacenet_model_path='models/infer/model',
                                   face_db_path='face_db',
                                   threshold=0.6)
        self.cap = cv2.VideoCapture(0)
        atn_infer = tk.Button(self.face3,text='预测',command=self.infer)
        atn_infer.pack()
        atn_back = tk.Button(self.face3,text='退出',command=self.back)
        atn_back.pack()
    def infer(self):
        start = time.time()
        boxes, names =self.predictor.recognition('dataset/mimi.jpg')
        print('预测的人脸位置：', boxes.astype(np.int_).tolist())
        print('识别的人脸名称：', names)
        print('总识别时间：%dms' % int((time.time() - start) * 1000))
        # self.predictor.draw_face('dataset/mimi.jpg', boxes, names)
    def back(self):
        self.face1.destroy()
        initface(self.master)

if __name__ == '__main__':
    root = tk.Tk()
    basedesk(root)
    root.mainloop()

