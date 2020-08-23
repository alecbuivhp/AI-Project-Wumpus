class Node:
    def __init__(self,row,col):
        self.row = row
        self.col = col
        self.name = str(row) + ',' + str(col)
        self.left = ''
        self.right = ''
        self.up = ''
        self.down = ''



class GameState:
    def __init__(self,max_row,max_col):
        self.visited = []
        self.unvisited = []
        self.state = dict()
        self.max_row = max_row
        self.max_col = max_col

    def add_state(self,node):
        #FIX ME LATER
        if node.col == 0:
            node.left = 'Wall'
        else:
            node.left = str(node.row) + ',' + str(node.col-1)

        if node.col == self.max_col:
            node.right = 'Wall'
        else:
            node.right = str(node.row) + ',' + str(node.col+1)

        if node.row == 0:
            node.up = 'Wall'
        else:
            node.up = str(node.row - 1) + ',' + str(node.col)

        if node.row == self.max_row:
            node.down = 'Wall'
        else:
            node.down = str(node.row + 1) + ',' + str(node.col)

        self.state[node.name] = node
        if node.name not in self.visited:
            self.visited.append(node.name)