class Node:
    def __init__(self, x, y):
        # Position
        self.x = x
        self.y = y
        self.is_sink = False
        self.hop = 0

        # Behaviour
        self.active = True
        self.pending_actions = []
        self.ongoing_actions = []
        self.previous_actions = []

        # RL
        self.EE_log = []
        self.probabilities = []

    def make_sink(self):
        self.is_sink = True



'''
def requestToSend(self, node):
    for i in range(n):
        if incidenceMatrix[node][i] == 1:
            node.queue = 0
'''
