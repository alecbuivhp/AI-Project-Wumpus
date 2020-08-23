import world, tile
from tkinter import *

class Board:
    def __init__(self, root, world):
        self.canvas = Canvas(root, width=64*world.width, height=64*world.height, background='white')
        self.canvas.pack()

        self.world = world

        self.tiles = []
        self.objects = []
        self.warnings = []
        self.terrains = []
        self.player = None

            # Load images
        self.DOOR = PhotoImage(file='assets/door.png')
        self.TILE = PhotoImage(file='assets/floor.png')
        self.GOLD_TILE = PhotoImage(file='assets/floor_gold.png')

        self.WUMPUS = PhotoImage(file='assets/wumpus.png')
        self.GOLD = PhotoImage(file='assets/gold.png')
        self.PIT = PhotoImage(file='assets/pit.png')

        self.TERRAIN = PhotoImage(file='assets/terrain.png')

        self.PLAYER_DOWN = PhotoImage(file='assets/agent_down.png')
        self.PLAYER_UP = PhotoImage(file='assets/agent_up.png')
        self.PLAYER_LEFT = PhotoImage(file='assets/agent_left.png')
        self.PLAYER_RIGHT = PhotoImage(file='assets/agent_right.png')

        # TODO: Score here?

    def createWorld(self):
        for i in range(self.world.height):
            tiles_line = []
            for j in range(self.world.width):
                tiles_line.append(self.canvas.create_image(64 * j, 64 * i, image=self.TILE, anchor=NW))
            self.tiles.append(tiles_line)


        self.canvas.delete(self.tiles[self.world.coordDoor[0]][self.world.coordDoor[1]])
        self.tiles[self.world.coordDoor[0]][self.world.coordDoor[1]] = self.canvas.create_image(64 * self.world.coordDoor[1], 64 * self.world.coordDoor[0], image=self.DOOR, anchor=NW)


        for i in range(self.world.height):
            objects_line = []
            for j in range(self.world.width):
                tile_at_loc = self.world.listTiles[i][j]
                if tile_at_loc.getPit():
                    objects_line.append(self.canvas.create_image(64 * j, 64 * i, image=self.PIT, anchor=NW))
                elif tile_at_loc.getWumpus():
                    objects_line.append(self.canvas.create_image(64 * j, 64 * i, image=self.WUMPUS, anchor=NW))
                elif tile_at_loc.getGold():
                    self.canvas.delete(self.tiles[i][j])
                    self.tiles[i][j] = self.canvas.create_image(64 * j, 64 * i, image=self.GOLD_TILE, anchor=NW)
                    objects_line.append(self.canvas.create_image(64 * j, 64 * i, image=self.GOLD, anchor=NW))
                else:
                    objects_line.append(None)
            self.objects.append(objects_line)


        for i in range(self.world.height):
            warnings_line = []
            for j in range(self.world.width):
                tile_at_loc = self.world.listTiles[i][j]
                first_cord = (i, j)
                if tile_at_loc.getBreeze():
                    warnings_line.append(self.canvas.create_text(64 * j + 3, 64 * i, fill='white', font='Verdana 10', text='Breeze', anchor=NW))
                if tile_at_loc.getStrench():
                    warnings_line.append(self.canvas.create_text(64 * j + 3, (64 * i) + 15, fill='white', font='Verdana 10', text='Strench', anchor=NW))
                if not tile_at_loc.getBreeze() and not tile_at_loc.getStrench():
                    warnings_line.append(None)
            self.warnings.append(warnings_line)


        for i in range(self.world.height):
            terrains_line = []
            for j in range(self.world.width):
                tile_at_loc = self.world.listTiles[i][j]
                if tile_at_loc.getPlayer():
                    player = self.canvas.create_image(64 * j, 64 * i, image=self.PLAYER_RIGHT, anchor=NW)
                    terrains_line.append(None)
                else:
                    terrains_line.append(self.canvas.create_image(64 * j, 64 * i, image=self.TERRAIN, anchor=NW))
            self.terrains.append(terrains_line)


#############################################################

wumpus_world = world.WumpusWorld()
wumpus_world.read_Map('map\original.txt')

root = Tk()
board = Board(root, wumpus_world)
board.createWorld()



root.mainloop()