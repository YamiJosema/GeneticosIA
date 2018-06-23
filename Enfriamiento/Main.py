import Tkinter
from Tkinter import *
import tkMessageBox
import operator
import PIL
from PIL import ImageTk
import PIL.Image
import matplotlib.pyplot as plt
import networkx

import random
from random import shuffle
from Enfriamiento.Modelo import *
import math

from matplotlib import colors as mcolors

TEMPERATURE_START = 8
TEMPERATURE_END = 0.1
COOLING_FACTOR = 0.999 
EDGE_CHANCE = 0.15 #La probabilidad de que se cree un arista
R_EDGES = []
Colores=[] #'red','blue','yellow','green','black','white','brown','orange','pink','purple','grey'
  
mutation_chance = 0.1 #La probabilidad de que un individuo mute


def cargar_colores():
    colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
    for c in colors:
        Colores.append(c)
    shuffle(Colores)


def edges(paises):
    """
        Generamos aristas aleatorias para el grafo usando
        la constante EDGE_CHANCE por defecto a 0.15
    """
    edges=[]
    for i in range(paises):
        for j in range(paises):
            if i!=j and random.random() <= EDGE_CHANCE:
                edges.append(Edge(i,j))
    
    return edges


def individual(paises, colores):
    """
        Crea un individuo. Las aristas solo se generan una vez
        para los individuos de una misma poblacion.
    """
    graph = Graph(paises, colores)
    
    if len(R_EDGES)==0:
        R_EDGES.extend(edges(paises))
        print("Aristas: %s"%(R_EDGES))
    
    graph.set_edges(R_EDGES)
    
    return  graph


def create_population(paises, colores, poblacion):
    """
        Crea una poblacion con los datos solicitados.
    """
    return [individual(paises, colores) for i in range(poblacion)]


def get_fitness(individual):
    """
        Calcula el fitness de un individuo concreto.
        Nuestro objetivo sera minimizar. Se penalizara sumando
        el tamano del grafo si el color de dos paises conectados 
        por una arista es el mismo.
    """
    fitness = 0
    for edge in individual.edges:
        nodes = individual.nodes
        if nodes[edge.i].color==nodes[edge.j].color:
            fitness+=individual.n
            
#     print(str(fitness)+"-->"+str(individual))
    return fitness


def selection_and_reproduction(population, poblacion):
    """
        Puntua todos los elementos de la poblacion (population) y se queda con los mejores
        guardandolos dentro de 'selected'. El numero de seleccionados sera una tercera parte
        del total del a poblacion.
        Despues mezcla el material genetico de los elegidos para crear nuevos individuos y
        llenar la poblacion (guardando tambien una copia de los individuos seleccionados sin
        modificar).
  
        Por ultimo muta a los individuos.
    """
    pressure=int(poblacion/3)
  
    fitness = [ (get_fitness(i), i) for i in population] #Calcula el fitness de cada individuo, y lo guarda en pares ordenados de la forma (5 , [1,2,1,1,4,1,8,9,4,1])
    fitness = [i[1] for i in sorted(fitness, reverse=True)] #Ordena los pares ordenados y se queda solo con el array de valores
    population = fitness
  
    selected =  fitness[(len(fitness)-pressure):] #Esta linea selecciona los 'n' individuos del final, donde n viene dado por 'pressure'
    pprint =[(get_fitness(i), i) for i in selected]
    print("Seleccion:\n%s"%(pprint)) #Se muestra la seleccion
    
    #Se mezcla el material genetico para crear nuevos individuos
    for i in range(len(population)-pressure):
        punto = random.randint(1,population[i].n-1) #Se elige un punto para hacer el intercambio
        padre = random.sample(selected, 2) #Se eligen dos padres
          
        population[i].nodes[:punto] = padre[0].nodes[:punto] #Se mezcla el material genetico de los padres en cada nuevo individuo
        population[i].nodes[punto:] = padre[1].nodes[punto:]
        
    return population #El array 'population' tiene ahora una nueva poblacion de individuos, que se devuelven


