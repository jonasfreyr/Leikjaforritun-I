class Class1:
    def __init__(self, obj):
        self.obj = obj

    def print(self):
        print(self.obj.x)

class Class2:
    def __init__(self):
        self.x = 5


g = Class2()

h = Class1(g)

h.print()