import world, tile, bind, controller
from tkinter import *
from tkinter import font
import time

# Propositional logic agent 
import gamestate, agent

DELAY = 50

class Board:
    def __init__(self, world):
        self.root = Tk()
        self.root.title("WUMPUS WORLD")

        self.canvas = Canvas(self.root, width=64 * world.width, height=64 * world.height + 64, background='white')
        self.canvas.pack()
        
        # self.root.bind("<Key>", self.updateBoard) # Manual agent

        self.world = world

        self.tiles = []
        self.objects = []
        self.warnings = []
        self.terrains = []
        self.player = None
        self.display_score = None

        self.scoreFont = font.Font(family='KacstBook', size=22)

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
        self.ARROW_DOWN = PhotoImage(file='assets/arrow_down.png')
        self.ARROW_UP = PhotoImage(file='assets/arrow_up.png')
        self.ARROW_LEFT = PhotoImage(file='assets/arrow_left.png')
        self.ARROW_RIGHT = PhotoImage(file='assets/arrow_right.png')
        self.SCORE = PhotoImage(file='assets/score_icon.png')

        # Game state
        self.gameState = bind.GameState.NOT_RUNNING

        # Agent
        # self.agent = controller.ManualAgent()
        self.agent = None # PL agent

        self.agentPos = None

        # Score
        self.score = 0

    ############################# CREATE WORLD #############################

    def createWorld(self):
        for i in range(self.world.height):
            tiles_line = []
            for j in range(self.world.width):
                tiles_line.append(self.canvas.create_image(64 * j, 64 * i, image=self.TILE, anchor=NW))
            self.tiles.append(tiles_line)


        self.canvas.delete(self.tiles[self.world.doorPos[0]][self.world.doorPos[1]])
        self.tiles[self.world.doorPos[0]][self.world.doorPos[1]] = self.canvas.create_image(64 * self.world.doorPos[1], 64 * self.world.doorPos[0], image=self.DOOR, anchor=NW)


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


        warningFont = font.Font(family='Verdana', size=10)
        for i in range(self.world.height):
            warnings_line = []
            for j in range(self.world.width):
                warning_at_loc = []
                tile_at_loc = self.world.listTiles[i][j]
                first_cord = (i, j)
                if tile_at_loc.getBreeze():
                    warning_at_loc.append(self.canvas.create_text(64 * j + 3, 64 * i, fill='white', font=warningFont, text='Breeze', anchor=NW))
                else:
                    warning_at_loc.append(None)
                if tile_at_loc.getStench():
                    warning_at_loc.append(self.canvas.create_text(64 * j + 3, (64 * i) + 50, fill='white', font=warningFont, text='Stench', anchor=NW))
                else:
                    warning_at_loc.append(None)
                if not tile_at_loc.getBreeze() and not tile_at_loc.getStench():
                    warnings_line.append(None)
                else:
                    warnings_line.append(warning_at_loc)
            self.warnings.append(warnings_line)

        for i in range(self.world.height):
            terrains_line = []
            for j in range(self.world.width):
                tile_at_loc = self.world.listTiles[i][j]
                if tile_at_loc.getPlayer():
                    self.player = self.canvas.create_image(64 * j, 64 * i, image=self.PLAYER_RIGHT, anchor=NW)
                    self.agentPos = (i, j)
                    terrains_line.append(None)
                else:
                    terrains_line.append(self.canvas.create_image(64 * j, 64 * i, image=self.TERRAIN, anchor=NW))
            self.terrains.append(terrains_line)

        # Init PL agent
        starting_node = gamestate.Node(self.agentPos[0], self.agentPos[1], self.world)
        self.agent = agent.Level_solver(self.world, starting_node)

        #self.world.printWorld()

        self.canvas.create_rectangle(0, 64 * self.world.height, 64 * self.world.width, 64 * self.world.height + 64, fill='#85888a')
        self.canvas.create_image(64, 64 * self.world.height + 16, image=self.SCORE, anchor=NW)
        self.score_display = self.canvas.create_text(64 + 64, 64 * self.world.height + 16, fill='#ffff00', font=self.scoreFont, text=str(self.score), anchor=NW)

    ############################# ACTIONS #############################
    
    def validPos(self, pos):
        return pos[0] >= 0 and pos[0] <= self.world.height - 1 and pos[1] >= 0 and pos[1] <= self.world.width - 1


    def moveForward(self, action): # action: current action
        nextPos = None
        fixed_x = 0
        fixed_y = 0

        if action == bind.Action.LEFT:
            nextPos = (self.agentPos[0], self.agentPos[1] - 1)
            fixed_x = -64
        elif action == bind.Action.RIGHT:
            nextPos = (self.agentPos[0], self.agentPos[1] + 1)
            fixed_x = 64
        elif action == bind.Action.UP:
            nextPos = (self.agentPos[0] - 1, self.agentPos[1])
            fixed_y = -64
        elif action == bind.Action.DOWN:
            nextPos = (self.agentPos[0] + 1, self.agentPos[1])
            fixed_y = 64
                
        if self.validPos(nextPos):
            self.world.movePlayer(self.agentPos[0], self.agentPos[1], nextPos[0], nextPos[1])
            self.agentPos = nextPos
            
            if self.terrains[self.agentPos[0]][self.agentPos[1]]:
                self.canvas.delete(self.terrains[self.agentPos[0]][self.agentPos[1]])
                self.terrains[self.agentPos[0]][self.agentPos[1]] = None
            
            self.canvas.move(self.player, fixed_x, fixed_y)
            self.agent.currentState = action

            self.score -= 10
            self.canvas.itemconfig(self.score_display, text=str(self.score))

            tile_at_loc = self.world.listTiles[self.agentPos[0]][self.agentPos[1]]
            if tile_at_loc.getPit():
                self.score -= 10000
                self.canvas.itemconfig(self.score_display, text=str(self.score))
                self.canvas.update()
                time.sleep(0.5)
                self.endGame("Pit")
            elif tile_at_loc.getWumpus():
                self.score -= 10000
                self.canvas.itemconfig(self.score_display, text=str(self.score))
                self.canvas.update()
                time.sleep(0.5)
                self.endGame("Wumpus")


    def shootForward(self, direction): # direction: current state
        arrow = None
        arrow_loc = None
        if self.agent.currentState == bind.Action.LEFT:
            arrow_loc = (self.agentPos[0], self.agentPos[1] - 1)
            arrow = self.canvas.create_image(64 * arrow_loc[1], 64 * arrow_loc[0], image=self.ARROW_LEFT, anchor=NW)
        elif self.agent.currentState == bind.Action.RIGHT:
            arrow_loc = (self.agentPos[0], self.agentPos[1] + 1)
            arrow = self.canvas.create_image(64 * arrow_loc[1], 64 * arrow_loc[0], image=self.ARROW_RIGHT, anchor=NW)
        elif self.agent.currentState == bind.Action.UP:
            arrow_loc = (self.agentPos[0] - 1, self.agentPos[1])
            arrow = self.canvas.create_image(64 * arrow_loc[1], 64 * arrow_loc[0], image=self.ARROW_UP, anchor=NW)
        elif self.agent.currentState == bind.Action.DOWN:
            arrow_loc = (self.agentPos[0] + 1, self.agentPos[1])
            arrow = self.canvas.create_image(64 * arrow_loc[1], 64 * arrow_loc[0], image=self.ARROW_DOWN, anchor=NW)

        self.canvas.update()
        time.sleep(0.5)
        self.canvas.delete(arrow)

        self.score -= 100
        self.canvas.itemconfig(self.score_display, text=str(self.score))


        if self.world.listTiles[arrow_loc[0]][arrow_loc[1]].getWumpus():
            self.agent.scream = True
            # UPDATE WORLD
            self.world.killWumpus(arrow_loc[0], arrow_loc[1])

            # UPDATE BOARD
            if self.terrains[arrow_loc[0]][arrow_loc[1]]:
                self.canvas.delete(self.terrains[arrow_loc[0]][arrow_loc[1]])
                self.terrains[arrow_loc[0]][arrow_loc[1]] = None
                
            self.canvas.delete(self.objects[arrow_loc[0]][arrow_loc[1]])
            self.objects[arrow_loc[0]][arrow_loc[1]] = None

            adj = self.world.get_Adjacents(arrow_loc[0], arrow_loc[1])
            for a in adj:
                if not self.world.listTiles[a[0]][a[1]].getStench():
                    self.canvas.delete(self.warnings[a[0]][a[1]][1])
                    self.warnings[a[0]][a[1]][1] = None

            # END GAME ?
            if not self.world.leftWumpus() and not self.world.leftGold():
                self.endGame("Clear")



    def grabGold(self):
        if self.world.listTiles[self.agentPos[0]][self.agentPos[1]].getGold():
            self.score += 100
            self.canvas.itemconfig(self.score_display, text=str(self.score))

            # UPDATE WORLD
            self.world.grabGold(self.agentPos[0], self.agentPos[1])

            # UPDATE BOARD
            self.canvas.delete(self.objects[self.agentPos[0]][self.agentPos[1]])
            self.objects[self.agentPos[0]][self.agentPos[1]] = None

            self.canvas.delete(self.tiles[self.agentPos[0]][self.agentPos[1]])
            self.tiles[self.agentPos[0]][self.agentPos[1]] = self.canvas.create_image(64 * self.agentPos[1], 64 * self.agentPos[0], image=self.TILE, anchor=NW)

                # Overlapping handle            
            if self.warnings[self.agentPos[0]][self.agentPos[1]]:
                if (self.warnings[self.agentPos[0]][self.agentPos[1]])[0]:
                    self.canvas.tag_raise(self.warnings[self.agentPos[0]][self.agentPos[1]][0], self.tiles[self.agentPos[0]][self.agentPos[1]])
                if (self.warnings[self.agentPos[0]][self.agentPos[1]])[1]:
                    self.canvas.tag_raise(self.warnings[self.agentPos[0]][self.agentPos[1]][1], self.tiles[self.agentPos[0]][self.agentPos[1]])
            self.canvas.tag_raise(self.player, self.tiles[self.agentPos[0]][self.agentPos[1]])

            # END GAME ?
            if not self.world.leftWumpus() and not self.world.leftGold():
                self.endGame("Clear")

    def endGame(self, reason):
        self.gameState = bind.GameState.NOT_RUNNING
        time.sleep(2)
        for i in range(self.world.height):
            for j in range(self.world.width):
                if self.terrains[i][j]:
                    self.canvas.delete(self.terrains[i][j])
        
        print(reason)

    # def endGame(self, reason):
    #     self.canvas.delete("all")
    #     self.canvas.config(width=64 * self.world.width, height=64 * self.world.height)
    #     self.canvas.create_rectangle(0, 0, 64 * self.world.width, 64 * self.world.height, fill='#704917')

    #     endFont = font.Font(family='KacstBook', size=35, weight='bold')
    #     self.canvas.create_text((64 * self.world.width) // 2, (64 * self.world.height) // 2, fill='#ffffff', font=endFont, text='GAME ENDED', anchor=CENTER)

    #     reasonFont = font.Font(family='KacstBook', size=25)
    #     if reason == 'Pit':
    #         self.canvas.create_text((64 * self.world.width) // 2, ((64 * self.world.height) // 2) // 2 + 64, fill='#d5d5d5', font=reasonFont, text='You fell into a Pit', anchor=CENTER)
    #     elif reason == 'Wumpus':
    #         self.canvas.create_text((64 * self.world.width) // 2, ((64 * self.world.height) // 2) // 2 + 64, fill='#d5d5d5', font=reasonFont, text='You were killed by a Wumpus', anchor=CENTER)
    #     elif reason == 'Climb':
    #         self.canvas.create_text((64 * self.world.width) // 2, ((64 * self.world.height) // 2) // 2 + 64, fill='#d5d5d5', font=reasonFont, text='You climb out of the Cave', anchor=CENTER)
    #     elif reason == 'Clear':
    #         self.canvas.create_text((64 * self.world.width) // 2, ((64 * self.world.height) // 2) // 2 + 64, fill='#d5d5d5', font=reasonFont, text='You cleared the Map', anchor=CENTER)

    #     self.canvas.create_image((64 * self.world.width) // 2 - 70, ((64 * self.world.height) // 2) + 64 + 30, image=self.SCORE, anchor=NW)
    #     self.canvas.create_text((64 * self.world.width) // 2, ((64 * self.world.height) // 2) + 124 - 30, fill='#ffff00', font=self.scoreFont, text=str(self.score), anchor=NW)

    #     self.root.unbind("<Key>")
        
    #     self.gameState = bind.GameState.NOT_RUNNING

    ############################# INPUT AND UPDATE GAME #############################

    def updateBoard(self, event):
        key = event.char
        action = self.agent.getAction(key)

        if action == bind.Action.DOWN:
            if action == self.agent.currentState:
                self.moveForward(action)
            else:
                self.canvas.itemconfigure(self.player, image=self.PLAYER_DOWN)
                self.agent.currentState = bind.Action.DOWN
        elif action == bind.Action.UP:
            if action == self.agent.currentState:
                self.moveForward(action)
            else:
                self.canvas.itemconfigure(self.player, image=self.PLAYER_UP)
                self.agent.currentState = bind.Action.UP
        elif action == bind.Action.LEFT:
            if action == self.agent.currentState:
                self.moveForward(action)
            else:
                self.canvas.itemconfigure(self.player, image=self.PLAYER_LEFT)
                self.agent.currentState = bind.Action.LEFT
        elif action == bind.Action.RIGHT:
            if action == self.agent.currentState:
                self.moveForward(action)
            else:
                self.canvas.itemconfigure(self.player, image=self.PLAYER_RIGHT)
                self.agent.currentState = bind.Action.RIGHT
        elif action == bind.Action.SHOOT:
            self.shootForward(self.agent.currentState)
        elif action == bind.Action.GRAB:
            self.grabGold()
        elif action == bind.Action.CLIMB:
            if self.agentPos == self.world.doorPos:
                self.score += 10
                self.endGame("Climb")

    ############################# MAIN LOOP #############################
        # Manual agent's
    # def mainloop(self):
    #     self.root.mainloop()

        # PL agent's
    def mainloop(self):
        self.gameState = bind.GameState.RUNNING

        while self.gameState == bind.GameState.RUNNING:
            action = self.agent.getAction()

            if action == bind.Action.DOWN:
                if action == self.agent.currentState:
                    self.moveForward(action)
                else:
                    self.canvas.itemconfigure(self.player, image=self.PLAYER_DOWN)
                    self.agent.currentState = bind.Action.DOWN
            elif action == bind.Action.UP:
                if action == self.agent.currentState:
                    self.moveForward(action)
                else:
                    self.canvas.itemconfigure(self.player, image=self.PLAYER_UP)
                    self.agent.currentState = bind.Action.UP
            elif action == bind.Action.LEFT:
                if action == self.agent.currentState:
                    self.moveForward(action)
                else:
                    self.canvas.itemconfigure(self.player, image=self.PLAYER_LEFT)
                    self.agent.currentState = bind.Action.LEFT
            elif action == bind.Action.RIGHT:
                if action == self.agent.currentState:
                    self.moveForward(action)
                else:
                    self.canvas.itemconfigure(self.player, image=self.PLAYER_RIGHT)
                    self.agent.currentState = bind.Action.RIGHT
            elif action == bind.Action.SHOOT:
                self.shootForward(self.agent.currentState)
            elif action == bind.Action.GRAB:
                self.grabGold()
            elif action == bind.Action.CLIMB:
                if self.agentPos == self.world.doorPos:
                    self.score += 10
                    self.endGame("Climb")

            self.root.update()
            self.root.after(DELAY)
            # self.world.printWorld()

        self.root.mainloop()

##########################################################################################################
#FIX 10G-0P-10W
wumpus_world = world.WumpusWorld()
wumpus_world.read_Map('map/10G-10P-10W-base.txt')
# wumpus_world.generate_Map((0, 0), 10, 10, 10, 10, 10)

board = Board(wumpus_world)
board.createWorld()

board.mainloop()