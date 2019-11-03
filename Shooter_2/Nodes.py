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
        self.list = {}

        self.game = game

        self.s = None

    def put(self, node, index=0):
        self.list[index] = node

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

    def make_node(self, pos, id):
        n = Node(pos.x, pos.y, id)

        n.connect(self.game.nodes, self.game)

        for next in n.neighbors:
            next.neighbors.append(n)

        return n

    def del_node(self, node):
        for next in node.neighbors:
            next.neighbors.remove(node)

        del node

    def get(self):
        p = min(self.list)

        c = self.list[p]

        del self.list[p]

        return c

    def draw_path(self, nodes):
        glBegin(GL_LINES)
        glColor3f(1, 0, 0)

        prev = nodes[0]

        for node in nodes[1:]:
            glVertex2i(int(prev.x), int(prev.y))
            glVertex2i(int(node.x), int(node.y))

            prev = node

        glColor3f(1, 1, 1)
        glEnd()

    def draw(self):
        if self.s is not None:
            self.draw_path(self.s)

    def heuristic(self, a, b):
        # Manhattan distance on a square grid
        return abs(a.x - b.x) + abs(a.y - b.y)

    def get_cost(self, node, node2):
        return (Vector(node.x ,node.y) - Vector(node2.x, node2.y)).magnitude()

    def find_path(self, start, goal):
        self.goal = goal.copy()
        self.pos = start.copy()

        start = self.make_node(start, "start")
        goal = self.make_node(goal, "goal")

        self.list = {}

        self.put(start)

        came_from = dict()
        cost_so_far = dict()

        came_from[start] = None
        cost_so_far[start] = 0

        while len(self.list) > 0:
            curr = self.get()

            if curr == goal:
                break

            for next in curr.neighbors:
                new_cost = cost_so_far[curr] + self.get_cost(curr, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    p = new_cost + self.heuristic(goal, next)
                    # print(p)
                    self.put(next, int(p))
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

        self.del_node(start)
        self.del_node(goal)

        self.s = path
