import sys



class Action:
    def __init__(self, name, time):
        self.name = name
        self.time = time

    def describe(self):
        return self.name

