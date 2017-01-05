import sys

DEBUG = False

def cout(m):
    if DEBUG:
        print(m)


class Action:
    def __init__(self, name, time, callback):
        self.name = name
        self.time = time
        self.priority = 0 # for further use ?
        self.callback = callback

    def describe(self):
        return self.name + ': starting at t = ' + str(self.time)

    def execute(self):
        cout('Executing ' + self.describe())
        return self.callback()