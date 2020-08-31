import world, tile, bind, controller
from tkinter import *
from tkinter import font
from tkinter import scrolledtext
import time

# Propositional logic agent 
import gamestate, agent

DELAY = 10

class Board:
    def __init__(self, world):
        self.root = Tk()
        self.root.title("WUMPUS WORLD")
        self.root.geometry("+200+50")

        self.canvas = Canvas(self.root, width=64 * world.width, height=64 * world.height + 64, background='white')
        self.outputFrame = Frame(self.root)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.outputFrame.pack(side="right", fill="both", expand=False)
        
        # KB and Action
        self.KBArea = None
        self.actionArea = None
        self.buttonStep = None
        self.buttonRun = None
        self.buttonFont = font.Font(size=10)

        self.runMode = -1

        self.world = world

        self.tiles = []
        self.objects = []
        self.warnings = []
        self.terrains = []
        self.player = None
        self.display_score = None

        self.scoreFont = font.Font(family='KacstBook', size=22)

        # Load images
        self.DOOR = PhotoImage(file='../assets/door.png')
        self.TILE = PhotoImage(file='../assets/floor.png')
        self.GOLD_TILE = PhotoImage(file='../assets/floor_gold.png')
        self.WUMPUS = PhotoImage(file='../assets/wumpus.png')
        self.GOLD = PhotoImage(file='../assets/gold.png')
        self.PIT = PhotoImage(file='../assets/pit.png')
        self.TERRAIN = PhotoImage(file='../assets/terrain.png')
        self.PLAYER_DOWN = PhotoImage(file='../assets/agent_down.png')
        self.PLAYER_UP = PhotoImage(file='../assets/agent_up.png')
        self.PLAYER_LEFT = PhotoImage(file='../assets/agent_left.png')
        self.PLAYER_RIGHT = PhotoImage(file='../assets/agent_right.png')
        self.ARROW_DOWN = PhotoImage(file='../assets/arrow_down.png')
        self.ARROW_UP = PhotoImage(file='../assets/arrow_up.png')
        self.ARROW_LEFT = PhotoImage(file='../assets/arrow_left.png')
        self.ARROW_RIGHT = PhotoImage(file='../assets/arrow_right.png')
        self.SCORE = PhotoImage(file='../assets/score_icon.png')

        # Game state
        self.gameState = bind.GameState.NOT_RUNNING

        # Agent
        # self.agent = controller.ManualAgent()
        # self.root.bind("<Key>", self.updateBoard) # Manual agent
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

        self.canvas.create_rectangle(0, 64 * self.world.height, 64 * self.world.width, 64 * self.world.height + 64, fill='#85888a')
        self.canvas.create_image(64, 64 * self.world.height + 16, image=self.SCORE, anchor=NW)
        self.score_display = self.canvas.create_text(64 + 64, 64 * self.world.height + 16, fill='#ffff00', font=self.scoreFont, text=str(self.score), anchor=NW)


        # Output frame
        self.buttonStep = Button(self.outputFrame, text='STEP', height=2, width=30, command=lambda: self.changeRunMode(0))
        self.buttonRun = Button(self.outputFrame, text='RUN ALL', height=2, width=30, command=lambda: self.changeRunMode(1))
        self.buttonStep['font'] = self.buttonFont
        self.buttonRun['font'] = self.buttonFont
        
        self.KBArea = scrolledtext.ScrolledText(self.outputFrame, wrap=WORD, width=40, height=20, font=('Verdana', 15))
        self.actionArea = scrolledtext.ScrolledText(self.outputFrame, wrap=WORD, width=40, height=6, font=('Verdana', 15))

        self.buttonStep.grid(row=0, column=0)
        self.buttonRun.grid(row=0, column=1)
        self.KBArea.grid(row=1, column=0, columnspan=2)
        self.actionArea.grid(row=2, column=0, columnspan=2)

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
                self.actionArea.insert(END, 'ACTION: Clear map\n')
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
                self.actionArea.insert(END, 'ACTION: Clear map\n')
                self.endGame("Clear")


    def endGame(self, reason):
        self.gameState = bind.GameState.NOT_RUNNING
        for i in range(self.world.height):
            for j in range(self.world.width):
                if self.terrains[i][j]:
                    self.canvas.delete(self.terrains[i][j])
        self.buttonRun['state'] = DISABLED
        self.buttonStep['state'] = DISABLED


    def senseObject(self):
        if self.world.listTiles[self.agentPos[0]][self.agentPos[1]].getStench() and self.world.listTiles[self.agentPos[0]][self.agentPos[1]].getBreeze():
            self.actionArea.insert(END, 'SENSE: Stench, Breeze\n')
        else:
            if self.world.listTiles[self.agentPos[0]][self.agentPos[1]].getStench():
                self.actionArea.insert(END, 'SENSE: Stench\n')
            if self.world.listTiles[self.agentPos[0]][self.agentPos[1]].getBreeze():
                self.actionArea.insert(END, 'SENSE: Breeze\n')

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
                self.endGame("Climb")

    def changeRunMode(self, key):
        self.runMode = key        
        self.mainloop()
        
    ############################# MAIN LOOP #############################
        # Manual agent's
    # def mainloop(self):
    #     self.root.mainloop()

        # PL agent's
    def mainloop(self):
        self.gameState = bind.GameState.RUNNING

        if self.runMode == 1:
            while self.gameState == bind.GameState.RUNNING:
                self.senseObject()
                self.actionArea.see(END)
                action = self.agent.getAction()

                # Update KB
                    # CLEAR KB
                self.KBArea.delete(1.0, END)
                    # Rewrite KB
                for i in range(len(self.agent.KB.KB)):
                    temp_string = 'R' + str(i + 1) + ': '
                    for j in self.agent.KB.KB[i]:
                        if j[0] == '~':
                            temp_string += '¬' + j[1:]
                        else:
                            temp_string += j
                        if j != self.agent.KB.KB[i][-1]:
                            temp_string += ' ∨ '
                    self.KBArea.insert(END, temp_string + '\n')
                    self.KBArea.see(END)


                if action == bind.Action.DOWN:
                    if action == self.agent.currentState:
                        self.actionArea.insert(END, 'ACTION: Move forward\n')
                        self.moveForward(action)
                    else:
                        self.canvas.itemconfigure(self.player, image=self.PLAYER_DOWN)
                        self.actionArea.insert(END, 'ACTION: Face down\n')
                        self.agent.currentState = bind.Action.DOWN
                elif action == bind.Action.UP:
                    if action == self.agent.currentState:
                        self.actionArea.insert(END, 'ACTION: Move forward\n')
                        self.moveForward(action)
                    else:
                        self.canvas.itemconfigure(self.player, image=self.PLAYER_UP)
                        self.actionArea.insert(END, 'ACTION: Face up\n')
                        self.agent.currentState = bind.Action.UP
                elif action == bind.Action.LEFT:
                    if action == self.agent.currentState:
                        self.actionArea.insert(END, 'ACTION: Move forward\n')
                        self.moveForward(action)
                    else:
                        self.canvas.itemconfigure(self.player, image=self.PLAYER_LEFT)
                        self.actionArea.insert(END, 'ACTION: Face left\n')
                        self.agent.currentState = bind.Action.LEFT
                elif action == bind.Action.RIGHT:
                    if action == self.agent.currentState:
                        self.actionArea.insert(END, 'ACTION: Move forward\n')
                        self.moveForward(action)
                    else:
                        self.canvas.itemconfigure(self.player, image=self.PLAYER_RIGHT)
                        self.actionArea.insert(END, 'ACTION: Face right\n')
                        self.agent.currentState = bind.Action.RIGHT
                elif action == bind.Action.SHOOT:
                    self.actionArea.insert(END, 'ACTION: Shoot arrow\n')
                    self.shootForward(self.agent.currentState)
                elif action == bind.Action.GRAB:
                    self.actionArea.insert(END, 'ACTION: Grab gold\n')
                    self.grabGold()
                elif action == bind.Action.CLIMB:
                    self.actionArea.insert(END, 'ACTION: Climb out\n')
                    self.actionArea.see(END)
                    if self.agentPos == self.world.doorPos:
                        self.score += 10
                        self.canvas.itemconfig(self.score_display, text=str(self.score))
                        self.endGame("Climb")
                
                # self.senseObject()
                self.actionArea.see(END)
                self.root.update()
                self.root.after(DELAY)

            self.root.mainloop()

        elif self.runMode == 0:
            if self.gameState == bind.GameState.RUNNING:
                self.senseObject()
                self.actionArea.see(END)

                action = self.agent.getAction()

                # Update KB
                    # CLEAR KB
                self.KBArea.delete(1.0, END)
                    # Rewrite KB
                for i in range(len(self.agent.KB.KB)):
                    temp_string = 'R' + str(i + 1) + ': '
                    for j in self.agent.KB.KB[i]:
                        if j[0] == '~':
                            temp_string += '¬' + j[1:]
                        else:
                            temp_string += j
                        if j != self.agent.KB.KB[i][-1]:
                            temp_string += ' ∨ '
                    self.KBArea.insert(END, temp_string + '\n')
                    self.KBArea.see(END)


                if action == bind.Action.DOWN:
                    if action == self.agent.currentState:
                        self.actionArea.insert(END, 'ACTION: Move forward\n')
                        self.moveForward(action)
                    else:
                        self.canvas.itemconfigure(self.player, image=self.PLAYER_DOWN)
                        self.actionArea.insert(END, 'ACTION: Face down\n')
                        self.agent.currentState = bind.Action.DOWN
                elif action == bind.Action.UP:
                    if action == self.agent.currentState:
                        self.actionArea.insert(END, 'ACTION: Move forward\n')
                        self.moveForward(action)
                    else:
                        self.canvas.itemconfigure(self.player, image=self.PLAYER_UP)
                        self.actionArea.insert(END, 'ACTION: Face up\n')
                        self.agent.currentState = bind.Action.UP
                elif action == bind.Action.LEFT:
                    if action == self.agent.currentState:
                        self.actionArea.insert(END, 'ACTION: Move forward\n')
                        self.moveForward(action)
                    else:
                        self.canvas.itemconfigure(self.player, image=self.PLAYER_LEFT)
                        self.actionArea.insert(END, 'ACTION: Face left\n')
                        self.agent.currentState = bind.Action.LEFT
                elif action == bind.Action.RIGHT:
                    if action == self.agent.currentState:
                        self.actionArea.insert(END, 'ACTION: Move forward\n')
                        self.moveForward(action)
                    else:
                        self.canvas.itemconfigure(self.player, image=self.PLAYER_RIGHT)
                        self.actionArea.insert(END, 'ACTION: Face right\n')
                        self.agent.currentState = bind.Action.RIGHT
                elif action == bind.Action.SHOOT:
                    self.actionArea.insert(END, 'ACTION: Shoot arrow\n')
                    self.shootForward(self.agent.currentState)
                elif action == bind.Action.GRAB:
                    self.actionArea.insert(END, 'ACTION: Grab gold\n')
                    self.grabGold()
                elif action == bind.Action.CLIMB:
                    self.actionArea.insert(END, 'ACTION: Climb out\n')
                    self.actionArea.see(END)
                    if self.agentPos == self.world.doorPos:
                        self.score += 10
                        self.canvas.itemconfig(self.score_display, text=str(self.score))
                        self.endGame("Climb")
                
                # self.senseObject()
                self.actionArea.see(END)
                self.root.update()
                self.root.after(DELAY)

            self.root.mainloop()

        else:
            self.root.mainloop()