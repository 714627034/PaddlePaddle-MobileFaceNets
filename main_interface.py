
import tkinter as tk
import tkinter.filedialog
import numpy as np
from infer import Predictor
from infer_camera import Predictor_Video
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
        filePath = tk.filedialog.askopenfilename()
        if len(filePath ) == 0 :
            print("filePath is null")
            return
        start = time.time()
        boxes, names =self.predictor.recognition(filePath)
        print('预测的人脸位置：', boxes.astype(np.int_).tolist())
        print('识别的人脸名称：', names)
        print('总识别时间：%dms' % int((time.time() - start) * 1000))
        img=self.predictor.draw_face(filePath, boxes, names)
        if names[0] != "unknow":
            cv2.imwrite("./dataset/"+names[0]+".jpg",img)
            print("图片已保存在 ./dataset/"+names[0]+".jpg")
        else:
            print("图片识别失败,不予保存")
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


class face3(): ##获取摄像头，对摄像头逐帧进行甄别。
    def __init__(self,master):
        self.master = master
        # self.master.config(bg='blue')
        self.face3 = tk.Frame(self.master,)
        self.face3.pack()
        self.predictor = Predictor_Video(mtcnn_model_path='models/mtcnn',
                                   mobilefacenet_model_path='models/infer/model',
                                   face_db_path='face_db',
                                   threshold=0.6)
        self.cap = cv2.VideoCapture(0)
        atn_infer = tk.Button(self.face3,text='监控预测',command=self.infer)
        atn_infer.pack()
        atn_vi_infer = tk.Button(self.face3,text='视频预测',command=self.v_infer)
        atn_vi_infer.pack()
        atn_back = tk.Button(self.face3,text='退出',command=self.back)
        atn_back.pack()
    def infer(self):
        cap = cv2.VideoCapture(0)
        if cap.isOpened() :
            print("视频正常开启")
        else:
            print("视频开启失败，返回")
            return
        while cap.isOpened():
            ret, img = cap.read() #读取一帧的图片
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if ret:
                start = time.time()
                boxes, names = self.predictor.recognition(img)
                ti= int((time.time() - start) * 1000)
                if boxes is not None:
                    img=self.predictor.draw_face(img, boxes, names)
                    print('预测的人脸位置：', boxes.astype('int32').tolist())
                    print('识别的人脸名称：', names)
                    print('总识别时间：%dms' %ti)
                    # xiangji=False
                cv2.imshow("esc is exit", img)
                if cv2.waitKey(1) & 0xFF == 27:
                    break
        cap.release()
        cv2.destroyAllWindows()
    def v_infer(self):
        filePath = tk.filedialog.askopenfilename()
        if len(filePath ) == 0 :
            print("filePath is null")
            return
        cap = cv2.VideoCapture(filePath)
        if cap.isOpened() :
            print("视频正常开启")
        else:
            print("视频开启失败，返回")
            return
        while cap.isOpened():
            ret, img = cap.read() #读取一帧的图片
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if ret:
                start = time.time()
                boxes, names = self.predictor.recognition(img)
                ti= int((time.time() - start) * 1000)
                if boxes is not None:
                    img=self.predictor.draw_face(img, boxes, names)
                    print('预测的人脸位置：', boxes.astype('int32').tolist())
                    print('识别的人脸名称：', names)
                    print('总识别时间：%dms' %ti)
                    # xiangji=False
                cv2.imshow("esc is exit", img)
                if cv2.waitKey(1) & 0xFF == 27:
                    break
        cap.release()
        cv2.destroyAllWindows()
    def answer(self):
        tk.showerror("Answer", "Sorry, no answer available")
    def back(self):
        self.face3.destroy()
        initface(self.master)

if __name__ == '__main__':
    root = tk.Tk()
    basedesk(root)
    root.mainloop()