def cooldown(population, colores, poblacion):
    """
        Enfriamiento Simulado. Partiendo de una temperatura inicial, iremos generando vecinoso y siempre y cuando el fitness haya mejorado, lo sustituiremos 
    """
    pressure=int(poblacion/3)
    
    for i in range(len(population)-pressure):
        ind = population[i].nodes[:]
        fitness_previous = 1000000000
        temperature = TEMPERATURE_START
          
        while temperature > TEMPERATURE_END:
            mutated = mute(ind, population[i].n, colores)
            graph = Graph(population[i].n, colores)
            graph.set_edges(R_EDGES)
            graph.set_nodes(ind)
            fitness_new = get_fitness(graph)
            difference = fitness_new-fitness_previous
            if difference < 0 or math.exp(-difference/temperature)>random.random(): #Meter opcion de decir cuanto mejora para aceptarla
                fitness_previous=fitness_new
                ind = mutated
            temperature *= COOLING_FACTOR
               
        population[i].set_nodes(ind)
    
    return population
            

def mute(ind, paises, colores):
    """
        Muta al individuo. Cambiando al hazar el color de uno de los nodos
    """
    punto = random.randint(0,paises-1) #Se elgie un punto al azar
    nuevo_valor = random.randint(1,colores) #y un nuevo valor para este punto
    #Es importante mirar que el nuevo valor no sea igual al viejo
    while nuevo_valor == ind[punto]:
        nuevo_valor = random.randint(1,colores)
    #Se aplica la mutacion
    ind[punto] = nuevo_valor
    return ind


def final(population):
    """
        Devolvera TRUE si hay algun individuo con fitnes 0 en la poblacion
    """
    res = False
    for p in population:
        if p[0]==0:
            res=True
            break
    return res


def get_best(population, poblacion):
    """
        Devuelve los n mejores individuos de una poblacion. El valor de n viene definido por pressure
    """
    pressure=int(poblacion/3)
    
    fitness = [ (get_fitness(i), i) for i in population] #Calcula el fitness de cada individuo, y lo guarda en pares ordenados de la forma (5 , [1,2,1,1,4,1,8,9,4,1])
    fitness = [i[1] for i in sorted(fitness, reverse=True)] #Ordena los pares ordenados y se queda solo con el array de valores
    population = fitness
  
    selected =  fitness[(len(fitness)-pressure):] #Esta linea selecciona los 'n' individuos del final, donde n viene dado por 'pressure'
    
    return selected


def algoritmo_random(paises, colores, poblacion):
    del R_EDGES[:]
    
    toplevel = Toplevel()
    text = Text(toplevel)
    
    population = create_population(paises, colores, poblacion)#Inicializar una poblacion
    pprint =[(get_fitness(i), i) for i in population]
    print("Poblacion Inicial:\n%s"%(pprint)) #Se muestra la poblacion inicial
    print("\n")
    
    text.insert(INSERT, "Numero de Paises = "+str(paises)+"\nNumero de Colores = "+str(colores))
    text.insert(INSERT, "\nAristas:\n")
    text.insert(INSERT, R_EDGES)
    text.insert(INSERT, "\nPoblacion Inicial:\n")
    for row in pprint:
        text.insert(INSERT, row)
        text.insert(INSERT,"\n")
    
    #Se evoluciona la poblacion
    for i in range(100):
        population = selection_and_reproduction(population, poblacion)
        population = cooldown(population, colores, poblacion)
     
        pprint =[(get_fitness(j), j) for j in population]
        print("Generacion "+str(i+1)+":\n%s"%(pprint))
        if final(pprint):
            break
    
    print("\nPoblacion Final:\n%s"%(pprint)) #Se muestra la poblacion evolucionada
    print("\nMejores soluciones:\n%s"%([(get_fitness(j), j) for j in get_best(population, poblacion)]))
    print("\n\n")
    
    text.insert(INSERT, "Mejores Soluciones con "+str(i+1)+" iteraciones:\n")
    text.insert(INSERT, "")
    
    for row in get_best(population, poblacion):         
        text.insert(INSERT, row)
        fitness = get_fitness(row)
        text.insert(INSERT, " Fiteness = "+str(fitness)+"\n")
        
    #Representamos el grafo
    solucion_a_dibujar = get_best(population, poblacion)[-1]
    GrafoParaDibujar,mapa_colores = ConvertirParaDibujar(solucion_a_dibujar)
    pos = networkx.spring_layout(GrafoParaDibujar)
    
    #Dibujamos el grafo y lo guardamos como PNG
    networkx.draw(GrafoParaDibujar,pos,node_color=mapa_colores,with_labels=True)
    plt.savefig("Graph.png", format="PNG")
    plt.clf()
    
    #Cargamos el grafo que acabamos de guardar y lo pintamos
    imgn = PIL.ImageTk.PhotoImage(PIL.Image.open("Graph.png"))
    
    panel = Toplevel()
    grafoo = Label(panel, image = imgn)
        
    sc = Scrollbar(toplevel)
    sc.pack(side=RIGHT, fill=Y)
    
    grafoo.pack(side = "bottom", fill = "both", expand = "yes")

    text.pack()
    toplevel.mainloop()
    
