from MSDefs import Block
from tkinter import *
from random import randint


#----------------------------------------v-Settings Window-v------------------------------------------------

SETWND = Tk()


SETWND.mainloop()

#----------------------------------------^-Settings Window-^----------------------------------------------

#----------------------------------------v-Main Window Code-v----------------------------------------------

#Create the game window
WND = Tk()
WND.title("PySweeper")

# Initialize the variables that aren't reliant on the settings
sprites = []
tiles = []

tileFrame = Frame(WND,width=100,height=100)
tileFrame.pack()

# Initialize the variables that are reliant on the settings
dimensions = {"x":12,"y":15}
mineCount:int = round((dimensions["x"]*dimensions["y"])*0.1)

#----------Define open_init and Flag early, to bind them to the frame

# Run initialization for Open to get the coordinates, allowing FloodZero() to access Open without needing an event
def open_init(evnt):

    # Separate the name of the label into its coordinates
    try:
        tileName = int(evnt.widget._name.removeprefix('!label'))-1
    except:
        # If it fails, then the label doesn't have a number attached, meaning it has to be the first label
        tileName = 0
    
    # Select the tile by its coordinates, and open it with Open()
    tile = (tileName//dimensions.get("y"),tileName%dimensions.get("y"))
    Open(tile[0],tile[1])

def Flag(evnt):

    # Separate the name of the label into its coordinates
    try:
        tileName = int(evnt.widget._name.removeprefix('!label'))-1
    except:
        # If it fails, then the label doesn't have a number attached, meaning it has to be the first label
        tileName = 0
    
    # Get the tile based on its coordinates, and toggle its flag state
    tile = (tileName//dimensions.get("y"),tileName%dimensions.get("y"))
    tiles[tile[0]][tile[1]].FlagToggle()



# Bind the required functions to the frame, which will be inherited by the tiles
tileFrame.bind_all("<Button-1>",open_init)
tileFrame.bind_all("<Button-3>",Flag)



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

    # Run as a 3x3 grid, getting the surrounding blocks recursively
    for i in range(3):
        for j in range(3):

            # Select the target tile relative to the given tile
            targetx = x+(i-1)
            targety = y+(j-1)

            # Only run if the target tile hasn't already been opened, to prevent an infinite recursion error
            target = tiles[targetx][targety]
            
            if targetx>-1 and targety>-1 and not target.open:
                try:
                    Open(targetx,targety)
                except IndexError:
                    # Prevents the fill from trying to go outside the bounds of the tiles
                    pass
                except RecursionError:
                    pass

#Define Open as a function separate to Block.OpenBlock() so that it can access FloodZero()
def Open(x,y):

    # Get the tile by the provided coordinates and open it through Block.OpenBlock()
    tile = tiles[x][y]
    mine = tile.OpenBlock()

    # If it's a mine, you lose, so run Disable()
    if mine:
        Disable()

    # If a tile has zero neighbors that are mines, then the 8 tiles surrounding it must be safe
    if tile.mineNeighbors == 0:

        # So run FloodZero()
        FloodZero(x,y)

def MakeTile(x,y):

    # Define a label and apply it to a grid
    lbl = Label(tileFrame,image=sprites[10],borderwidth=0)
    lbl.grid(column=x+1,row=y+2)

    # Create a Block object and return it
    tile = Block(x,y,sprites,lbl)
    return tile

def Disable():

    # Disable clicking for all the tiles by opening them
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



for i in range(12): #There are 12 sprites for the buttons

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
    tiles.append(tileColumn)

for i in range(mineCount):

    # Create the number of mines dictated by the mineCount variable
    AddMine()

for column in tiles:
    
    # Iterating through a 2D list
    for tile in column:
        
        # Pre-calculate the number of mines are surrounding the tile, then add that to the Block object
        tile.mineNeighbors = CalculateNeighbors(tiles.index(column),column.index(tile))


# Start the main program loop
WND.mainloop()


#----------------------------------------^-Main Window Code-^----------------------------------------------