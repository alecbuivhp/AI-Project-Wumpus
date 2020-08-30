import world

class Node():
    def __init__(self, row, col, world):
        self.name = str(row) + ',' + str(col)
        self.row = row
        self.col = col
        adjacents = world.get_Adjacents(row,col)
        self.left = ''
        self.right = ''
        self.up = ''
        self.down = ''
        for adjacent in adjacents:
            if adjacent[0] == row - 1:
                self.up = str(adjacent[0]) + ',' + str(adjacent[1])
            elif adjacent[0] == row + 1:
                self.down = str(adjacent[0]) + ',' + str(adjacent[1])
            elif adjacent[1] == col + 1:
                self.right = str(adjacent[0]) + ',' + str(adjacent[1])
            elif adjacent[1] == col - 1:
                self.left = str(adjacent[0]) + ',' + str(adjacent[1])

class Game_State:
    def __init__(self,world):
        self.visited = []
        self.unvisited_safe = []
        self.state = dict()
        self.max_row= world.height
        self.max_col = world.width

    def add_state(self,node):
        if node.left == '':
            node.left = 'Wall'
        if node.right == '':
            node.right = 'Wall'
        if node.up == '':
            node.up = 'Wall'
        if node.down == '':
            node.down = 'Wall'
        self.state[node.name] = node
        if node.name not in self.visited:
            self.visited.append(node.name)