import tile
from random import randrange

class WumpusWorld:
    def __init__(self):
        """Initialize an empty board"""
        self.height = 0
        self.width = 0
        self.__numGold = 0
        self.__numWumpus = 0    
        self.listTiles = []
        self.doorPos = None

    def get_Adjacents(self, i, j):
        adj = []

        if i - 1 >= 0:
            adj.append((i - 1, j))
        if i + 1 <= self.height - 1:
            adj.append((i + 1, j))
        if j - 1 >= 0:
            adj.append((i, j - 1))
        if j + 1 <= self.width - 1:
            adj.append((i, j + 1))  

        return adj

    def read_Map(self, filename):
        try:
            with open(filename, 'r') as f:
                lines = f.read().splitlines()
                lines = lines[1:]
                self.height = len(lines)

                tiles = []
                for line in lines:
                    tiles.append(line.split('.'))
                self.width = len(tiles[0])

                # Empty tiles map
                for i in range(self.height):
                    tile_line = []
                    for j in range(self.width):
                        tile_line.append(tile.Tile())
                    self.listTiles.append(tile_line)

                # Tile's objects
                for i in range(self.height):
                    for j in range(self.width):
                        if 'G' in tiles[i][j]:
                            (self.listTiles[i][j]).setGold()
                            self.__numGold += 1
                        if 'P' in tiles[i][j]:
                            (self.listTiles[i][j]).setPit()
                            adj = self.get_Adjacents(i, j)
                            for a in adj:
                                (self.listTiles[a[0]][a[1]]).setBreeze()
                        if 'W' in tiles[i][j]:
                            (self.listTiles[i][j]).setWumpus()    
                            self.__numWumpus += 1
                            adj = self.get_Adjacents(i, j)
                            for a in adj:
                                (self.listTiles[a[0]][a[1]]).setStench()
                        if 'A' in tiles[i][j]:
                            (self.listTiles[i][j]).setPlayer()
                            self.doorPos =  (i, j)
        except IOError:
            return None

    def generate_Map(self, agentPos, numPit, numWumpus, numGold, mapHeight, mapWidth):
        """Generate random map: A pit, wumpus or gold will not exist at the same tile also they are not at the door"""
        self.height = mapHeight
        self.width = mapWidth

        for i in range(self.height):
            tile_line = []
            for j in range(self.width):
                tile_line.append(tile.Tile())
            self.listTiles.append(tile_line)

        self.doorPos = agentPos
        self.listTiles[agentPos[0]][agentPos[1]].setPlayer()

        self.__numGold = numGold
        for i in range(self.__numGold):
            while True:
                randomPos = (randrange(self.height), randrange(self.width))
                if not randomPos == self.doorPos and not self.listTiles[randomPos[0]][randomPos[1]].getPit() and not self.listTiles[randomPos[0]][randomPos[1]].getWumpus() and not self.listTiles[randomPos[0]][randomPos[1]].getGold():
                    self.listTiles[randomPos[0]][randomPos[1]].setGold()
                    break
                    
        for i in range(numPit):
            while True:
                randomPos = (randrange(self.height), randrange(self.width))
                if not randomPos == self.doorPos and not self.listTiles[randomPos[0]][randomPos[1]].getPit() and not self.listTiles[randomPos[0]][randomPos[1]].getWumpus() and not self.listTiles[randomPos[0]][randomPos[1]].getGold():
                    self.listTiles[randomPos[0]][randomPos[1]].setPit()
                    adj = self.get_Adjacents(randomPos[0], randomPos[1])
                    for a in adj:
                        (self.listTiles[a[0]][a[1]]).setBreeze()
                    break

        
        self.__numWumpus = numWumpus
        for i in range(self.__numWumpus):
            while True:
                randomPos = (randrange(self.height), randrange(self.width))
                if not randomPos == self.doorPos and not self.listTiles[randomPos[0]][randomPos[1]].getPit() and not self.listTiles[randomPos[0]][randomPos[1]].getWumpus() and not self.listTiles[randomPos[0]][randomPos[1]].getGold():
                    self.listTiles[randomPos[0]][randomPos[1]].setWumpus()
                    adj = self.get_Adjacents(randomPos[0], randomPos[1])
                    for a in adj:
                        (self.listTiles[a[0]][a[1]]).setStench()
                    break

    def grabGold(self, i , j):
        self.__numGold -= 1
        self.listTiles[i][j].removeGold()
    
    def killWumpus(self, i, j):
        self.__numWumpus -= 1
        self.listTiles[i][j].removeWumpus()
        adj = self.get_Adjacents(i, j)
        for a in adj:
            if self.listTiles[a[0]][a[1]].getStench():
                self.listTiles[a[0]][a[1]].removeStench()

    def movePlayer(self, before_i, before_j, after_i, after_j):
        self.listTiles[before_i][before_j].removePlayer()
        self.listTiles[after_i][after_j].setPlayer()

    def leftGold(self):
        return False if self.__numGold == 0 else True

    def leftWumpus(self):
        return False if self.__numWumpus == 0 else True


    ################################# DEBUGGING #################################

    def printWorld(self):
        string = []
        for i in range(self.height):
            line = []
            for j in range(self.width):
                line.append(self.listTiles[i][j].printTile())
            string.append(line)
        
        for i in string:
            print(i)