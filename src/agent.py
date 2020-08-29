import gamestate
import kb
import bind
import world
from src.search import *

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
        if self.current_direction == bind.Action.LEFT and state[self.current_state].left != 'Wall':
            self.current_state = state[self.current_state].left
        elif self.current_direction == bind.Action.RIGHT and state[self.current_state].right != 'Wall':
            self.current_state = state[self.current_state].right
        elif self.current_direction == bind.Action.UP and state[self.current_state].up != 'Wall':
            self.current_state = state[self.current_state].up
        elif self.current_direction == bind.Action.DOWN and state[self.current_state].down != 'Wall':
            self.current_state = state[self.current_state].down

    def move(self,Node, world):
        row, col = Node.split(',')
        new_state = gamestate.Node(int(row), int(col), world)
        self.current_state.add_state(new_state)
        self.current_state = self.current_state[Node]


    def turn_left(self):
        self.current_direction = bind.Action.LEFT

    def turn_right(self):
        self.current_direction = bind.Action.RIGHT

    def turn_up(self):
        self.current_direction = bind.Action.UP

    def turn_down(self):
        self.current_direction = bind.Action.DOWN


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
        self.killing_wumpus = False
        self.itter = 0

    def getAction(self):
        current_node = self.state.state[self.agent.current_state]
        tile_at_loc = self.world.listTiles[current_node.row][current_node.col]
        if current_node.name in self.state.unvisited_safe:
            self.state.unvisited_safe.remove(current_node.name)
        print("visited = " ,self.state.visited)
        print("unvisited = ", self.state.unvisited_safe)
        print("current_node =", self.agent.current_state)

        # if current_node.name == self.starting_node.name and tile_at_loc.getStench() and (not tile_at_loc.getBreeze()) and (self.itter == 0):
        #     self.start_stench = True
        #     self.handle_stench(current_node)
        #     if current_node.right != 'Wall':
        #         self.kill_wumpus('Right')
        #         self.state.unvisited_safe.append(current_node.right)
        # if current_node.name == self.starting_node.name and tile_at_loc.getStench() and (not tile_at_loc.getBreeze()) and (self.itter == 1):
        #     self.start_stench = True
        #     self.handle_stench(current_node)
        #     if current_node.up != 'Wall':
        #         self.kill_wumpus('Up')
        #         self.state.unvisited_safe.append(current_node.up)
        # if current_node.name == self.starting_node.name and tile_at_loc.getStench() and (not tile_at_loc.getBreeze()) and (self.itter == 2):
        #     self.start_stench = True
        #     self.handle_stench(current_node)
        #     if current_node.left != 'Wall':
        #         self.kill_wumpus('Left')
        #         self.state.unvisited_safe.append(current_node.left)
        # if current_node.name == self.starting_node.name and tile_at_loc.getStench() and (not tile_at_loc.getBreeze()) and (self.itter == 3):
        #     self.start_stench = True
        #     self.handle_stench(current_node)
        #     if current_node.down != 'Wall':
        #         self.kill_wumpus('Down')
        #         self.state.unvisited_safe.append(current_node.down)
        # self.itter += 1
        if current_node.name == self.starting_node.name and tile_at_loc.getBreeze():
            self.move.append(bind.Action.CLIMB)
        if not self.exit and not self.killing_wumpus:
            if tile_at_loc.getStench():
                self.handle_stench(current_node)
                self.check_wumpus(current_node)
            elif not tile_at_loc.getStench():
                self.handle_no_stench(current_node)
            if tile_at_loc.getBreeze():
                self.handle_breeze(current_node)
            elif not tile_at_loc.getBreeze():
                self.handle_no_breeze(current_node)
            self.check_safe(current_node)
            if tile_at_loc.getGold():
                return bind.Action.GRAB
            if not self.killing_wumpus:
                if len(self.state.unvisited_safe) > 0:
                    search = Search(self.state.state, self.agent.current_state,self.state.unvisited_safe[-1:], self.state.visited,self.agent.current_direction)
                    cost_path = search.unicost()
                    self.move = self.move_list(cost_path)
                else:
                    self.exit = True
                    search = Search(self.state.state, self.agent.current_state, self.starting_node.name, self.state.visited, self.agent.current_direction)
                    cost_path = search.unicost()
                    self.move = self.move_list(cost_path)
        if self.move:
            move = self.move.pop(0)
            if move == bind.Action.SHOOT:
                self.killing_wumpus = False
                self.clearKB()
            return move


    def clearKB(self):
        remove = []
        for item in self.KB.KB:
            if item[0][0] == 'W' or item[0][1] == 'W':
                remove.append(item)
        for item in remove:
            self.KB.KB.remove(item)

    def handle_breeze(self,current_node):
        sentence = []
        prefix = 'P'
        current_prefix = 'B'
        if current_node.right not in self.state.visited and current_node.right != 'Wall':
            sentence.append(prefix + current_node.right)
        if current_node.up not in self.state.visited and current_node.up != 'Wall':
            sentence.append(prefix + current_node.up)
        if current_node.left not in self.state.visited and current_node.left != 'Wall':
            sentence.append(prefix + current_node.left)
        if current_node.down not in self.state.visited and current_node.down != 'Wall':
            sentence.append(prefix + current_node.down)
        self.KB.add(sentence)
        self.KB.add([current_prefix + current_node.name])

    def handle_stench(self,current_node):
        sentence = []
        prefix = 'W'
        current_prefix = 'S'
        if current_node.right not in self.state.visited and current_node.right != 'Wall':
            sentence.append(prefix + current_node.right)
        if current_node.up not in self.state.visited and current_node.up != 'Wall':
            sentence.append(prefix + current_node.up)
        if current_node.left not in self.state.visited and current_node.left != 'Wall':
            sentence.append(prefix + current_node.left)
        if current_node.down not in self.state.visited and current_node.down != 'Wall':
            sentence.append(prefix + current_node.down)
        self.KB.add(sentence)
        self.KB.add([current_prefix + current_node.name])
