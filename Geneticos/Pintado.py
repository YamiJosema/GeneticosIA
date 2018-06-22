#!/usr/bin/env python
"""
Draw a graph with matplotlib, color by degree.

You must have matplotlib for this to work.
"""
from Enfriamiento.Modelo import *
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import colors as mcolors


def plot(individuo, colores):
    colores = []
    colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
    for c in colors:
        colores.append(c)
    G=nx.Graph()
    pos={}
    j=1
    for i in range(1, individuo.n*2):
        pos[i]=(i+j,i-j)
        i+=1
        if i%3==0:
            j+=5
    i=1
    for node in individuo.nodes:
        nx.draw_networkx_nodes(G, pos,
                                nodelist=[i], 
                                node_size=500, 
                                node_color=colores[node.color])
        i+=1
     
    edges=[]
    for edge in individuo.edges:
        edges.append((edge.i,edge.j))   
        
    G.add_edges_from([(1 ,2) , (2 ,3) , (1 ,3) , (1 ,4) ])
    nx.draw_networkx_edges(G, pos, width=1.0)
    plt.axis('off')
    plt.show()
     
     
graph = Graph(10,3)

edges=[]
for i in range(10):
    for j in range(10):
        if i!=j and random.random() <= 0.15:
            edges.append(Edge(i,j))
graph.set_edges(edges)
plot(graph, 3)