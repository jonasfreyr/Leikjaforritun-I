import math

class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __str__(self):
        return str([self.x, self.y, self.width, self.height])

    def get_center(self):
        return Vector(self.x + self.width / 2, self.y + self.height / 2)

    def copy(self):
        return Rect(self.x, self.y, self.width, self.height)

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return Vector(self.x * other.x, self.y * other.y)

    def __str__(self):
        return str([self.x, self.y])

    def copy(self):
        return Vector(self.x, self.y)

    def get_tuple(self):
        return self.x, self.y

    def rotate(self, degrees):
        a = math.radians(degrees)

        cs = math.cos(a)
        sn = math.sin(a)

        px = self.x * cs - self.y * sn
        py = self.x * sn + self.y * cs

        return Vector(px, py)

    def multiply(self, num):
        self.x = self.x * num
        self.y = self.y * num

    def magnitude(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))
