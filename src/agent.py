import gamestate
import kb
import bind
import world

# from src.gamestate import *
# from src.kb import *
# from src.bind import *
# from src.world import *

class Agent:
    def __init__(self, state):
        self.current_state = state
        self.current_direction = bind.Action.RIGHT
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
        self.state = gamestate.Game_State(world)
        self.state.add_state(gamestate.Node(starting_node.row, starting_node.col,world))
        self.agent = Agent(state = starting_node.name)
        self.KB = kb.Knowledge_base()
        self.KB.add(["~P" + str(starting_node.name)])
        self.KB.add(["~W" + str(starting_node.name)])
        self.direction = ['Up','Left','Down','Right']
        self.exit = False
        self.move = []
        self.start_stench = False
        self.starting_node = starting_node
        self.world = world
        self.currentState = bind.Action.RIGHT

    def getAction(self):
        if self.move:
            return self.move.pop()

        current_node = self.state.state[self.agent.current_state]

        tile_at_loc = self.world.listTiles[current_node.row][current_node.col]

        if current_node.name == self.starting_node and tile_at_loc.getStench() and not tile_at_loc.getBreeze():
            self.start_stench = True
            sentence = self.world.get_Adjacents(current_node.row, current_node.col)
            for adjecent in sentence:
                self.KB.add(['W' + str(adjecent)])
            self.move.append(('Right', bind.Action.SHOOT))

        elif tile_at_loc.getStench():
            self.KB.add(['~W' + current_node.right])
            self.move.append(('Up', bind.Action.SHOOT))

        elif tile_at_loc.getStench():
            self.KB.add(['~W' + current_node.up])
            self.move.append(('Left', bind.Action.SHOOT))

        elif tile_at_loc.getStench():
            self.KB.add(['~W' + current_node.left])
            self.move.append(('Down', bind.Action.SHOOT))
            self.KB.add(['~W' + current_node.down])
        else:
            self.start_stench = False
            self.clearKB()

        if current_node.name == self.starting_node.name and tile_at_loc.getBreeze():
            self.move.append(bind.Action.CLIMB)







    def clearKB(self):
        remove = []
        for item in self.KB.KB:
            if item[0][0] == 'W' or item[0][1] == 'W':
                remove.append(item)
        for item in remove:
            self.KB.KB.remove(item)

    def handle_breeze(self,current_node):
        sentence = []
        tile_at_loc = self.world.listTiles[current_node.row][current_node.col]
        prefix = ''
        current_prefix = ''
        if tile_at_loc.getBreeze():
            prefix = 'P'
            current_prefix = 'B'
        elif not tile_at_loc.getBreeze():
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
        tile_at_loc = self.world.listTiles[current_node.row][current_node.col]
        prefix = ''
        current_prefix = ''
        if tile_at_loc.getStench():
            prefix = 'W'
            current_prefix = 'S'
        elif not tile_at_loc.getStench():
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
        self.KB.add([current_prefix + current_node.name])

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
                self.move.append(('Right', bind.Action.SHOOT))
        if current_node.up != 'Wall':
            if self.KB.check(['~W'+str(current_node.up)]) and self.KB.check(['~S'+current_node.name]):
                self.move.append(('Up', bind.Action.SHOOT))
        if current_node.left != 'Wall':
            if self.KB.check(['~W'+str(current_node.left)]) and self.KB.check(['~S'+current_node.name]):
                self.move.append(('Left', bind.Action.SHOOT))
        if current_node.down != 'Wall':
            if self.KB.check(['~W'+str(current_node.down)]) and self.KB.check(['~S'+current_node.name]):
                self.move.append(('Down', bind.Action.SHOOT))
