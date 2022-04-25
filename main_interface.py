# from tkinter import*
import tkinter as tk
import tkinter.filedialog
import numpy as np
from infer import Predictor
from infer_camera import Predictor_Video
import cv2
import time

class land():
    def __init__(self,master):
        self.root = master
        self.root.config()
        self.root.title('人脸识别系统登陆')
        # self.root.geometry('600x400')
        width=800
        height=302
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)
        photo=tkinter.PhotoImage(file="dataset/caozuo.gif")
        # l = tk.Label(self.root, text='你好！this is AI', bg='green', font=('Arial', 12), width=30, height=2)
        tk.Label(self.root, text='你好！欢迎使用人脸识别系统。请确认您的身份',font=('Arial', 12)).place(relx=0.3,rely=0.08)
    # tk.Label(self.root, text='你好！欢迎使用人脸识别系统。请确认您的身份', image=photo,compound='center',font=('Arial', 12)).place(relx=0.3,rely=0.08)
        initface(self.root)

class basedesk():
    def __init__(self,master):
        self.root = master
        self.root.config()
        self.root.title('人脸识别')
        # self.root.geometry('600x400')
        width=800
        height=302
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
        self.root.geometry(alignstr)
        # self.root.resizable(width=False, height=False)
        # l = tk.Label(self.root, text='你好！this is AI', bg='green', font=('Arial', 12), width=30, height=2)
        tk.Label(self.root, text='你好！欢迎使用人脸识别系统。请选择功能',bg='lightskyblue', fg='white', font=('Arial', 12)).place(relx=0.35,rely=0.08)
        initface(self.root)

class initface():
    def __init__(self,master):

        self.master = master
        # self.master.config(bg='white')
        #基准界面initface
        self.initface = tk.Frame(self.master,)
        self.initface.place(relx=0.4,rely=0.55)
        btn = tk.Button(self.initface,text='图片类人脸识别',command=self.picture)
        btn.pack()
        atn = tk.Button(self.initface,text='视频类人脸识别',command=self.video)
        atn.pack()
        db_qt = tk.Button(self.initface,text='人脸库照片添加',command=self.db)
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
        self.DB.place(relx=0.25,rely=0.35)
        tk.Label(self.DB, text="识别对象名称").grid(row=0)
        tk.entry1=tk.Entry(self.DB)
        tk.entry1.grid(row=0, column=1)
        # db_back = tk.Button(self.DB,text='退出',command=self.back)
        tk.Button(self.DB, text='选择存入人脸库的图片', command=self.load).grid(row=2, column=0,sticky=tk.W, padx=5, pady=5)
        # tk.Button(self.DB, text='Quit', command=self.load).grid(row=2, column=0,sticky=tk.W, padx=5, pady=5)
        tk.Button(self.DB, text='退出', command=self.back).grid(row=2, column=2,sticky=tk.W, padx=5, pady=5)
        # db_back.pack()
    def load(self):
        filePath = tk.filedialog.askopenfilename()
        if len(filePath) == 0 or tk.entry1.get()=="":
            print("filePath is null")
            root1=tk.Tk()
            tk.Label(root1,text='未输入人脸名称或图片路径不存在',fg='red',width=28, height=6).pack()
            tk.Button(root1,text='确定',width=3,height=1,command=root1.destroy).pack(side='bottom')
            return
        img = cv2.imdecode(np.fromfile(filePath, dtype=np.uint8), -1)
        cv2.imwrite("./face_DB/"+tk.entry1.get()+".jpg",img)
        root1=tk.Tk()
        tk.Label(root1,text='图片：'+tk.entry1.get()+' 已存入人脸库!',fg='green',width=20, height=6).pack()
        tk.Button(root1,text='确定',width=3,height=1,command=root1.destroy).pack(side='bottom')
        # return filePath

    def back(self):
        self.DB.destroy()
        initface(self.master)

class face1():
    def __init__(self,master):
        self.master = master
        # self.master.config(bg='blue')
        self.face1 = tk.Frame(self.master,)
        self.face1.place(relx=0.4,rely=0.55)
        self.predictor = Predictor(mtcnn_model_path='models/mtcnn',
                                    mobilefacenet_model_path='models/infer/model',
                                    face_db_path='face_db',
                                    threshold=0.6)
        atn_infer = tk.Button(self.face1,text='选择图片',command=self.infer)
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
            root1=tk.Tk()
            tk.Label(root1,text='识别成功，图片已保存在 ./dataset/'+names[0]+'.jpg',fg='red',width=40, height=6).pack()
            tk.Button(root1,text='确定',width=3,height=1,command=root1.destroy).pack(side='bottom')
            # cv2.imshow("esc is exit", img)
            while ((cv2.waitKey(1) & 0xFF) !=27):
                cv2.imshow("esc is exit", img)
                # pass
            cv2.destroyAllWindows()
        else:
            print("图片识别失败,不予保存")
            root1=tk.Tk()
            tk.Label(root1,text='图片识别失败,不予保存!',fg='red',width=20, height=6).pack()
            tk.Button(root1,text='确定',width=3,height=1,command=root1.destroy).pack(side='bottom')
    def back(self):
        self.face1.destroy()
        initface(self.master)


class face2():
    def __init__(self,master):
        self.master = master
        # self.master.config(bg='yellow')
        self.face2 = tk.Frame(self.master,)
        self.face2.place(relx=0.4,rely=0.55)
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
        self.face3.place(relx=0.4,rely=0.55)
        self.predictor = Predictor_Video(mtcnn_model_path='models/mtcnn',
                                   mobilefacenet_model_path='models/infer/model',
                                   face_db_path='face_db',
                                   threshold=0.6)
        # self.cap = cv2.VideoCapture(0)
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
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
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
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
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
    # canvas = tk.Canvas(root, width=1200,height=699,bd=0, highlightthickness=0)
    canvas = tk.Canvas(root, width=800, height=302, bg=None)
    image_file = tk.PhotoImage(file="dataset/denglu.gif")
    canvas.create_image(400, 0, anchor='n', image=image_file)
    canvas.pack()
    # land(root)
    basedesk(root)
    root.mainloop()

