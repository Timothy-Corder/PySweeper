from tkinter import *

def SettingsWindow():
    SETWND = Tk()

    def only_numbers(char:str):
        return char.isdigit()
        
    validation = SETWND.register(only_numbers)

    sizeFrame = Frame(SETWND)
    doneFrame = Frame(SETWND)
    diffFrame = Frame(SETWND)

    launchMS = Button(doneFrame,text="Launch PySweeper",command=SETWND.destroy)
    launchMS.pack()

    diff = IntVar()
    x = StringVar(value=15)
    y = StringVar(value=15)

    xLabel = Label(sizeFrame,text="Size (x,y): ")
    xLabel.grid(row=1,column=1)
    xGet = Spinbox(sizeFrame,width=2,validate="key",justify=CENTER,validatecommand=(validation, '%S'),from_=5,to=30,textvariable=x)
    xGet.grid(row=1,column=2)

    yLabel = Label(sizeFrame,text="x")
    yLabel.grid(row=1,column=3)
    yGet = Spinbox(sizeFrame,width=2,validate="key",justify=CENTER,validatecommand=(validation, '%S'),from_=5,to=30,textvariable=y)
    yGet.grid(row=1,column=4)

    diffLabel = Label(diffFrame,text="Difficulty:")
    diffLabel.grid(row=2,column=1)
    diffEasy = Radiobutton(diffFrame,text="Easy", variable=diff, value=0)
    diffEasy.grid(row=1,column=2,sticky=W)
    diffMed = Radiobutton(diffFrame,text="Medium", variable=diff, value=1)
    diffMed.grid(row=2,column=2,sticky=W)
    diffHard = Radiobutton(diffFrame,text="Hard", variable=diff, value=2)
    diffHard.grid(row=3,column=2,sticky=W)


    def on_closing():
        SETWND.destroy()
        exit(0)
    SETWND.protocol("WM_DELETE_WINDOW", on_closing)

    sizeFrame.pack()
    diffFrame.pack()
    doneFrame.pack()


    SETWND.mainloop()

    return (int(x.get()),int(y.get()),diff.get())