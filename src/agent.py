from src.gamestate import *
from src.kb import *

class Agent:
    def __init__(self ,state, direction):
        self.current_state = state
        self.current_direction = direction
        self.has_gold = 0
        self.has_killed_wumpus = 0
        self.is_leaving = False

    def move_foward(self,state):
        if self.current_direction == "Left" and state[self.current_state].left != 'Wall':
            self.current_state = state[self.current_state].left
        elif self.current_direction == "Right" and state[self.current_state].right != 'Wall':
            self.current_state = state[self.current_state].right
        elif self.current_direction == "Up" and state[self.current_state].up != 'Wall':
            self.current_state = state[self.current_state].up
        elif self.current_direction == "Down" and state[self.current_state].down != 'Wall':
            self.current_state = state[self.current_state].down

    def turn_left(self):
        self.current_direction = "Left"

    def turn_right(self):
        self.current_direction = "Right"

    def turn_up(self):
        self.current_direction = "Up"

    def turn_down(self):
        self.current_direction = "Down"

    def shoot(self):
        pass

class Level_solver(Agent):
    #FIX starting node
    def __init__(self,world,starting_node): #Starting node = (1,1)
        self.state = GameState(world)
        self.state.add_state(Node(starting_node.row, starting_node.col))
        self.agent = Agent(state = starting_node.name, direction = "Right")
        self.KB = Knowledge_base()
        self.KB.add(["~P" + str(starting_node.name)])
        self.KB.add(["~W" + str(starting_node.name)])
        self.direction = ['Up','Left','Down','Right']
        self.exit = False
        self.move = []
        self.start_stench = False

        def getAction(self,current_tile):
            current_node = self.state.state[self.agent.current_state]
            if current_node.name == starting_node and current_tile.getStench() and not current_tile.getBreeze():
                self.start_stench = True
                self.shoot()



