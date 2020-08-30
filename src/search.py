import heapq
from bind import *

class Search:
    def __init__(self, graph, start, goals, visited_states, current_direction):
        self.start = start
        self.goals = goals
        self.visited_states = visited_states
        self.current_direction = current_direction
        self.graph = graph

    def unicost(self):
        frontier = []
        expansion = [[0, self.current_direction, self.start, [self.start]]]
        
        if self.start in self.goals:
            return expansion[-1][3]

        for item in [Action.RIGHT, Action.UP, Action.LEFT, Action.DOWN]:
            if item == Action.RIGHT:
                if self.graph[self.start].right in self.visited_states or self.graph[self.start].right in self.goals:
                    cost = self.movement_cost(self.current_direction, Action.RIGHT)
                    heapq.heappush(frontier,(cost, Action.RIGHT.name, self.graph[self.start].right, [self.start] + [self.graph[self.start].right]))
            elif item == Action.UP:
                if self.graph[self.start].up in self.visited_states or self.graph[self.start].up in self.goals:
                    cost = self.movement_cost(self.current_direction, Action.UP)
                    heapq.heappush(frontier,(cost, Action.UP.name, self.graph[self.start].up, [self.start] + [self.graph[self.start].up]))
            elif item == Action.LEFT:
                if self.graph[self.start].left in self.visited_states or self.graph[self.start].left in self.goals:
                    cost = self.movement_cost(self.current_direction, Action.LEFT)
                    heapq.heappush(frontier,(cost, Action.LEFT.name, self.graph[self.start].left, [self.start] + [self.graph[self.start].left]))
            elif item == Action.DOWN:
                if self.graph[self.start].down in self.visited_states or self.graph[self.start].down in self.goals:
                    cost = self.movement_cost(self.current_direction, Action.DOWN)
                    heapq.heappush(frontier,(cost, Action.DOWN.name, self.graph[self.start].down, [self.start] + [self.graph[self.start].down]))
        while True:
            current = heapq.heappop(frontier)
            expansion.append(current)
            if current[2] in self.goals:
                break
            else:
                for item in [Action.RIGHT, Action.UP, Action.LEFT, Action.DOWN]:
                    if item == Action.RIGHT:
                        if self.graph[current[2]].right in self.visited_states or self.graph[
                            current[2]].right in self.goals:
                            path = current[3] + [self.graph[current[2]].right]
                            cost = self.movement_cost(current[1], Action.RIGHT) + current[0]
                            heapq.heappush(frontier,(cost, Action.RIGHT.name, self.graph[current[2]].right, path))
                    elif item == Action.UP:
                        if self.graph[current[2]].up in self.visited_states or self.graph[current[2]].up in self.goals:
                            path = current[3] + [self.graph[current[2]].up]
                            cost = self.movement_cost(current[1], Action.UP) + current[0]
                            heapq.heappush(frontier,(cost, Action.UP.name, self.graph[current[2]].up, path))
                    elif item == Action.LEFT:
                        if self.graph[current[2]].left in self.visited_states or self.graph[
                            current[2]].left in self.goals:
                            path = current[3] + [self.graph[current[2]].left]
                            cost = self.movement_cost(current[1], Action.LEFT) + current[0]
                            heapq.heappush(frontier,(cost, Action.LEFT.name, self.graph[current[2]].left, path))
                    elif item == Action.DOWN:
                        if self.graph[current[2]].down in self.visited_states or self.graph[
                            current[2]].down in self.goals:
                            path = current[3] + [self.graph[current[2]].down]
                            cost = self.movement_cost(current[1], Action.DOWN) + current[0]
                            heapq.heappush(frontier,(cost, Action.DOWN.name, self.graph[current[2]].down, path))

        return expansion[-1][3][0:]


    def movement_cost(self, current, next):
        if isinstance(current,enum.Enum):
            if int(current.value) == int(next.value):
                return 1
            elif int(current.value) == Action.RIGHT.value:
                if int(next.value) == Action.LEFT.value:
                    return 3
                else:
                    return 2
            elif int(current.value) == Action.UP.value:
                if int(next.value) == Action.DOWN.value:
                    return 3
                else:
                    return 2
            elif int(current.value) == Action.LEFT.value:
                if int(next.value) == Action.RIGHT.value:
                    return 3
                else:
                    return 2
            elif int(current.value) == Action.DOWN.value:
                if int(next.value) == Action.UP.value:
                    return 3
                else:
                    return 2
        elif type(current) is str:
            if current == str(next.name):
                return 1
            elif current == str(Action.RIGHT.name):
                if int(next.value) == int(Action.LEFT.value):
                    return 3
                else:
                    return 2
            elif current == str(Action.UP.name):
                if int(next.value) == int(Action.DOWN.value):
                    return 3
                else:
                    return 2
            elif current == str(Action.LEFT.name):
                if int(next.value) == int(Action.RIGHT.value):
                    return 3
                else:
                    return 2
            elif current == str(Action.DOWN.name):
                if int(next.value) == int(Action.UP.value):
                    return 3
                else:
                    return 2

