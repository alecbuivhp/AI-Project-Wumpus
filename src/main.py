import world, graphics

wumpus_world = world.WumpusWorld()
wumpus_world.read_Map('../map/original.txt')
# wumpus_world.generate_Map((0, 0), 10, 10, 10, 10, 10)

board = graphics.Board(wumpus_world)
board.createWorld()

board.mainloop()