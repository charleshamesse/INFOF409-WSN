import sys, random
import numpy as np
from action import Action
from battery import Battery
from message import Message

DEBUG = False

STATES = ['SLEEP', 'AWAKE']
WEIGHTS = [0.2, 0.2, 0.2, 0.2, 0.0]
#IDLE_LSITENING - OVERHEQRING - UNSECCESS -QUEUE - BQTREYRE
LEARNING_RATE = 0.2
MAX_TRIES = 3
MESSAGE_WEIGHT = 1
DUTY_CYCLES = np.arange(0.25,0.80,0.05)
MODE = 'RL'#'RAND' # 'RL' #or

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
        self.messages_to_send = []
        self.number_messages_to_send = 0
        self.messages_to_send_log = 0
        self.current_action = random.randint(0,10)
        self.duty_cycle = DUTY_CYCLES[self.current_action]
        self.actions = {}
        self.tries = 0

        # RL
        self.EE_log = []
        self.ESEE_log = []
        self.ESEE = None
        self.probabilities = np.ones(len(DUTY_CYCLES)) / len(DUTY_CYCLES)

        self.unsuccessful_transmissions = 0
        self.successful_transmissions = 0
        self.latency_log = 0 # sum of durations each packets passed in the queue
        self.idle_listening = 0
        self.messages_to_send_log_total = 0
        self.successful_transmissions_log_total = 0
        self.awake_log = 0
        self.sleep_log = 0

        self.IL = []
        self.OH = []
        self.UT = []
        self.DQ = []

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
        #        for neighbour in self.neighbours:
        WINDOW_LENGTH = 4
        FRAME_LENGTH = 100

        if t > WINDOW_LENGTH*FRAME_LENGTH:
            # Compute ESEE
            id = 1 + WINDOW_LENGTH
            own_EEs = self.EE_log[-id:-1]
            neighbours_EEs = [n.EE_log[-id:-1] for n in self.neighbours]
            Ni = len(neighbours_EEs)
            temp = 0
            #print neighbours_EEs
            #print Ni
            for f in range(WINDOW_LENGTH):
                temp2 = np.sum([neighbours_EEs[n][f] for n in range(Ni)]) # second sum
                temp2 += own_EEs[f]
                temp2 /= Ni + 1
                temp += temp2
            ESEE = (1. / WINDOW_LENGTH )* temp
            #print ESEE
            self.ESEE_log.append(ESEE)

            # Update probabilities
            if MODE == 'RL':
                self.probabilities[self.current_action] += LEARNING_RATE * ESEE * (1 -  self.probabilities[self.current_action])
                for a in range(len(DUTY_CYCLES)):
                    if a != self.current_action:
                        self.probabilities[a] -= LEARNING_RATE * ESEE * self.probabilities[a]

            #if self.n == 0:
            #    print self.probabilities


        if MODE == 'RAND':
            self.duty_cycle = 0.2 #random.choice(DUTY_CYCLES)
        else: # RL
            self.current_action = np.random.choice(len(DUTY_CYCLES), 1, replace=False, p=self.probabilities)[0]
            self.duty_cycle = DUTY_CYCLES[self.current_action]

        if self.is_sink:
            self.duty_cycle = 1

        return True

    def schedule_frame(self, t):
        # Flush logs
        # todo
        self.awake_log = 0
        self.sleep_log = 0
        self.messages_to_send_log = 0
        self.latency_log = 0
        self.successful_transmissions = 0
        self.unsuccessful_transmissions = 0
        self.idle_listening = 0

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
        number_of_messages = 1#random.randint(1,2)
        for m in range(number_of_messages):
            temp = random.randint(0,99)
            actions.append(Action('SENSE', (t + temp), self.add_message))


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
        IL = self.idle_listening*1. / self.awake_log #0.23345
        OH = 0.1  #0.1
        if (self.unsuccessful_transmissions + self.successful_transmissions) > 0:
            denominator = (self.unsuccessful_transmissions + self.successful_transmissions)
        else:
            denominator = 1
        UT = self.unsuccessful_transmissions*1. / denominator #0.254
        DQ = self.latency_log*1. / (3*self.messages_to_send_log)  #0.1
        EE = WEIGHTS[0]*(0.5 - IL) + \
             WEIGHTS[1]*(0.5 - OH) + \
             WEIGHTS[2]*(1 - UT) + \
             WEIGHTS[3]*(1 - DQ) + \
             WEIGHTS[4]*self.battery.battery
        #print 'Activity log: ' + str(self.awake_log) + 'A / '+  str(self.sleep_log) + 'S'
        #print 'Node ' + str(self.n) + ':\t' + str(self.messages_to_send_log)
        #print 'Node ' + str(self.n) + '\tBattery=' + str(self.battery.battery)  +'\tEE = ' + str(EE)
        #if self.n == 10:
        #    print (IL, OH, UT, DQ), 'Node'+str(self.n)
        if t%7 == 0:
            self.IL.append(IL)
            self.OH.append(OH)
            self.UT.append(UT)
            self.DQ.append(DQ)
        # if self.n == 0: print ('Node', self.n, 'Time', t, IL, OH, UT, DQ, 'Action', self.current_action)

        self.EE_log.append(EE)

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
            for idx, action in enumerate(self.actions[t]):
                if self.n ==4:
                    print 'Executing', idx, action.name

                action.execute()
        print 'State is ', self.state
        # Check if there are messages to send
        if self.state is 'AWAKE':
            self.awake_log += 1
            if self.number_messages_to_send== 0:
                self.idle_listening += 1
            if self.number_messages_to_send> 0:
                self.send_message(t, self.messages_to_send[-1])
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
        message = Message('MSG', self.n)
        self.number_messages_to_send += 1
        self.messages_to_send.append(message)
        self.messages_to_send_log += 1
        self.messages_to_send_log_total += 1
        return True

    def send_message(self, t, m):
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
                self.number_messages_to_send-= 1
                self.tries = 0
                self.latency_log += self.tries
                m.transfer('FAIL')
                self.messages_to_send.remove(m)
                self.unsuccessful_transmissions += 1

        # There's some node to send the message
        else:
            self.battery.account('RX') # CTS coming back
            receiver = random.choice(awake_neighbours) #random.randint(0, len(awake_neighbours)-1)
            if not receiver.is_sink:
                receiver.number_messages_to_send+= 1
            receiver.messages_to_send_log += 1
            receiver.messages_to_send_log_total += 1

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

            self.number_messages_to_send-= 1
            m.transfer(receiver.n)
            receiver.messages_to_send.append(m)
            self.messages_to_send.remove(m)
            self.successful_transmissions += 1
            self.successful_transmissions_log_total +=1
            self.latency_log += self.tries
            self.tries = 0

    def get_messages(self):
        return self.messages_to_send
