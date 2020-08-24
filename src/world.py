import tile

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
                                (self.listTiles[a[0]][a[1]]).setStrench()
                        if 'A' in tiles[i][j]:
                            (self.listTiles[i][j]).setPlayer()
                            self.doorPos =  (i, j)
        except IOError:
            return None

    def generate_Map(self, numPit, numWumpus, numGold):
        pass

    def grabGold(self, i , j):
        self.__numGold -= 1
        self.listTiles[i][j].removeGold()
    
    def killWumpus(self, i, j):
        self.__numWumpus -= 1
        self.listTiles[i][j].removeWumpus()
        adj = self.get_Adjacents(i, j)
        for a in adj:
            if self.listTiles[a[0]][a[1]].getStrench():
                self.listTiles[a[0]][a[1]].removeStrench()

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

        print()