#Aqui pasamos de nuestro tipo de grafo a uno que podamos usar para imprimir y dibujar por pantalla:
def ConvertirParaDibujar(Grafito):
    GrafoParaDibujar = networkx.Graph()
    color_map=[]
    for i in  range(0,len(Grafito.nodes)):
        GrafoParaDibujar.add_node(i) #Cogemos los nodos de nuestro grafo y los anadimos al nuevo
        color_map.append(Colores[Grafito.nodes[i].color]) #Anadimos cada color de cada nodo al mapa de colores del grafo
    for i in range(0,len(Grafito.nodes)):
        for arista in R_EDGES:
            if i == arista.i:
                #Para cada nodo cogemos SUS aristas (sus aristas seran las que sean iguales en nodo_a) y las anadimos al grafo
                GrafoParaDibujar.add_edge(i,arista.j)
    return GrafoParaDibujar,color_map
    

def algoritmo_variable():
    
    busqueda = Toplevel()
    label1 = Label(busqueda, text="Paises: ")
    label2 = Label(busqueda, text="Colores: ")
    label3 = Label(busqueda, text="Individuos: ")
    entrada3=Entry(busqueda, bd=5)
    entrada1=Entry(busqueda, bd=5)
    entrada2=Entry(busqueda, bd=5)

    def buttCallBack():
        paises=entrada1.get()
        colores=entrada2.get()
        individuos=entrada3.get()
        if paises=='':
            paises=10
        elif int(paises)<2:
            paises=2
        if colores=='':
            colores=3
        elif int(colores)<2:
            colores=2
        if individuos=='':
            individuos=10
        elif int(individuos)<6:
            individuos=6  
        algoritmo_random(int(paises), int(colores), int(individuos))
        
        
    butt=Tkinter.Button(busqueda, text="Ejecutar", command = buttCallBack)
    
    label1.pack(side=LEFT)
    entrada1.pack(side=LEFT)
    
    label2.pack(side=LEFT)
    entrada2.pack(side=LEFT)
    
    label3.pack(side=LEFT)
    entrada3.pack(side=LEFT)
    
    butt.pack(side=LEFT)
    
    busqueda.mainloop()
    

def principal():
    cargar_colores()
    
    top = Tkinter.Tk()
     
    menubar = Menu(top)
    
    text = Text(top)
    
    dm = Menu(menubar, tearoff=0)
    dm.add_command(label="Estandar", command=lambda: algoritmo_random(10, 3, 10)) #, command=
    dm.add_command(label="Variable", command=algoritmo_variable)
    dm.add_command(label="Salir", command=top.destroy)
    menubar.add_cascade(label="Algoritmo", menu=dm)
    
    text.insert(INSERT, "Estandar: Paises=10, Colores=3, Poblacion=10\n")
    text.insert(INSERT, "Variable: Paises>=2, Colores>=2, Poblacion>=6\nCampos vacios tendran valores estandar")
    
    text.pack()
    top.config(menu=menubar)
    
    
    top.mainloop()
    
    
if __name__=="__main__":
    principal()
