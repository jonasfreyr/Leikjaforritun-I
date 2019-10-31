from vector import Vector
from settings import *
import math
import pyglet
from pyglet.gl import *

class Node:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y

        self.neighbors = []
        self.id = id

        self.s = pyglet.text.Label(str(id), x=x, y=y)
        self.s.anchor_x = "center"
        self.s.anchor_y = "center"
        self.s.color = (0, 0, 0, 255)

    def __str__(self):
        return str(self.id)

    def line_collide(self, game, pos, o):
        for wall in game.walls:
            topleft = [wall.pos.x, wall.pos.y + wall.height]
            topright = [wall.pos.x + wall.width, wall.pos.y + wall.height]

            bottomleft = [wall.pos.x, wall.pos.y]
            bottomright = [wall.pos.x + wall.width, wall.pos.y]
            # x1, y1, x2, y2, x3, y3, x4, y4
            left = lineLine(pos.x, pos.y, o.x, o.y, topleft[0], topleft[1], bottomleft[0], bottomleft[1])

            right = lineLine(pos.x, pos.y, o.x, o.y, topright[0], topright[1], bottomright[0], bottomright[1])

            top = lineLine(pos.x, pos.y, o.x, o.y, topleft[0], topleft[1], topright[0], topright[1])

            bottom = lineLine(pos.x, pos.y, o.x, o.y, bottomleft[0], bottomleft[1], bottomright[0], bottomright[1])

            if left or right or top or bottom:
                return True

        return False

    def connect(self, nodes, game):
        for node in nodes:
            if node != self:
                if not self.line_collide(game, Vector(self.x, self.y), Vector(node.x, node.y)):
                    self.neighbors.append(node)

    def draw(self):
        circle(self.x, self.y, 10)

        glBegin(GL_LINES)
        for node in self.neighbors:


            glVertex2i(int(self.x), int(self.y))
            glVertex2i(int(node.x), int(node.y))


        glEnd()

        self.s.draw()

def circle(x, y, radius):
    """
    We want a pixel perfect circle. To get one,
    we have to approximate it densely with triangles.
    Each triangle thinner than a pixel is enough
    to do it. Sin and cosine are calculated once
    and then used repeatedly to rotate the vector.
    I dropped 10 iterations intentionally for fun.
    """
    iterations = int(2*radius*math.pi)
    s = math.sin(2*math.pi / iterations)
    c = math.cos(2*math.pi / iterations)

    dx, dy = radius, 0

    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    for i in range(iterations+1):
        glVertex2f(x+dx, y+dy)
        dx, dy = (dx*c - dy*s), (dy*c + dx*s)
    glEnd()

class Queue:
    def __init__(self, game):
        self.list = []

        self.game = game

        self.goal_line = None
        self.start_line = None

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

            left = lineLine(pos.x, pos.y, o.x, o.y, topleft[0], topleft[1], bottomleft[0], bottomleft[1])

            right = lineLine(pos.x, pos.y, o.x, o.y, topright[0], topright[1], bottomright[0], bottomright[1])

            top = lineLine(pos.x, pos.y, o.x, o.y, topleft[0], topleft[1], topright[0], topright[1])

            bottom = lineLine(pos.x, pos.y, o.x, o.y, bottomleft[0], bottomleft[1], bottomright[0], bottomright[1])

            if left or right or top or bottom:
                return True

        return False

    def get_nearest(self, pos):
        nearest = None
        for node in self.game.nodes:
            if not self.line_collide(self.game, Vector(node.x, node.y), pos):
                if nearest is None:
                    nearest = node

                elif (Vector(nearest.x, nearest.y) - pos).magnitude() > (Vector(node.x, node.y) - pos).magnitude():
                    nearest = node
        return nearest

    def get(self):
        p = self.list[len(self.list)-1]
        self.list.remove(p)
        return p

    def test(self):
        self.pos = Vector(1696.0, 160.0)
        self.goal = Vector(104.0, 1312.0)

        nearest_goal = self.get_nearest(self.goal)
        nearest_start = self.get_nearest(self.pos)

        self.goal_line = [self.goal.x, self.goal.y, nearest_goal.x, nearest_goal.y]
        self.start_line = [self.pos.x, self.pos.y, nearest_start.x, nearest_start.y]

        s = self.find_path(self.get_nearest(self.pos), self.get_nearest(self.goal))

        for node in s:
            print(node)

    def draw(self):
        circle(self.pos.x, self.pos.y, 10)
        circle(self.goal.x, self.goal.y, 10)

        glBegin(GL_LINES)
        glVertex2i(int(self.goal_line[0]), int(self.goal_line[1]))
        glVertex2i(int(self.goal_line[2]), int(self.goal_line[3]))

        glVertex2i(int(self.start_line[0]), int(self.start_line[1]))
        glVertex2i(int(self.start_line[2]), int(self.start_line[3]))

        glEnd()

    def find_path(self, start, goal):
        self.put(start)

        came_from = dict()
        came_from[start] = None
        while len(self.list) > 0:
            curr = self.get()

            # print(self.list)

            if curr == goal:
                break

            for next in curr.neighbors:
                if next not in came_from:
                    self.put(next)
                    came_from[next] = curr
        else:
            print("Goal and Start cannot be none")

        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)  # optional
        path.reverse()  # optional

        return path
