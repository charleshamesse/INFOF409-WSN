import time, sys, random
import numpy as np
from node import Node
from graph import Graph

SIMULATION_LENGTH = 10
WINDOW_LENGTH = 4
FRAME_LENGTH = 10

DEBUG = True

def cout(m):
    if DEBUG:
        print(m)


def main():

    # Init
    graph = Graph(10, 10 ** 16, 4)
    t = 0

    # Routing
    sink = graph.get_sink()
    sink.update_hop(0)

    print graph.incidenceMatrix

    for n in graph.get_nodes():
        print ('node ' + str(n.n) + ', neighbours: ' + str(len(n.neighbours)) + ', hop:' + str(n.hop))


    # Processing
    cout('Starting simulation...')
    for w in range(SIMULATION_LENGTH):
        for f in range(WINDOW_LENGTH):
            for i in range(FRAME_LENGTH):
                #print t
                t += 1
                # call all nodes - update
            # delay?

    cout('End of simulation.')

if __name__ == '__main__':
    main()
