import enum

class Action(enum.Enum):
    LEFT    = 1
    UP      = 2
    DOWN    = 3
    RIGHT   = 4
    SHOOT   = 5
    GRAB    = 6
    CLIMB   = 7

class GameState(enum.Enum):
    RUNNING     = 1
    NOT_RUNNING = 2 