import sys



class Action:
    def __init__(self, name, start_time, timespan, end_time):
        self.name = name
        self.start_time = start_time
        self.timespan = timespan
        self.end_time = end_time

    def describe(self):
        return self.name

