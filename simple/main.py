import matplotlib.pyplot as plt
import numpy as np
import random
from node import Node

#
DEBUG = False
NODES = 20
SIMULATIONS = 10
ITERATIONS = 100
DO_SIM = True

#

#
def cout(m):
    if DEBUG:
        print(m)

def get_node(n, nodes):
    if n > -1:
        return nodes[n]
    else:
        return None

def main():
    cout('Generate line')

    results = np.zeros((SIMULATIONS, NODES))


    if DO_SIM:
        for s in range(SIMULATIONS):
            print 'S#\t' + str(s)
            nodes = []
            for n in range(NODES):
                # parent = n-1 if n-1 > -1 else None
                node = Node(n)  # , parent)
                nodes.append(node)

            for i in range(ITERATIONS):
                #print('#\t' + str(i))

                # Sense
                rand = random.randint(0,NODES-1)
                sensing_node = get_node(rand, nodes)
                cout('Node ' + str(sensing_node.n) + ' is sensing')

                # Get needed nodes
                needed_nodes = []
                current_node = sensing_node
                while current_node is not None:
                    needed_nodes.append(current_node)
                    cout('--Message going to node ' + str(current_node.n) + ' - ' + str(current_node.state))
                    current_node = get_node(current_node.n-1, nodes)

                # Apply rewards or penalties - message
                last_node = 0 # correct?
                for n in needed_nodes:
                    if n.state == 'AWAKE':
                        # Reward
                        cout('Rewarding ' + str(n.n))
                        n.reward = 10
                    elif n.state == 'SLEEPING':
                        # Penalty
                        cout('Punishing ' + str(n.n) + ' and end')
                        n.reward = -10
                        last_node = n.n-1
                        #break

                for n in range(rand+1, NODES):
                    node = get_node(n, nodes)
                    if node.state == 'AWAKE':
                        node.reward = -5
                    elif node.state == 'SLEEPING':
                        node.reward = 5

                for n in range(0, last_node):
                    node = get_node(n, nodes)
                    node.reward = 0

                # Apply penalties - battery
                for node in nodes:
                    if node.state == 'AWAKE':
                        node.reward -= 5
                    else:
                        node.reward -= 1


                 # Update probabilities
                for node in nodes:
                    node.reward = node.reward / 10
                    node.update()
                    results[s][node.n] = node.probabilities[0]

            del nodes

    awake_p = np.zeros(NODES)
    for n in range(NODES):
        for s in range(SIMULATIONS):
            awake_p[n] += results[s][n]
        awake_p[n] /= SIMULATIONS

    plt.plot(awake_p)
    print awake_p
    plt.show()


if __name__ == '__main__':
    main()
