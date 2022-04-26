import tkinter as tk
def jiemian1():
    root1=tk.Tk()
    bu1=tk.Button(root1,text="第一个窗口",command=lambda:[root1.destroy(),jiemian2()])
    bu1.grid(row=0,column=0)
    root1.mainloop()

def jiemian2():
    root2=tk.Tk()
    bu1=tk.Button(root2,text="第二个窗口",command=lambda:[root2.destroy(),jiemian1()])
    bu1.grid(row=0,column=0)
    root2.mainloop()

jiemian1()


