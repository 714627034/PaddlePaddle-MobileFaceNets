import tkinter
from tkinter.messagebox import *
index = tkinter.Tk()  #创建主窗口
# index.attributes('-alpha',1)  #窗口背景透明化
index.title('登录界面 v1.0.0') #设置主窗口标题
index.geometry('500x400') #设置主窗口大小
#下面两行代码的作用是固定窗口大小，不可拉动调节
index.maxsize(500,300)
index.minsize(500,300)

#**************************************************
#                 添加组件

# 加载图片
canvas = tkinter.Canvas(index, width=500, height=300, bg=None)
image_file = tkinter.PhotoImage(file="dataset/background.gif")
image = canvas.create_image(250, 0, anchor='n', image=image_file)
canvas.pack()

#账号与密码文字标签
account_lable = tkinter.Label(index, text = '账号', bg='lightskyblue', fg='white', font=('Arial', 12), width=5, height=1)
account_lable.place(relx=0.29,rely=0.4)
pasw_lable = tkinter.Label(index, text = '密码', bg='lightskyblue', fg='white', font=('Arial', 12), width=5, height=1)
pasw_lable.place(relx=0.29,rely=0.5)

#账号与密码输入框
account = tkinter.Entry(index,width=20,highlightthickness = 1,highlightcolor = 'lightskyblue',relief='groove')  #账号输入框
account.place(relx=0.4,rely=0.4 )  #添加进主页面,relx和rely意思是与父元件的相对位置
password = tkinter.Entry(index,show='*',highlightthickness = 1,highlightcolor = 'lightskyblue',relief='groove')  #密码输入框
password.place(relx=0.4,rely=0.5) #添加进主页面

user = {"admin":"123456"}  #定义一个字典来存储用户的信息(key :账号 , value：密码)


#登录按钮处理函数
def login():
    ac = account.get()
    ps = password.get()
    if (ac == "" or ps == ""):
        showinfo("用户登录", "请完整填写信息！！")  # messagebox的方法
    elif user.get(ac) != ps:
        account.delete(0,'end')  #清空文本框的内容
        password.delete(0,'end')  #清空文本框的内容
        showinfo("用户登录", "账号或者密码有误！")   #messagebox的方法
    else:
        account.delete(0, 'end')  # 清空文本框的内容
        password.delete(0, 'end')  # 清空文本框的内容
        showinfo("用户登录", "登录成功！即将进入菜单界面....")  # messagebox的方法

def reguest():
    ac = account.get()
    ps = password.get()
    if (ac == "" or ps == ""):
        showinfo("用户登录", "请完整填写信息！！")  # messagebox的方法
    elif ac in user:
        account.delete(0,'end')  #清空文本框的内容
        password.delete(0,'end')  #清空文本框的内容
        showinfo("用户注册", "账号已存在！")   #messagebox的方法
    else:
        user[ac] = ps
        account.delete(0, 'end')  # 清空文本框的内容
        password.delete(0, 'end')  # 清空文本框的内容
        showinfo("用户注册", "注册成功！")  # messagebox的方法
#登录与注册按钮
loginBtn = tkinter.Button(index,text='登录',font = ('宋体',12),width=4,height=1,command=login,relief='solid',bd = 0.5,bg='lightcyan')
loginBtn.place(relx=0.41,rely=0.63)
loginBtn = tkinter.Button(index,text='注册',font = ('宋体',12),width=4,height=1,bd=0.5,command=reguest,relief='solid',bg='lightcyan')
loginBtn.place(relx=0.56,rely=0.63)

#**************************************************
index.mainloop() #使窗口不断刷新，应该放在代码最后一句