"""
this file defines all the datastrues will be used in the assignment
"""


#The cards players have
class MyNode:
    def __init__(self, role,side,coordinate,board):
        # 0 = paper; 1 = siser; 2 = stone, 3= rock
        self.role = role
        # upper/ lower/ Neutral
        self.side = side
        self.coordinate = coordinate
        board.addtoboard(self)
    
    def getside(self):
        return self.side
    
    def getrole(self):
        return self.role

    def NodeImfo(self):
        print("Coordinate: " + str(self.coordinate) + " role: " + str(self.role) + "  side: " + self.side)
    
    def Move(self, NewCoordinate,board):
        board.moveOnboard(self,NewCoordinate)
        self.coordinate =  NewCoordinate
    
    def getx(self):
        return self.coordinate[0] + 4
    
    def gety(self):
        return self.coordinate[1] + 4

# A singeleton board
class Board:
    __instance = None

    @staticmethod 
    def getInstance():
        if Board.__instance == None:
            raise Exception("You have to initialise board first")
        return Board.__instance
   
    def __init__(self):
        if Board.__instance != None:
            raise Exception("Overwritting the board!")
        else:
            Board.__instance = self
            #mellocating a n x n empty grid            
            Board.grid = [[] for i in range(9)]
            for i in range(9):
                self.grid[i] = [None]*9
            # filling the board with grid
            ran = range(-4, +4+1)
            for (r,q) in [(r,q) for r in ran for q in ran if -r-q in ran]:
                self.grid[r+4][q+4] = grid((r,q))
         
            for (r,q) in [(r,q) for r in ran for q in ran if -r-q in ran]:
                if(r+1 in ran and q in ran and -(r+1)-(q) in ran):
                    (self.grid[r+4][q+4]).surrounding.append(self.grid[r+5][q+4])

                if(r+1 in ran and q-1 in ran and -(r+1)-(q-1) in ran):
                    (self.grid[r+4][q+4]).surrounding.append(self.grid[r+5][q+3])
                if(r in ran and q-1 in ran and -(r)-(q-1) in ran):
                    (self.grid[r+4][q+4]).surrounding.append(self.grid[r+4][q+3])
                if(r-1 in ran and q in ran and -(r-1)-(q) in ran):
                    (self.grid[r+4][q+4]).surrounding.append(self.grid[r+3][q+4])
                if(r-1 in ran and q+1 in ran and -(r-1)-(q+1) in ran):
                    (self.grid[r+4][q+4]).surrounding.append(self.grid[r+3][q+5])
                if(r in ran and q+1 in ran and -(r)-(q+1) in ran):
                    (self.grid[r+4][q+4]).surrounding.append(self.grid[r+4][q+5])
    
    def addtoboard(self, card):
        self.grid[card.getx()][card.gety()].cards.append(card)

    def moveOnboard(self,card,Newcoordinate):
        self.grid[card.getx()][card.gety()].cards.remove(card)
        self.grid[Newcoordinate[0] + 4][Newcoordinate[1] + 4].cards.append(card)

class grid:
    
    def __init__(self, coordinate):
        self.surrounding = []
        self.coordinate = coordinate
        self.cards = []

    def PrintAGrid(self):
        print(self.coordinate,end='')
    def PrintSurroundings(self):
        for i in self.surrounding:
            print(i.coordinate,end='')
            print(", ",end = '')
    def getx(self):
        return (self.coordinate[0]+4)
    def gety(self):
        return (self.coordinate[1]+4)