import time, sys, random
import numpy as np
from node import Node
from graph import Graph

SIMULATION_LENGTH = 2
WINDOW_LENGTH = 4
FRAME_LENGTH = 10

DEBUG = True

def cout(m):
    if DEBUG:
        print(m)


def main():

    '''
    First, generate the graph. The routing (assigning hop values) is already done during the graph generation.
    '''
    cout('Generating graph..')
    graph = Graph(10, 10 ** 12, 4)
    t = 0

    cout(['node ' + str(n.n) + ', neighbours: ' + str(len(n.neighbours)) + ', hop:' + str(n.hop) for n in graph.get_nodes()])

    for n in graph.get_nodes():
        print n.battery.battery

    # Processing
    cout('Starting simulation...')
    for w in range(SIMULATION_LENGTH):
        cout('WINDOW')
        # Learn
        for n in graph.get_nodes():
            n.learn(t)

        for f in range(WINDOW_LENGTH):
            cout('FRAME')
            # Schedule sleep
            for n in graph.get_nodes():
                n.schedule_sleep(t)

            for i in range(FRAME_LENGTH):
                print t
                # Update nodes
                for n in graph.get_nodes():
                    n.update(t)
                t += 1

            # Compute EE
            for n in graph.get_nodes():
                n.compute_ee(t)

                # delay?

    cout('End of simulation.')

if __name__ == '__main__':
    main()
