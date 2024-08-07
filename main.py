from MSDefs import Block, Emi
from tkinter import *
from random import randint
import SettingsWin
import datetime


#----------------------------------------v-Main Window Code-v----------------------------------------------

if __name__ == "__main__":
    SIZEX,SIZEY,DIFFICULTY = SettingsWin.SettingsWindow()
    WND = Tk()

def PlayAgain():
    global WND,sprites,emi,tiles,dimensions,mineCount,SIZEX,SIZEY,DIFFICULTY,gameOver

    SIZEX,SIZEY,DIFFICULTY = SettingsWin.SettingsWindow()

    dimensions = {"x": SIZEX, "y": SIZEY}
    mineCount = round((dimensions["x"] * dimensions["y"]) * diffLevels[DIFFICULTY])

    sprites = []
    emi = Emi([],Frame,StringVar,Label)
    tiles = [] 
    gameOver = False
    
    WND = Tk()
    main()

def main():
    global WND

    MakeInterface()
    MakeGrid()

    WND.title("PySweeper")
    timer = datetime.datetime.now()

    WND.mainloop()
    timeEnd = round((datetime.datetime.now() - timer).total_seconds(),2)
    seconds = timeEnd % 60
    minutes = int(timeEnd // 60)# round((timeEnd % (60 * 60)) - seconds)
    print("\nTime: %02d:%05.2f" % (minutes, seconds))
    PlayAgain()
    

#----------------------------------------^-Main Window Code-^----------------------------------------------


#----------------------------------------v-Global Variables-v----------------------------------------------

emiIdle = ["Nice!","You got this!","I believe in you!",":)"]
gameOver = False
sprites:Block = []
emi = Emi([],Frame,StringVar,Label)
tiles:Block = []
diffLevels = [0.15, 0.2, 0.25]
showFrame = None
tileFrame = None
emiFrame = None
dimensions = {"x": SIZEX, "y": SIZEY}
mineCount = round((dimensions["x"] * dimensions["y"]) * diffLevels[DIFFICULTY])
safe = (dimensions["x"] * dimensions["y"]) - mineCount
flagDisplay = None
flagLabel = None
totalFlags = None
 
#----------------------------------------^-Global Variables-^----------------------------------------------


#----------------------------------------v-----Interface----v----------------------------------------------

def MakeInterface():
    global showFrame,tileFrame,flagDisplay,flagLabel,emi,sprites
    
    emi = Emi([],Frame(),StringVar(),Label())
    emi.frame = Frame(WND)
    emi.label = Label(emi.frame)
    
    emi.frame.pack()

    showFrame = Frame(WND)
    showFrame.pack()

    tileFrame = Frame(WND,width=100,height=100)
    tileFrame.pack()

    flagDisplay = IntVar(value=mineCount,name="flags")

    totalFlags = Label(showFrame,text="Flags Remaining: ")
    totalFlags.grid(row=3,column=1)
    emi.label.grid(row=1,column=1)
    emiSpeech = Label(emi.frame,textvariable=emi.speech)
    emiSpeech.grid(row=2,column=1)
    GetSprites()
    flagLabel = Label(showFrame,textvariable=flagDisplay)
    flagLabel.grid(row=3,column=3)
    # Bind the required functions to the frame, which will be inherited by the tiles
    tileFrame.bind_all("<Button-1>",OpenInit)
    tileFrame.bind_all("<Button-3>",Flag)
    emi.happy()

#----------------------------------------^-----Interface----^----------------------------------------------


#--------------------------------------------v-Functions-v-------------------------------------------------

# Run initialization for Open to get the coordinates, allowing FloodZero() to access Open without needing an event
def OpenInit(evnt):
    global flagDisplay
    # print(evnt,evnt.widget)
    try:
        # print(evnt.widget.winfo_parent(),tileFrame.winfo_name())
        if '!label' in evnt.widget._name and evnt.widget.winfo_parent() == "."+tileFrame.winfo_name():
        # Separate the name of the label into its coordinates
            try:
                    tileName = int(evnt.widget._name.removeprefix('!label'))-1
            except:
                # If it fails, then the label doesn't have a number attached, meaning it has to be the first label
                tileName = 0
        else:
            return None
    except AttributeError:
        return None
    
    # Select the tile by its coordinates, and open it with Open()
    tile = (tileName//dimensions.get("y"),tileName%dimensions.get("y"))
    Open(tile[0],tile[1])

def Flag(evnt):
    # Separate the name of the label into its coordinates
    try:
        if '!label' in evnt.widget._name and evnt.widget.winfo_parent() == "."+tileFrame.winfo_name():
        # Separate the name of the label into its coordinates
            try:
                tileName = int(evnt.widget._name.removeprefix('!label'))-1
            except:
                # If it fails, then the label doesn't have a number attached, meaning it has to be the first label
                tileName = 0
        else:
            return None
    except AttributeError:
        return None
    
    # Get the tile based on its coordinates, and toggle its flag state
    tile = (tileName//dimensions.get("y"),tileName%dimensions.get("y"))
    tile = tiles[tile[0]][tile[1]]
    if tile.open or gameOver:
        return None
    flagged = tile.FlagToggle()
    if not tile.open and not gameOver:
        if flagged:
            flagDisplay.set(flagDisplay.get()-1)
            CheckWin()
        else:
            flagDisplay.set(flagDisplay.get()+1)

def CalculateNeighbors(x,y):
    # Calculate the number of mines surrounding the block at the given coordinates
    
    # Initialize the number of mines at zero
    mines = 0

    # Run in a 3x3 grid
    for i in range(3):
        for j in range(3):

            # Set the target coordinates relative to the given coordinates
            targetx = x+(i-1)
            targety = y+(j-1)

            try:
                # Set the target based on the target coordinates
                target = tiles[targetx][targety]

                # Prevent the function from running at index -1, stopping it from incorrectly checking the rightmost block
                if targetx>-1 and targety>-1:
                        
                        #If the target is a mine, increment mines
                        if target.mine:
                            mines+=1
            except IndexError:
                pass
    
    # Return the number of mines surrounding the given coordinates
    return mines

# A flood fill command that opens all tiles surrounding a zero tile
def FloodZero(x,y):
    highestNeighbor = 0
    # Run as a 3x3 grid, getting the surrounding blocks recursively
    for i in range(3):
        for j in range(3):

            # Select the target tile relative to the given tile
            targetx = x+(i-1)
            targety = y+(j-1)

            try:
                # Only run if the target tile hasn't already been opened, to prevent an infinite recursion error
                target = tiles[targetx][targety]
                
                if targetx>-1 and targety>-1 and not target.open:
                        opened = Open(targetx,targety)
                        if opened > highestNeighbor:
                            highestNeighbor = opened
            except IndexError:
                # Prevents the fill from trying to go outside the bounds of the tiles
                pass
            except RecursionError:
                # If the fill hits infinite recursion anyway, just carry on
                pass
    return highestNeighbor

#Define Open as a function separate to Block.OpenBlock() so that it can access FloodZero()
def Open(x,y):
    global flagDisplay,safe,emi,emiIdle

    flooded = 0

    # Get the tile by the provided coordinates and open it through Block.OpenBlock()
    tile = tiles[x][y]

    closed = not tile.open

    if tile.flagged:
        flagDisplay.set(flagDisplay.get()+1)
    if closed:
        safe-=1

    mine = tile.OpenBlock()

    # If it's a mine, you lose, so run Disable()
    if mine:
        Disable()
        tile.label.configure(image=sprites[12])
    
    else:
        # If a tile has zero neighbors that are mines, then the 8 tiles surrounding it must be safe
        if tile.mineNeighbors == 0:
            # So run FloodZero()
            flooded = FloodZero(x,y)
        if tile.mineNeighbors > flooded:
            flooded = tile.mineNeighbors
        
        if closed:
            if tile.mineNeighbors == 0:
                emi.interest()
                emi.speak("Ooh! A zero fill!")
            elif flooded > 5:
                emi.shock()
                emi.speak("!!!")
            elif flooded > 3:
                emi.nervous()
                emi.speak("Eek!")
            else:
                emi.happy()
                if randint(1,100) <= 15:
                    emi.speak(emiIdle[randint(0,len(emiIdle)-1)])
                else:
                    emi.speech.set("")
    CheckWin()

    return flooded

def CheckWin():
    global flagDisplay,safe
    if (safe <= 0 and flagDisplay.get() == 0):
        WinGame()

def MakeTile(x,y):
    global tileFrame, sprites

    # Define a label and apply it to a grid
    lbl = Label(tileFrame,image=sprites[10],borderwidth=0)
    lbl.grid(column=x+1,row=y+1)

    # Create a Block object and return it
    tile = Block(x,y,sprites,lbl)
    return tile

def Disable():
    global gameOver

    gameOver = True

    # Disable clicking for all the tiles by opening them
    emi.dead()
    emi.speak("*dies*")
    for column in tiles:
        for tile in column:

            # Open every block
            tile.OpenBlock()

def AddMine():
    
    # Choose a random candidate from all the tiles
    candidate = tiles[randint(0,dimensions.get("x")-1)][randint(0,dimensions.get("y")-1)]
    
    # If the candidate is not already a mine
    if not candidate.mine:

        # Turn the candidate into a mine
        candidate.mine = True
    else:

        #Otherwise, re-run the code until a valid candidate is found
        AddMine()
        # NOTE: Could lead to a recursion bug if there are more mines than tiles

def GetSprites():
    for i in range(13): # There are 13 sprites for the buttons

        # Iteratively append the sprites to btnImg so that they can all be accessed easily
        sprites.append(PhotoImage(file=".\\assets\\button\\button_%02d.png" % i))

    for i in range(6): # We use 6 sprites for Emi
        emi.sprites.append(PhotoImage(file=".\\assets\\face\\emi_%d.png" % i))

def MakeGrid():
    # Iterate through the columns
    for i in range(dimensions.get("x")):

        # Empty the column list before each iteration
        tileColumn = []

        # Iterate through the rows
        for j in range(dimensions.get("y")):

            # Create a tile and append it to the column list
            tileColumn.append(MakeTile(i,j))
        # Add the column list to the blocks[] list, creating a 2D list that can be accessed through coordinates
        tiles.append(tileColumn)

    for i in range(mineCount):

        # Create the number of mines dictated by the mineCount variable
        AddMine()

    for column in tiles:
        
        # Iterating through a 2D list
        for tile in column:
            
            # Pre-calculate the number of mines are surrounding the tile, then add that to the Block object
            tile.mineNeighbors = CalculateNeighbors(tiles.index(column),column.index(tile))

#--------------------------------------------^-Functions-^-------------------------------------------------

def WinGame():
    print("Victory!")
    emi.joy()
    emi.speak("Woo! You did it!")


if __name__ == "__main__":
    # Start the main program loop
    main()