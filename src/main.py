import world, graphics
import sys
import os.path

wumpus_world = world.WumpusWorld()

if sys.argv[1] == 'random':
    agentPos_i, agentPos_j, numPit, numWumpus, numGold = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]
    if int(numPit) + int(numGold) + int(numWumpus) >= 100:
        print("Invalid arguments. Please check your command")
    else:
        try:
            wumpus_world.generate_Map((int(agentPos_i), int(agentPos_j)), int(numPit), int(numWumpus), int(numGold), 10, 10)
        except:
            print("Something is wrong. Please check your command.")
        board = graphics.Board(wumpus_world)
        board.createWorld()
        board.mainloop()
elif sys.argv[1] == 'file':
    map_name = sys.argv[2]
    if os.path.isfile('../map/' + map_name):
        wumpus_world.read_Map('../map/' + map_name)
        board = graphics.Board(wumpus_world)
        board.createWorld()
        board.mainloop()
    else:
        print("Unavailable map. Please check your path.")
else:
    print("Unavailable command. Please check user manual.")
