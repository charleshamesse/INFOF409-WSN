from graph import Graph
import matplotlib.pyplot as plt
import numpy as np

SIMULATION_LENGTH = 50
WINDOW_LENGTH = 4
FRAME_LENGTH = 100
NODES = 20
DEGREE = 4
DISCRETISATION = 10 ** 16

DEBUG = True

def cout(m):
    if DEBUG:
        print(m)

def main():
    '''
    First, generate the graph. The routing (assigning hop values) is already done during the graph generation.
    '''
    cout('Generating graph..')
    graph = Graph(NODES, DISCRETISATION, DEGREE)
    t = 0

    cout(['node ' + str(n.n) + ', neighbours: ' + str(len(n.neighbours)) + ', hop:' + str(n.hop) for n in graph.get_nodes()])


    # Processing
    cout('Starting simulation...')
    for w in range(SIMULATION_LENGTH):
        #cout('WINDOW')
        # Learn
        for n in graph.get_nodes():
            n.learn(t)

        for f in range(WINDOW_LENGTH):

            #print t
            #cout('FRAME')
            # Schedule sleep
            for n in graph.get_nodes():
                n.schedule_frame(t)

            for i in range(FRAME_LENGTH):
                # Update nodes
                for n in graph.get_nodes():
                    n.update(t)
                t += 1

            # Compute EE
            for n in graph.get_nodes():
                n.compute_ee(t)

                # delay?

    cout('End of simulation.')

    mean = []
        #print 'Node ' +  str(n.n) + '\t Last action:' + str(n.current_action)
        #print n.ESEE_log
    for s in range(SIMULATION_LENGTH-12):
        mean.append(0)
        for n in graph.get_nodes():
            mean[s] +=  n.ESEE_log[s]
        mean[s] /= NODES
        #plt.plot( np.arange(len(n.probabilities)), [1.0/11]*11)
        #plt.plot( np.arange(len(n.probabilities)), n.probabilities)
    plt.plot(mean)
    plt.xlabel('RANDOM, QUEUE')
    plt.show()

if __name__ == '__main__':
    main()
