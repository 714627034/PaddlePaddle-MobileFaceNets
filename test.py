#导入需要的模块
import tkinter as tk
import tkinter.filedialog

import pandas as pd
import matplotlib.pyplot as plt


#主界面的建立
root = tk.Tk()
root.title("一款简单的数据可视化小软件")

#设置界面大小
root.minsize(500,350)

#定义函数
def fileChose():
    filePath = tkinter.filedialog.askopenfilename()
    df = pd.read_csv(filePath)
    x = df.iloc[:,0].values
    y = df.iloc[:,1].values
    plt.bar(x,y)

def savePathChose():
    resultPlot = tkinter.filedialog.askdirectory()
    plt.savefig(resultPlot+"/barPlot.pdf")
    print("The result barplot has been saved in",resultPlot)

#摆放按钮
btn1 = tk.Button(root,text="选择数据",command=fileChose)
btn1.pack()

btn2 = tk.Button(root,text="选择结果保存路径",command=savePathChose)
btn2.pack()

#画布
canvas = tk.Canvas(root)
image_file = tk.PhotoImage(file="a.gif")
image = canvas.create_image(0,0,anchor="nw",image=image_file)
canvas.pack()

root.mainloop()