###################################
    def handle_no_stench(self, current_node):
        prefix = '~W'
        if current_node.right not in self.state.visited and current_node.right != 'Wall':
            self.KB.add([prefix + current_node.right])
        if current_node.up not in self.state.visited and current_node.up != 'Wall':
            self.KB.add([prefix + current_node.up])
        if current_node.left not in self.state.visited and current_node.left != 'Wall':
            self.KB.add([prefix + current_node.left])
        if current_node.down not in self.state.visited and current_node.down != 'Wall':
            self.KB.add([prefix + current_node.down])

    def handle_no_breeze(self,current_node):
        prefix = '~P'
        if current_node.right not in self.state.visited and current_node.right != 'Wall':
            self.KB.add([prefix + current_node.right])
        if current_node.up not in self.state.visited and current_node.up != 'Wall':
            self.KB.add([prefix + current_node.up])
        if current_node.left not in self.state.visited and current_node.left != 'Wall':
            self.KB.add([prefix + current_node.left])
        if current_node.down not in self.state.visited and current_node.down != 'Wall':
            self.KB.add([prefix + current_node.down])
#####################################

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
#####################################
    def check_wumpus(self, current_node):
        row = current_node.row
        col = current_node.col
        if current_node.right != "Wall":
            if (self.KB.check(["W" + str(row - 1) + "," + str(col)]) and self.KB.check(["S" + str(row - 1) + "," + str(col - 1)])) or (self.KB.check(["W" + str(row + 1) + "," + str(col)]) and self.KB.check(["S" + str(row + 1) + "," + str(col - 1)])):
                self.kill_wumpus("Right")
        if current_node.down != "Wall":
            if (self.KB.check(["W" + str(row) + "," + str(col - 1)]) and self.KB.check(["~S" + str(row + 1) + "," + str(col - 1)])) or (self.KB.check(["W" + str(row) + "," + str(col + 1)]) and self.KB.check(["~S" + str(row + 1) + "," + str(col + 1)])):
                self.kill_wumpus("Down")
        if current_node.left != "Wall":
            if (self.KB.check(["W" + str(row - 1) + "," + str(col)]) and self.KB.check(["~S" + str(row - 1) + "," + str(col - 1)])) or (self.KB.check(["W" + str(row + 1) + "," + str(col)]) and self.KB.check(["~S" + str(row + 1) + "," + str(col - 1)])):
                self.kill_wumpus("Left")
        if current_node.up != "Wall":
            if (self.KB.check(["W" + str(row) + "," + str(col - 1)]) and self.KB.check(["~S" + str(row - 1) + "," + str(col - 1)])) or (self.KB.check(["W" + str(row) + "," + str(col + 1)]) and self.KB.check(["~S" + str(row - 1) + "," + str(col + 1)])):
                self.kill_wumpus("Up")

    def kill_wumpus(self, direction):
        self.killing_wumpus = True
        self.move = []
        if direction == 'Right':
            if self.agent.current_direction == bind.Action.RIGHT:
                self.move.insert(0, bind.Action.SHOOT)
            elif self.agent.current_direction != bind.Action.RIGHT:
                self.agent.current_direction = bind.Action.RIGHT
                self.move.insert(0, bind.Action.SHOOT)
                self.move.insert(0, bind.Action.RIGHT)
        elif direction == 'Up':
            if self.agent.current_direction == bind.Action.UP:
                self.move.insert(0, bind.Action.SHOOT)
            elif self.agent.current_direction != bind.Action.UP:
                self.agent.current_direction = bind.Action.UP
                self.move.insert(0, bind.Action.SHOOT)
                self.move.insert(0, bind.Action.UP)
        elif direction == 'Left':
            if self.agent.current_direction == bind.Action.LEFT:
                self.move.insert(0, bind.Action.SHOOT)
            elif self.agent.current_direction != bind.Action.LEFT:
                self.agent.current_direction = bind.Action.LEFT
                self.move.insert(0, bind.Action.SHOOT)
                self.move.insert(0, bind.Action.LEFT)
        elif direction == 'Down':
            if self.agent.current_direction == bind.Action.DOWN:
                self.move.insert(0, bind.Action.SHOOT)
            elif self.agent.current_direction != bind.Action.DOWN:
                self.agent.current_direction = bind.Action.DOWN
                self.move.insert(0, bind.Action.SHOOT)
                self.move.insert(0, bind.Action.DOWN)
