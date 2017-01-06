ACTIONS = {
    'TX': 0.00001,
    'RX': 0.00001,
    'SLEEP': 0.000005,
    'AWAKE': 0.00002
}

class Battery:
    def __init__(self):
        self.battery = 1

    def account(self, action):
        self.battery = self.battery - ACTIONS[action]
        if self.battery < 0:
            self.battery = 0
