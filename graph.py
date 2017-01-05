import random
from math import sqrt
from math import pi
from node import Node
from network import Network

# getGraph(n, p) returns a tuple (x,y, z) where :
# x = list of n random nodes coordinates in a 1x1 grid with discretisation level p
#     such that the average degree of a node is 4
# y = representation of the graph associated to the network as a (triangular) incidence matrix
# z = the radius of the emission area of a node

# what matters is the quotient between the length of one side of the square and the radius of emission r

def randomGraph(n, p):
  nodes = [] # randomly distributed node coordinates list
  for i in range(n):
    nodes.append(Node(random.randint(0,p)/p, random.randint(0,p)/p)) # p = discretisation level

  graph = [] # representation of the graph as a triangular matrix
  for i in range(n):
    row = []
    for j in range(n):
      row.append(0)
    graph.append(row)

  r = sqrt(4/(n*pi)) # optimisation : the radius should be approximately this value
  # because pi*n*r^2 = 4 (average degree of a node)

  for i in range(n):
    for j in range(n):
        if i == j:
            graph[i][j] = 1
        elif ( (sqrt((nodes[i][0]-nodes[j][0])**2 + (nodes[i][1]-nodes[j][1])**2)) < r ):
            graph[i][j] = 1
            graph[j][i] = 1
  return (nodes, graph, r)

def Sum(liste):
  res = 0
  for i in range(len(liste)):
    res += liste[i]
  return res

def getAverageDegree(graph):
  n = len(graph) # number of nodes
  res = 0
  for i in range(n):
    res += Sum(graph[i])
  return 2*res/n # 2*(nombre d'arêtes) = somme des degrés
                 # on divise par n pour faire la moyenne

def getGraph(n, p): #n = number of vertexes, p = pas de discrétisation
  while True: # could be infinite loop but always finish
    (nodes, graph, r) = randomGraph(n, p)
    d = getAverageDegree(graph)
    if d == 4.0:
      return (nodes, graph, r)

def test():
  print(getGraph(10, 10**16)) # python rounds up to ~16 decimals
                              # so this is ~ the max discretisation
  print(getGraph(50, 10**16))
