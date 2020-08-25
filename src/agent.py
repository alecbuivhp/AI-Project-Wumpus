from src.gamestate import *
from src.kb import *
from src.bind import *
from src.world import *

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
            if current_node.name == starting_node and current_node.getStench() and not current_node.getBreeze():
                self.start_stench = True
                sentence = world.get_Adjacents(current_node.row, current_node.col)
                for adjecent in sentence:
                    self.KB.add(['W'+ str(adjecent)])
                self.move.append(('Right', Action.SHOOT))

            elif current_node.getStench():
                self.KB.add(['~W'+current_node.right])
                self.move.append(('Up', Action.SHOOT))

            elif current_node.getStench():
                self.KB.add(['~W'+current_node.up])
                self.move.append(('Left',Action.SHOOT))

            elif current_node.getStench():
                self.KB.add(['~W'+current_node.left])
                self.move.append(('Down', Action.SHOOT))
                self.KB.add(['~W'+current_node.down])
            else:
                self.start_stench = False
                self.clearKB()

        def clearKB(self):
            remove = []
            for item in self.KB.KB:
                if item[0][0] == 'W' or item[0][1] == 'W':
                    remove.append(item)
            for item in remove:
                self.KB.KB.remove(item)


        def handle_breeze(self,current_node):
            sentence = []
            prefix = ''
            current_prefix = ''
            if current_node.getBreeze():
                prefix = 'P'
                current_prefix = 'B'
            elif not current_node.getBreeze():
                prefix = '~P'
                current_prefix = '~B'

            if current_node.right not in self.state.visited and current_node.right == 'Wall':
                sentence.append(prefix + current_node.right)
            if current_node.up not in self.state.visited and current_node.up == 'Wall':
                sentence.append(prefix + current_node.up)
            if current_node.left not in self.state.visited and current_node.left == 'Wall':
                sentence.append(prefix + current_node.left)
            if current_node.down not in self.state.visited and current_node.down == 'Wall':
                sentence.append(prefix + current_node.down)
            self.KB.add(sentence)
            self.KB.add([current_prefix + current_node.name])

        def handle_stench(self,current_node):
            sentence = []
            prefix = ''
            current_prefix = ''
            if current_node.getStench():
                prefix = 'W'
                current_prefix = 'S'
            elif not current_node.getStench():
                prefix = '~W'
                current_prefix = '~S'
            if current_node.right not in self.state.visited and current_node.right == 'Wall':
                sentence.append(prefix + current_node.right)
            if current_node.up not in self.state.visited and current_node.up == 'Wall':
                sentence.append(prefix + current_node.up)
            if current_node.left not in self.state.visited and current_node.left == 'Wall':
                sentence.append(prefix + current_node.left)
            if current_node.down not in self.state.visited and current_node.down == 'Wall':
                sentence.append(prefix + current_node.down)
            self.KB.add(sentence)
            self.KB.add([current_prefix+ current_node.name])

        def check_safe(self, current_node):
            if current_node.right != 'Wall' and current_node.right not in self.state.visited and current_node.right not in self.state.unvisited_safe:
                # alpha = \neg U . Safe => U = '~W' => \neg U = 'W'
                if self.KB.check(['W'+current_node.right]) and self.KB.check(['P'+current_node.right]):
                    self.state.unvisited_safe.append(current_node.right)

            if current_node.up != 'Wall' and current_node.up not in self.state.visited and current_node.up not in self.state.unvisited_safe:
                if self.KB.check(['W'+current_node.up]) and self.KB.check(['P'+current_node.up]):
                    self.state.unvisited_safe.append(current_node.up)

            if current_node.left != 'Wall' and current_node.left not in self.state.visited and current_node.left not in self.state.unvisited_safe:
                if self.KB.check(['W'+current_node.left]) and self.KB.check(['P'+current_node.left]):
                    self.state.unvisited_safe.append(current_node.left)

            if current_node.down != 'Wall' and current_node.down not in self.state.visited and current_node.down not in self.state.unvisited_safe:
                if self.KB.check(['W'+current_node.down]) and self.KB.check(['P'+current_node.down]):
                    self.state.unvisited_safe.append(current_node.down)

        def check_wumpus(self, current_node):
            if current_node.right != 'Wall':
                if self.KB.check(['~W'+str(current_node.right)]) and self.KB.check(['~S'+current_node.name]):
                    self.move.append(('Right',Action.SHOOT))
            if current_node.up != 'Wall':
                if self.KB.check(['~W'+str(current_node.up)]) and self.KB.check(['~S'+current_node.name]):
                    self.move.append(('Up',Action.SHOOT))
            if current_node.left != 'Wall':
                if self.KB.check(['~W'+str(current_node.left)]) and self.KB.check(['~S'+current_node.name]):
                    self.move.append(('Left',Action.SHOOT))
            if current_node.down != 'Wall':
                if self.KB.check(['~W'+str(current_node.down)]) and self.KB.check(['~S'+current_node.name]):
                    self.move.append(('Down',Action.SHOOT))

        def getKB(self):
            return self.KB.KB