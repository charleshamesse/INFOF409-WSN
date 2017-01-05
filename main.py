import time, sys, random
import numpy as np
from node import Node
from graph import Graph


SIMULATION_LENGTH = 100
WINDOW_LENGTH = 4
FRAME_LENGTH = 100

def main():

    graph = Graph(10, 10 ** 16, 4)

    print graph

    '''
    for w in range(SIMULATION_LENGTH):
        for f in range(WINDOW_LENGTH):
            for i in range(FRAME_LENGTH):
                print (w,f,i)
                # call all nodes - update
            # delay?
    '''

if __name__ == '__main__':
    main()
