from tkinter import Label

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
            