import sys
from Queue import Queue

STATES = ['sleep', 'awake', 'rtc_wait', 'cts_wait']
SLEEPS = np.arange(0, 110, 10)

class Node(object):
    def __init__(self, n, x, y):
        # Position
        self.n = n
        self.x = x
        self.y = y
        self.is_sink = False
        self.hop = sys.maxint
        self.neighbours = []


        # Behaviour
        self.state = None
        self.sensors = 0
        self.sleep_offset = -1
        self.sleep_counter = -1


        self.pending_actions = []
        self.ongoing_actions = []
        self.previous_actions = []

        # RL
        self.EE_log = []
        self.ESEE = None

        self.sleep_probabilities = [1.0/len(SLEEPS)]*11

        self.BL = 1.0
        self.IL = np.zeros(4)
        self.OH = np.zeros(4)
        self.UT = np.zeros(4)
        self.DQ = np.zeros(4)

    def make_sink(self):
        self.is_sink = True

    def update_hop(self, hop):
        if hop < self.hop:
            self.hop = hop
            for n in self.neighbours:
                n.update_hop(hop+1)

    def update_states(self):
        if self.state == 'sleep':
            #
            self.sleep_counter -= 1
            if self.sleep_counter == 0:
                self.state = 'awake'


        if self.state == 'awake':
            #

        if self.state == 'rtc_wait':
            #
        if self.state == 'cts_wait':
            #
'''
def requestToSend(self, node):
    for i in range(n):
        if incidenceMatrix[node][i] == 1:
            node.queue = 0
'''
