import heapq
import bind

class Search:
    def __init__(self,graph,start,goals,visited_states,current_direction):
        self.start = start
        self.goals = goals
        self.visited_states = visited_states
        self.current_direction = current_direction
        self.graph = graph
    def unicost(self):
        frontier = []
        expansion = [[0, self.current_direction, self.start, [self.start]]]
        if self.start in self.goals:
            return [expansion[-1][0], expansion[-1][3]]
        #HEAPQ FIX LATER
        for item in ['RIGHT', 'UP', 'LEFT', 'DOWN']:
            if item == 'RIGHT':
                if self.graph[self.start].right in self.visited_states or self.graph[self.start].right in self.goals:
                    cost = self.movement_cost(self.current_direction, 'RIGHT')
                    heapq.heappush(frontier,(cost, 'RIGHT', self.graph[self.start].right, [self.start] + [self.graph[self.start].right]))
            elif item == 'UP':
                if self.graph[self.start].up in self.visited_states or self.graph[self.start].up in self.goals:
                    cost = self.movement_cost(self.current_direction, 'UP')
                    heapq.heappush(frontier,(cost, 'UP', self.graph[self.start].up, [self.start] + [self.graph[self.start].up]))
            elif item == 'LEFT':
                if self.graph[self.start].left in self.visited_states or self.graph[self.start].left in self.goals:
                    cost = self.movement_cost(self.current_direction, 'LEFT')
                    heapq.heappush(frontier,(cost, 'LEFT', self.graph[self.start].left, [self.start] + [self.graph[self.start].left]))
            elif item == 'DOWN':
                if self.graph[self.start].down in self.visited_states or self.graph[self.start].down in self.goals:
                    cost = self.movement_cost(self.current_direction, 'DOWN')
                    heapq.heappush(frontier,(cost, 'DOWN', self.graph[self.start].down, [self.start] + [self.graph[self.start].down]))
        while True:
            current = heapq.heappop(frontier)
            expansion.append(current)
            if current[2] in self.goals:
                return current[3]
            else:
                for item in ['RIGHT', 'UP', 'LEFT', 'DOWN']:
                    if item == 'RIGHT':
                        if self.graph[current[2]].right in self.visited_states or self.graph[
                            current[2]].right in self.goals:
                            path = current[3] + [self.graph[current[2]].right]
                            cost = self.movement_cost_str(current[1], 'RIGHT') + current[0]
                            heapq.heappush(frontier,(cost, 'RIGHT', self.graph[current[2]].right, path))
                    elif item == 'UP':
                        if self.graph[current[2]].up in self.visited_states or self.graph[current[2]].up in self.goals:
                            path = current[3] + [self.graph[current[2]].up]
                            cost = self.movement_cost_str(current[1], 'UP') + current[0]
                            heapq.heappush(frontier,(cost, 'UP', self.graph[current[2]].up, path))
                    elif item == 'LEFT':
                        if self.graph[current[2]].left in self.visited_states or self.graph[
                            current[2]].left in self.goals:
                            path = current[3] + [self.graph[current[2]].left]
                            cost = self.movement_cost_str(current[1], 'LEFT') + current[0]
                            heapq.heappush(frontier,(cost, 'LEFT', self.graph[current[2]].left, path))
                    elif item == 'DOWN':
                        if self.graph[current[2]].down in self.visited_states or self.graph[
                            current[2]].down in self.goals:
                            path = current[3] + [self.graph[current[2]].down]
                            cost = self.movement_cost_str(current[1], 'DOWN') + current[0]
                            heapq.heappush(frontier,(cost, 'DOWN', self.graph[current[2]].down, path))

            return [expansion[-1][0], expansion[-1][3][1:]]


    def movement_cost(self, current, next):
        if current.name == next:
            return 1
        elif current.name == 'RIGHT':
            if next == 'LEFT':
                return 3
            else:
                return 2
        elif current.name == 'UP':
            if next == 'DOWN':
                return 3
            else:
                return 2
        elif current.name == 'LEFT':
            if next == 'RIGHT':
                return 3
            else:
                return 2
        elif current.name == 'DOWN':
            if next.name == 'UP':
                return 3
            else:
                return 2

    def movement_cost_str(self, current, next):
        if current == next:
            return 1
        elif current == 'RIGHT':
            if next == 'LEFT':
                return 3
            else:
                return 2
        elif current == 'UP':
            if next == 'DOWN':
                return 3
            else:
                return 2
        elif current == 'LEFT':
            if next == 'RIGHT':
                return 3
            else:
                return 2
        elif current == 'DOWN':
            if next == 'UP':
                return 3
            else:
                return 2