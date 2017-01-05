import sys, random
import numpy as np
from action import Action
from battery import Battery

DEBUG = False

STATES = ['SLEEP', 'AWAKE']
SLEEPS = np.arange(0, 110, 10)
WEIGHTS = [0.2, 0.3, 0.1, 0.3, 0.1]
LEARNING_RATE = 0.28

class Node(object):
    def __init__(self, n, x, y):
        # Position
        self.n = n
        self.x = x
        self.y = y
        self.is_sink = False
        self.hop = sys.maxint
        self.neighbours = []
        self.battery = Battery()


        # Behaviour
        self.state = 'SLEEP'
        self.sensors = 0
        self.duty_cycle = random.uniform(0, 1.0)


        self.actions = {}
        self.ongoing_actions = []
        self.previous_actions = []

        # RL
        self.EE_log = []
        self.ESEE = None

        self.sleep_probabilities = [1.0/len(SLEEPS)]*11

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
        '''
        Called at each end of frame window.
        - Compute EESE
        - Update probabilities
        :param t:
        :return:
        '''
        return True

    def schedule_sleep(self, t):
        FRAME_LENGTH = 10 # to-do: get it from main
        actions = []

        # Time managment
        rand = random.randint(0, FRAME_LENGTH)
        sleep_time = FRAME_LENGTH * (1-self.duty_cycle)
        start_time = int(t + rand)
        end_time = int(t + (rand+sleep_time)%FRAME_LENGTH)

        # Actions
        actions.append(Action('SLEEP', start_time, self.start_sleeping))
        actions.append(Action('WAKE', end_time, self.stop_sleeping))

        # Actions - if non compact
        if end_time < start_time:
            actions.append(Action('SLEEP', t, self.start_sleeping))
            actions.append(Action('WAKE', t+FRAME_LENGTH-1, self.stop_sleeping))

        # Add actions to node
        for a in actions:
            if a.time not in self.actions.keys():
                self.actions[a.time] = [a]
            else:
                self.actions[a.time].append(a)


    def compute_ee(self, t):
        '''
        Called at each end of frame
        :param t:
        :return:
        '''
        IL = 0.23345
        OH = 0.1
        UT = 0.254
        DQ = 0.1
        EE = WEIGHTS[0]*(1 - IL) + \
             WEIGHTS[1]*(1 - OH) + \
             WEIGHTS[2]*(1 - UT) + \
             WEIGHTS[3]*(1 - DQ) + \
             WEIGHTS[4]*self.battery.battery

        print 'Node ' + str(self.n) + '\tEOF \tBattery=' + str(self.battery.battery)  +'\tEE = ' + str(EE)

    def update(self, t):
        '''
        Called at each frame subdivision
        Watch out: self.actions[t] is a list
        :param t:
        :return:
        '''
        self.battery.account(self.state)
        #print self.state
        if t in self.actions.keys():
            for action in self.actions[t]:
                action.execute()

        #print 'updating node ' + str(self.n) + ', time:' + str(t)

    # Actions
    def start_sleeping(self):
        self.state = 'SLEEP'
        return True

    def stop_sleeping(self):
        self.state = 'AWAKE'
        return True