from MSDefs import Block
from tkinter import *
from random import randint

sprites = []
blocks = []

dimensions = {"x":12,"y":15}
mineCount:int = round((dimensions["x"]+dimensions["y"])*1.5)

WND = Tk()
WND.title("PySweeper")

def CalculateNeighbors(x,y):
    mines = 0
    for i in range(3):
        for j in range(3):
            targetx = x+(i-1)
            targety = y+(j-1)
            try:
                target = blocks[targetx][targety]
                if targetx>-1 and targety>-1:
                        if target.mine:
                            mines+=1
            except IndexError:
                pass
    return mines

def FloodZero(x,y):
    for i in range(3):
        for j in range(3):
            targetx = x+(i-1)
            targety = y+(j-1)
            target = blocks[targetx][targety]
            if targetx>-1 and targety>-1 and not target.open:
                try:
                    Open(targetx,targety)
                except IndexError:
                    pass
                except RecursionError:
                    pass

def open_init(evnt):
    try:
        tileName = int(evnt.widget._name.removeprefix('!label'))-1
    except:
        tileName = 0
    tile = (tileName//dimensions.get("y"),tileName%dimensions.get("y"))
    Open(tile[0],tile[1])

def Open(x,y):
    block = blocks[x][y]
    mine = block.OpenBlock()
    if mine:
        Disable()
    if block.mineNeighbors == 0:
        FloodZero(x,y)

def Flag(evnt):
    try:
        tileName = int(evnt.widget._name.removeprefix('!label'))-1
    except:
        tileName = 0
    tile = (tileName//dimensions.get("y"),tileName%dimensions.get("y"))
    blocks[tile[0]][tile[1]].FlagToggle()

def MakeTile(x,y):
    lbl = Label(tiles,image=sprites[10],borderwidth=0)
    lbl.grid(column=x+1,row=y+2)
    tile = Block(x,y,sprites,lbl)
    return tile

def Disable():
    for column in blocks:
        for tile in column:
            tile.OpenBlock()

def AddMine():
    candidate = blocks[randint(0,dimensions.get("x")-1)][randint(0,dimensions.get("y")-1)]
    if not candidate.mine:
        candidate.mine = True
    else:
        AddMine()

# Create the main frame, which will hold the tiles
tiles = Frame(WND,width=100,height=100)
tiles.pack()

# Bind the functions to the frame, which will be inherited by the tiles
tiles.bind_all("<Button-1>",open_init)
tiles.bind_all("<Button-3>",Flag)


#There are 12 sprites
for i in range(12):
    # Iteratively append the sprites to btnImg so that they can all be accessed easily
    sprites.append(PhotoImage(file=f".\\assets\\button\\sprite_{i}.png"))

# Iterate through the columns
for i in range(dimensions.get("x")):
    # Empty the column list before each iteration
    tileColumn = []
    # Iterate through the rows
    for j in range(dimensions.get("y")):
        # Create a tile and append it to the column list
        tileColumn.append(MakeTile(i,j))
    # Add the column list to the blocks[] list, creating a 2D list that can be accessed through coordinates
    blocks.append(tileColumn)

for i in range(mineCount):
    AddMine()

for column in blocks:
    for tile in column:
        tile.mineNeighbors = CalculateNeighbors(blocks.index(column),column.index(tile))


#Start the main program loop
WND.mainloop()