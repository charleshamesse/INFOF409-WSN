import sys, random
import numpy as np
from action import Action
from battery import Battery

DEBUG = False

STATES = ['SLEEP', 'AWAKE']
WEIGHTS = [0.2, 0.3, 0.1, 0.3, 0.1]
LEARNING_RATE = 0.28
MAX_TRIES = 3
MESSAGE_WEIGHT = 1
DUTY_CYCLES = np.arange(0,1.1,0.1)
MODE = 'RAND' # 'RL' #or

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
        self.messages_to_send = 0
        self.duty_cycle = random.choice(DUTY_CYCLES)
        self.actions = {}
        self.tries = 0

        # RL
        self.EE_log = []
        self.ESEE = None

        self.unsuccessful_transmissions = 0
        self.successful_transmissions = 0
        self.latency_log = []
        self.messages_to_send_log = 0
        self.awake_log = 0
        self.sleep_log = 0


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
        if MODE == 'RAND':
            self.duty_cycle = 0.2 #random.choice(DUTY_CYCLES)
        else: # RL
            self.duty_cycle = 0 # To-do np.random.choice(3, 1, replace=False, p=[0.1, 0.8, 0.1])

        return True

    def schedule_frame(self, t):
        # Flush logs
        # todo
        self.awake_log =0
        self.sleep_log =0

        FRAME_LENGTH = 100 # to-do: get it from main
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

        # Sensors
        temp = random.randint(0,99)
        actions.append(Action('SENSE', t + temp, self.add_message))

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
        print 'Activity log: ' + str(self.awake_log) + 'A / '+  str(self.sleep_log) + 'S'
        print 'Node ' + str(self.n) + '\tEOF \tBattery=' + str(self.battery.battery)  +'\tEE = ' + str(EE)

    def update(self, t):
        '''
        Called at each frame subdivision
        Watch out: self.actions[t] is a list
        :param t:
        :return:
        '''
        self.battery.account(self.state)

        # Check if there's an action
        if t in self.actions.keys():
            for action in self.actions[t]:
                action.execute()

        # Check if there are messages to send
        if self.state is 'AWAKE':
            self.awake_log += 1
            if self.messages_to_send > 0:
                self.send_message(t)
        else:
            self.sleep_log += 1


    # Actions
    def add_action(self, a):
        if a.time not in self.actions.keys():
            self.actions[a.time] = [a]
        else:
            self.actions[a.time].append(a)

    def start_sleeping(self):
        self.state = 'SLEEP'
        return True

    def stop_sleeping(self):
        self.state = 'AWAKE'
        return True

    def add_message(self):
        self.messages_to_send += 1
        self.messages_to_send_log += 1
        return True

    def send_message(self, t):
        # Get awake neighbours
        self.battery.account('TX') # RTS emission
        awake_neighbours = []
        for neighbour in self.neighbours:
            if neighbour.state == 'AWAKE':
                neighbour.battery.account('RX')  # RTS reception
                # If neighbour is further away, put it to sleep
                if neighbour.hop >= self.hop:
                    temp = False
                    neighbour.add_action(Action('SLEEP', t + 1, self.start_sleeping))
                    for k in range(1, 4):
                        if t+k in neighbour.actions.keys():
                            for a in neighbour.actions[t + k]:
                                if a.name in ['SLEEP']:
                                    temp = True
                                    print 'Sleeping programmed'
                                    print (a.describe(), t)
                    if temp == False:
                        neighbour.add_action(Action('WAKE', t + 3, self.stop_sleeping))

                else:
                    awake_neighbours.append(neighbour)

        # If there isn't any neighbour awake, do it again
        if awake_neighbours == []:
            if self.tries < MAX_TRIES:
                self.tries += 1
            # Else message is lost
            else:
                self.messages_to_send -= 1
                self.tries = 0
                self.latency_log.append(self.tries)
                self.unsuccessful_transmissions += 1

        # There's some node to send the message
        else:
            self.battery.account('RX') # CTS coming back
            receiver = random.choice(awake_neighbours) #random.randint(0, len(awake_neighbours)-1)
            receiver.messages_to_send += 1

            # The receiving node pays a CTS emission
            receiver.battery.account('TX')

            # Everyone else pays a CTS reception
            for neighbour in awake_neighbours:
                if neighbour != receiver:
                    neighbour.battery.account('RX')

            # Now send the message, once for the message, twice for the EE
            for x in range(MESSAGE_WEIGHT):
                self.battery.account('TX')
                receiver.battery.account('RX')

            # Ack
            receiver.battery.account('TX')
            self.battery.account('RX')

            self.messages_to_send -= 1
            self.latency_log.append(self.tries)
            self.tries = 0