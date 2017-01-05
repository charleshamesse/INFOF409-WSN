import sys

class Node:
    def __init__(self, n, x, y):
        # Position
        self.n = n
        self.x = x
        self.y = y
        self.is_sink = False
        self.hop = sys.maxint
        self.neighbours = []

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

    def update_hop(self, hop):
        if hop < self.hop:
            self.hop = hop
            for n in self.neighbours:
                n.update_hop(hop+1)

'''
def requestToSend(self, node):
    for i in range(n):
        if incidenceMatrix[node][i] == 1:
            node.queue = 0
'''
