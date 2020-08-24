import bind

class ManualAgent():
    def __init__(self):
        self.currentState = bind.Action.RIGHT

    def getAction(self, key):
        if key == 'w':
            return bind.Action.UP
            
        if key == 'a':
            return bind.Action.LEFT

        if key == 's':
            return bind.Action.DOWN
            
        if key == 'd':
            return bind.Action.RIGHT
            
        if key == 'f':
            return bind.Action.SHOOT
            
        if key == 'g':
            return bind.Action.GRAB
        
        if key == 'c':
            return bind.Action.CLIMB
        
        return None