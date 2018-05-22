import random

class Graph:
    def __init__(self,n):
        self.n=n
        self.nodes=[]
        for i in range(0,n):
            self.new_node(random.randint(1, 3))
        self.edges=[]
        
    def new_node(self, color):
        self.nodes.append(Node(color))
        
    def new_edge(self, i, j):
        self.edges.append(Edge(i,j))
        
    def __str__(self):
        return str(self.nodes)
    def __unicode__(self):
        return str(self.nodes)
    def __repr__(self):
        return str(self.nodes)


class Node:
    def __init__(self, color):
        self.color=color
        
    def __str__(self):
        return str(self.color)
    def __unicode__(self):
        return str(self.color)
    def __repr__(self):
        return str(self.color)


class Edge:   
    def __init__(self,i,j):
        self.i=i
        self.j=j
        
    def __str__(self):
        return "("+str(self.i)+", "+str(self.j)+")"
