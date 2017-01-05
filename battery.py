ACTIONS = {
    'TX': 0.001,
    'RX': 0.00035,
    'SLEEP': 0.00005,
    'AWAKE': 0.0002
}

class Battery:
    def __init__(self):
        self.battery = 1

    def account(self, action):
        self.battery = self.battery - ACTIONS[action]
        if self.battery < 0:
            self.battery = 0
