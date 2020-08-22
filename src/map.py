import tile

class WumpusWorld:
    def __init__(self):
        """Initialize an empty board"""
        self.__height = 0
        self.__width = 0
        self.__listTiles = []

    def get_Adjacents(self, i, j):
        adj = []

        if i - 1 >= 0:
            adj.append((i - 1, j))
        if i + 1 <= self.__height - 1:
            adj.append((i + 1, j))
        if j - 1 >= 0:
            adj.append((i, j - 1))
        if j + 1 <= self.__width - 1:
            adj.append((i, j + 1))

        return adj

    def read_Map(self, filename):
        try:
            with open(filename, 'r') as f:
                lines = f.read().splitlines()
                self.__height = len(lines)

                tiles = []
                for line in lines:
                    tiles.append(line.split('.'))
                self.__width = len(tiles[0])

                # Empty tiles map
                for i in range(self.__height):
                    tile_line = []
                    for j in range(self.__width):
                        tile_line.append(tile.Tile())
                    self.__listTiles.append(tile_line)

                # Tile's objects
                for i in range(self.__height):
                    for j in range(self.__width):
                        if 'G' in tiles[i][j]:
                            (self.__listTiles[i][j]).setGold()
                        if 'P' in tiles[i][j]:
                            (self.__listTiles[i][j]).setPit()
                            adj = self.get_Adjacents(i, j)
                            for a in adj:
                                (self.__listTiles[a[0]][a[1]]).setBreeze()
                        if 'W' in tiles[i][j]:
                            (self.__listTiles[i][j]).setWumpus()    
                            adj = self.get_Adjacents(i, j)
                            for a in adj:
                                (self.__listTiles[a[0]][a[1]]).setStrench()
                        if 'A' in tiles[i][j]:
                            (self.__listTiles[i][j]).setPlayer()    
        except IOError:
            return None

    def generate_Map(self, numPit, numWumpus, numGold):
        pass

world = WumpusWorld()
world.read_Map('map\original.txt')