######################################
    def move_list(self,path):
        direction = self.agent.current_direction
        state = self.agent.current_state
        current_node = self.state.state[state]
        move_list = []
        for item in path:
            row, col = item.split(',')
            new_state = gamestate.Node(int(row), int(col), self.world)
            self.state.add_state(new_state)
            # if item in self.state.unvisited_safe and item in self.state.visited:
            #     self.state.unvisited_safe.remove(item)
            if str(direction.name) == str(bind.Action.RIGHT.name):
                if item == current_node.right:
                    move_list.append(bind.Action.RIGHT)
                    current_node = self.state.state[current_node.right]
                elif item == current_node.up:
                    move_list.append(bind.Action.UP)
                    move_list.append(bind.Action.UP)
                    direction = bind.Action.UP
                    current_node = self.state.state[current_node.up]
                elif item == current_node.down:
                    move_list.append(bind.Action.DOWN)
                    move_list.append(bind.Action.DOWN)
                    direction = bind.Action.DOWN
                    current_node = self.state.state[current_node.down]
                elif item == current_node.left:
                    move_list.append(bind.Action.LEFT)
                    move_list.append(bind.Action.LEFT)
                    direction = bind.Action.LEFT
                    current_node = self.state.state[current_node.left]
            elif str(direction.name) == str(bind.Action.UP.name):
                if item == current_node.right:
                    move_list.append(bind.Action.RIGHT)
                    move_list.append(bind.Action.RIGHT)
                    direction = bind.Action.RIGHT
                    current_node = self.state.state[current_node.right]
                elif item == current_node.up:
                    move_list.append(bind.Action.UP)
                    current_node = self.state.state[current_node.up]
                elif item == current_node.down:
                    move_list.append(bind.Action.DOWN)
                    move_list.append(bind.Action.DOWN)
                    direction = bind.Action.DOWN
                    current_node = self.state.state[current_node.down]
                elif item == current_node.left:
                    move_list.append(bind.Action.LEFT)
                    move_list.append(bind.Action.LEFT)
                    direction = bind.Action.LEFT
                    current_node = self.state.state[current_node.left]
            elif str(direction.name) == str(bind.Action.LEFT.name):
                if item == current_node.right:
                    move_list.append(bind.Action.RIGHT)
                    move_list.append(bind.Action.RIGHT)
                    direction = bind.Action.RIGHT
                    current_node = self.state.state[current_node.right]
                elif item == current_node.up:
                    move_list.append(bind.Action.UP)
                    move_list.append(bind.Action.UP)
                    direction = bind.Action.UP
                    current_node = self.state.state[current_node.up]
                elif item == current_node.down:
                    move_list.append(bind.Action.DOWN)
                    move_list.append(bind.Action.DOWN)
                    direction = bind.Action.DOWN
                    current_node = self.state.state[current_node.down]
                elif item == current_node.left:
                    move_list.append(bind.Action.LEFT)
                    current_node = self.state.state[current_node.left]
            elif str(direction.name) == str(bind.Action.DOWN.name):
                if item == current_node.right:
                    move_list.append(bind.Action.RIGHT)
                    move_list.append(bind.Action.RIGHT)
                    direction = bind.Action.RIGHT
                    current_node = self.state.state[current_node.right]
                elif item == current_node.up:
                    move_list.append(bind.Action.UP)
                    move_list.append(bind.Action.UP)
                    direction = bind.Action.UP
                    current_node = self.state.state[current_node.up]
                elif item == current_node.down:
                    move_list.append(bind.Action.DOWN)
                    current_node = self.state.state[current_node.down]
                elif item == current_node.left:
                    move_list.append(bind.Action.LEFT)
                    move_list.append(bind.Action.LEFT)
                    direction = bind.Action.LEFT
                    current_node = self.state.state[current_node.left]

        if self.exit:
            move_list.append(bind.Action.CLIMB)
        if self.agent.current_direction != move_list[0]:
            self.agent.current_direction = move_list[0]
        else:
            self.agent.move_foward(self.state.state)
        return move_list
##########################################
    def walk(self):
        self.agent.move_foward(self.state.state)
        row_col = self.agent.current_state.split(",")
        state = gamestate.Node(int(row_col[0]), int(row_col[1]),self.world)
        self.state.add_state(state)