from graph import Graph

SIMULATION_LENGTH = 2
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

            print t
            cout('FRAME')
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

if __name__ == '__main__':
    main()
