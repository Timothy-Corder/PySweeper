from tkinter import Label,StringVar,Frame
import time

class Emi:
    def __init__(self,sprites:list,frame:Frame,speech:StringVar,label:Label):
        self.sprites = sprites
        self.label = label
        self.speech = speech
        self.frame = frame
    def switch(self,face):
        self.label.configure(image=self.sprites[face])
    def happy(self):
        self.switch(0)
    def interest(self):
        self.switch(1)
    def joy(self):
        self.switch(2)
    def dead(self):
        self.switch(3)
    def nervous(self):
        self.switch(4)
    def shock(self):
        self.switch(5)
    def speak(self,text:str):
        self.speech.set(value="Emi: "+text)

class Block:
    def __init__(self,x:int,y:int,images:list,label=Label):
        self.x = x
        self.y = y
        self.mine = False
        self.open = False
        self.flagged = False
        self.mineNeighbors = 0
        self.label = label
        self.images = images
    def FlagToggle(self):
        if not self.open:
            self.flagged = not self.flagged
            if self.flagged:
                self.label.configure(image=self.images[11])
            else:
                self.label.configure(image=self.images[10])
            return self.flagged
    def OpenBlock(self):
        if not self.open:
            self.open = True
            if not self.mine:
                self.label.configure(image=self.images[self.mineNeighbors])
                return False
            else:
                self.label.configure(image=self.images[9])
                return True
            