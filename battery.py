ACTIONS = {
    'TX': 0.001/5,
    'RX': 0.00035/5,
    'SLEEP': 0.00005/5,
    'AWAKE': 0.0002/5
}

class Battery:
    def __init__(self):
        self.battery = 1

    def account(self, action):
        self.battery = self.battery - ACTIONS[action]
        if self.battery < 0:
            self.battery = 0
