import random
import numpy as np

STATES = ['AWAKE', 'SLEEPING']

LEARNING_RATE = 0.003
class Node:

    def __init__(self, n):
        self.n = n
        self.state = random.choice(STATES)
        self.probabilities = [0.5, 0.5]
        self.reward = 0

    def act(self):
        self.state = np.random.choice(STATES, 1, replace=False, p=self.probabilities)

    def update(self):
        if self.state == STATES[0]:
            current_state = 0
            other_state = 1
        else:
            current_state = 1
            other_state = 0

        self.probabilities[current_state] += LEARNING_RATE * self.reward * (1 - self.probabilities[current_state])
        self.probabilities[other_state] -= LEARNING_RATE * self.reward * self.probabilities[other_state]

        #print self.probabilities