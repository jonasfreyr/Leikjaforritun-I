from vector import Vector
from settings import *

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.neighbors = []

    def line_collide(self, game, pos, o):
        for wall in game.walls:
            topleft = [wall.pos.x, wall.pos.y + wall.height]
            topright = [wall.pos.x + wall.width, wall.pos.y + wall.height]

            bottomleft = [wall.pos.x, wall.pos.y]
            bottomright = [wall.pos.x + wall.width, wall.pos.y]

            left = lineLine(pos.x, pos.y, o.x, o.y, topleft[0], topleft[1], topleft[0], bottomleft[1])

            right = lineLine(pos.x, pos.y, o.x, o.y, topright[0], topright[1], topright[0], bottomright[1])

            top = lineLine(pos.x, pos.y, o.x, o.y, topleft[0], topleft[1], topright[0], topright[1])

            bottom = lineLine(pos.x, pos.y, o.x, o.y, bottomleft[0], bottomleft[1], bottomright[0], bottomright[1])

            if left or right or top or bottom:
                return True

        return False

    def connect(self, nodes, game):
        for node in nodes:
            if not self.line_collide(game, Vector(node.x, node.y), Vector(self.x, self.y)):
                self.neighbors.append(node)


class Queue:
    def __init__(self, game):
        self.list = []

        self.game = game

    def put(self, node, index=None):
        if index is not None:
            self.list.insert(index, node)

        else:
            self.list.append(node)

    def line_collide(self, game, pos, o):
        for wall in game.walls:
            topleft = [wall.pos.x, wall.pos.y + wall.height]
            topright = [wall.pos.x + wall.width, wall.pos.y + wall.height]

            bottomleft = [wall.pos.x, wall.pos.y]
            bottomright = [wall.pos.x + wall.width, wall.pos.y]

            left = lineLine(pos.x, pos.y, o.x, o.y, topleft[0], topleft[1], topleft[0], bottomleft[1])

            right = lineLine(pos.x, pos.y, o.x, o.y, topright[0], topright[1], topright[0], bottomright[1])

            top = lineLine(pos.x, pos.y, o.x, o.y, topleft[0], topleft[1], topright[0], topright[1])

            bottom = lineLine(pos.x, pos.y, o.x, o.y, bottomleft[0], bottomleft[1], bottomright[0], bottomright[1])

            if left or right or top or bottom:
                return True

        return False

    def get_nearest(self, pos):
        nearest = None
        for node in self.list:

            if not self.line_collide(self.game, Vector(node.x, node.y), pos):
                if nearest is None:
                    nearest = node

                elif (Vector(nearest.x, nearest.y) - pos).magnitude() > (Vector(node.x, node.y) - pos).magnitude():
                    nearest = node
        print(nearest)
        return nearest

    def get(self):
        return self.list[len(self.list)-1]

    def test(self):
        pos = Vector(1696.0, 160.0)
        goal = Vector(104.0, 1312.0)
        
        self.find_path(self.get_nearest(pos), self.get_nearest(goal))

    def find_path(self, start, goal):
        self.put(start)

        came_from = dict()
        came_from[start] = None

        while True:
            curr = self.get()

            if curr == goal:
                break

            for next in curr.neighbors:
                if next not in came_from:
                    self.put(next)
                    came_from[next] = curr

        print(self.list)