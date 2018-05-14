import Tkinter as tkinter
from Tkinter import *

global s

s='sssss'
def func1():
    s='fucked!'
    outputtext.set(s)

root = Tk()                        #base window
buttonfrm = Frame(root)            #'button frame' is in Root window
buttonfrm.pack()

textframe = Frame(root)       #text frame in Root window
textframe.pack(side=LEFT)

btnfrm=Frame(root)
btnfrm.pack(side=BOTTOM)

inputbutton = Button(buttonfrm, text="Input",command=func1)       #command = helloCallBack
inputbutton.pack()

outputbutton = Button(buttonfrm, text="Output")
outputbutton.pack()




inputtext=StringVar()
inputmsg=Label(textframe,textvariable=inputtext, relief=RAISED)
inputtext.set(s)
inputmsg.pack()

s='changed!'
outputtext=StringVar()
outputmsg=Label(textframe,textvariable=outputtext, relief=RAISED)
outputtext.set(s)
outputmsg.pack()



#run & exit button
runbutton = Button(btnfrm, text="RUN!",fg='red')
runbutton.pack()

exitbutton = Button(btnfrm, text="EXIT!",command=root.quit)
exitbutton.pack()

root.mainloop()
