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

    def connect(self, nodes):
        pass


class Queue:
    def __init__(self):
        self.list = []

    def put(self, node, index):
        self.list.insert(index, node)

    def get(self):
        return self.list[len(self.list)-1]

