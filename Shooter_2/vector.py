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

    def get_angle(self):
        return math.atan2(self.x, self.y)*180/math.pi

    def angle_to(self, vector):
        upper = self.x * vector.x + self.y * vector.y
        lower = self.magnitude() * vector.magnitude()

        s = upper / lower

        return math.acos(s)*180/math.pi

    def set_length(self, length):
        s = Vector(1, 0)

        a = s.get_angle() - self.get_angle()

        s = s.rotate(a)

        s.multiply(length)

        self.x = s.x
        self.y = s.y
s = Vector(0, 5)
print(s.angle_to(Vector(1, 0)))
s = Vector(5, 5)
print(s.angle_to(Vector(1, 0)))
s = Vector(5, 0)
print(s.angle_to(Vector(1, 0)))
s = Vector(0, -5)
print(s.angle_to(Vector(1, 0)))