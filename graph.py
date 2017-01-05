import random
from math import sqrt
from math import pi
from node import Node
import numpy as np

# getGraph(n, p) returns a tuple (x,y, z) where :
# x = list of n random nodes coordinates in a 1x1 grid with discretisation level p
#     such that the average degree of a node is 4
# y = representation of the graph associated to the network as a (triangular) incidence matrix
# z = the radius of the emission area of a node

# what matters is the quotient between the length of one side of the square and the radius of emission r
class Graph:

    def __init__(self, n):
        (self.nodes, self.incidenceMatrix, self.range) = self.getGraph(n, 10 ** 16)

    def randomGraph(self, n, p):
        nodes = [] # randomly distributed node coordinates list
        for i in range(n):
            nodes.append(Node(random.randint(0,p)*1./p, random.randint(0,p)*1./p)) # p = discretisation level

        r = sqrt(4/(n*pi)) # optimisation : the radius should be approximately this value
        # because pi*n*r^2 = 4 (average degree of a node)

        # incidence matrix
        graph = np.zeros((n,n))
        for i in range(n):
          for j in range(n):
              if i == j:
                  graph[i][j] = 1
              elif ( (sqrt((nodes[i].x-nodes[j].x)**2 + (nodes[i].y-nodes[j].y)**2)) < r ):
                  graph[i][j] = 1
                  graph[j][i] = 1
        return (nodes, graph, r)


    def getAverageDegree(self, graph):
        n = len(graph) # number of nodes
        res = 0
        for i in range(n):
            res += np.sum(graph[i])
        print res
        return 2*res/n  # 2* nbr d'aretes = somme des degres # on divise par n pour faire la moyenne

    def getGraph(self, n, p): #n = number of vertexes, p = pas de discretisation
        while True: # could be infinite loop but always finish
            (nodes, graph, r) = self.randomGraph(n, p)
            d = self.getAverageDegree(graph)
            print(d)
            if d == 4.0:
                return (nodes, graph, r)

    def test(self):
        print(self.getGraph(10, 10**16)) # python rounds up to ~16 decimals, so this is ~ the max discretisation
        print(self.getGraph(50, 10**16))
