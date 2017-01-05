import sys


ACTIONS = {
    'RTS': 0.001,
    'CTS': 0.001,
    'ACK': 0.001,
    'SLEEP': 0.0001,
    'AWAKE': 0.0005,
    'MSG': 0.008
}

class Battery:
    def __init__(self):
        self.battery = 1

    def execute(self, action):
        self.battery = self.battery - ACTIONS[action]
