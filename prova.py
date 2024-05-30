import tkinter as tk
from PIL import Image, ImageTk
from GestionePagine.Widgets.Immagini.MySharedMultiImg import *
root = tk.Tk()

canvas1 = tk.Canvas()
canvas1.place(x = 0,y = 0,width=5000,height=5000, anchor="nw")
canvas2 = tk.Canvas()
canvas2.place(x = 100,y = 0,width=5000,height=5000, anchor="nw")
canvas3 = tk.Canvas()
canvas3.place(x = 200,y = 0,width=5000,height=5000, anchor="nw")

path = "ImmagineLogo.png"
path2 = "ImmagineLogo copy.png"
smi = MySharedMultiImg(pathsDict={"1" : path, "2" : path2})
i1 = 0
i2 = 0
i3 = 0
def f():
    i1 = smi.Show(canvas1, "1")
    i2 = smi.Show(canvas2, "1")
    i3 = smi.Show(canvas3, "1")
def g():
    global i1,i2,i3
    i1 = smi.Show(canvas1, "2", i1)
    i2 = smi.Show(canvas2, "2", i2)
    i3 = smi.Show(canvas3, "2", i3)
f() 
smi.ChangePaths({"1" : path, "2" : path2})
smi.ResizeAll(25,25)
g()
root.mainloop()