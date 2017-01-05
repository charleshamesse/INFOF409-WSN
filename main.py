import time, sys, random
import numpy as np
from node import Node
from graph import Graph

SIMULATION_LENGTH = 10
WINDOW_LENGTH = 4
FRAME_LENGTH = 10

def main():

    graph = Graph(10, 10 ** 16, 4)
    t = 0

    print graph

    # Routing


    # Processing
    for w in range(SIMULATION_LENGTH):
        for f in range(WINDOW_LENGTH):
            for i in range(FRAME_LENGTH):
                print t
                t += 1
                # call all nodes - update
            # delay?

if __name__ == '__main__':
    main()
