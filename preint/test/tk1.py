# -*- coding: cp936 -*-
from Tkinter import *
root = Tk()
root.title("hello world")
root.geometry('600x800')

Label(root, text='校训'.decode('gbk').encode('utf8'), font=('Arial', 20)).pack()

frm = Frame(root)
#left
frm_L = Frame(frm)
Label(frm_L, text='厚德'.decode('gbk').encode('utf8'), font=('Arial', 15)).pack(side=TOP)
Label(frm_L, text='博学'.decode('gbk').encode('utf8'), font=('Arial', 15)).pack(side=BOTTOM)
frm_L.pack(side=LEFT)

#right
frm_R = Frame(frm)
Label(frm_R, text='敬业'.decode('gbk').encode('utf8'), font=('Arial', 15)).pack(side=TOP)
Label(frm_R, text='乐群'.decode('gbk').encode('utf8'), font=('Arial', 15)).pack(side=BOTTOM)
frm_R.pack(side=RIGHT)

frm.pack()

root.mainloop()
