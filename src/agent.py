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


