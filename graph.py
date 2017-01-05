import random, sys
from math import sqrt
from math import pi
from node import Node
import numpy as np

class Graph:

    def __init__(self, n, p, d):
        (self.nodes, self.incidenceMatrix, self.range) = self.get_graph(n, p, d)
        self.sink = self.nodes[0]

    def randomGraph(self, n, p):
        '''
        Makes a random graph
        :param n: number of nodes
        :param p: discretisation level
        :return: tuple with nodes, graph and radius
        '''
        # Create nodes
        nodes = []
        for i in range(n):
            nodes.append(Node(i, random.randint(0,p)*1./p, random.randint(0,p)*1./p))

        # Define maximum adjacency radius
        r = sqrt(4/(n*pi)) # Radius should be approximately this value, because pi*n*r^2 = 4 (average degree of a node)

        # Compute incidence matrix
        graph = np.zeros((n,n))
        for i in range(n):
            for j in range(n):
                if i == j:
                    graph[i][j] = 1
                elif ( (sqrt((nodes[i].x-nodes[j].x)**2 + (nodes[i].y-nodes[j].y)**2)) < r ):
                    # Adjacency matrix
                    graph[i][j] = 1
                    graph[j][i] = 1
                    # Node's neighbours
                    if nodes[j] not in nodes[i].neighbours:
                        nodes[i].neighbours.append(nodes[j])
                    if nodes[i] not in nodes[j].neighbours:
                        nodes[j].neighbours.append(nodes[i])

        return (nodes, graph, r)


    def getAverageDegree(self, graph):
        '''
        Gets the average degree of a graph
        :param graph:
        :return:
        '''
        n = len(graph)
        res = 0
        for i in range(n):
            res += np.sum(graph[i])
        return res/n

    def get_graph(self, n, p, d):
        '''
        Returns a graph on n nodes, discretisation level p and average degree d
        :param n: number of nodes
        :param p: discretisation level
        :param d: degree
        :return: tuple with nodes, graph and radius
        '''
        while True: # Somehow always finishes
            # Generate graph
            (current_nodes, graph, r) = self.randomGraph(n, p)

            # Check the degree
            degree = self.getAverageDegree(graph)

            # Check if the graph is connected
            current_nodes[0].update_hop(0)
            connected = True
            for i in range(len(current_nodes)):
                if current_nodes[i].hop is sys.maxint:
                    connected = False

            # Return if both checks are okay
            if degree == d and connected:
                return (current_nodes, graph, r)



    def get_sink(self):
        return self.sink

    def get_nodes(self):
        return self.nodes

    def test(self):
        print(self.get_graph(10, 10**16)) # python rounds up to ~16 decimals, so this is ~ the max discretisation
        print(self.get_graph(50, 10**16))
