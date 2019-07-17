class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def multiply(self, num):
        self.x = self.x * num
        self.y = self.y * num