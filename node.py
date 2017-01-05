import sys, random
import numpy as np
from action import Action

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
        self.duty_cycle = 0.5


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

    def learn(self, t):
        return True

    def schedule_sleep(self, t):
        FRAME_LENGTH = 100 # to-do: get it from main

        actions = []
        rand = random.randint(0, FRAME_LENGTH)
        sleep_time = FRAME_LENGTH * self.duty_cycle

        start_time = t + rand
        end_time = t + (rand+sleep_time)%FRAME_LENGTH
        actions.append(Action('SLEEP', start_time))
        actions.append(Action('WAKE', end_time))

        # If non compact
        if end_time < start_time:
            actions.append(Action('SLEEP', t))
            actions.append(Action('WAKE', t+FRAME_LENGTH-1))


        for a in actions:
            print a.describe()

        return True

    def update(self, t):
        print 'updating node ' + str(self.n) + ', time:' + str(t)