import Tkinter
from Tkinter import *
import tkMessageBox

import random
from Enfriamiento.Modelo import *
import math

# n = 10 #numero de paises. Podra ser variable
# k = 3 #numero de colores
#el gen sera una lista en las que i=pais y lista[i]=color

TEMPERATURE_START = 8
TEMPERATURE_END = 0.1
COOLING_FACTOR = 0.999
EDGE_CHANCE = 0.15
R_EDGES = []

  
# modelo = [1,2,3,2,1,2,3,1,2,3] #Objetivo a alcanzar
# largo = 10 #La longitud del material genetico de cada individuo
# pressure = int(n/3) #Cuantos individuos se seleccionan para reproduccion. Necesariamente mayor que 2
#pressure deber ser un 30% del total de individuos
mutation_chance = 0.1 #La probabilidad de que un individuo mute

def edges(paises):
    edges=[]
    for i in range(paises):
        for j in range(paises):
            if i!=j and random.random() <= EDGE_CHANCE:
                edges.append(Edge(i,j))
    
    return edges


def individual(paises, colores):
    """
        Crea una poblacion nueva de individuos
    """
    graph = Graph(paises, colores)
    
    if len(R_EDGES)==0:
        R_EDGES.extend(edges(paises))
        print("Aristas: %s"%(R_EDGES))
    
    graph.set_edges(R_EDGES)
    
    return  graph


def create_population(paises, colores):
    return [individual(paises, colores) for i in range(paises)]


def get_fitness(individual):
    """
        Calcula el fitness de un individuo concreto.
    """
    fitness = 0
    for edge in individual.edges:
        nodes = individual.nodes
        if nodes[edge.i].color==nodes[edge.j].color:
            fitness+=individual.n
            
#     print(str(fitness)+"-->"+str(individual))
    return fitness


def selection_and_reproduction(population, paises):
    """
        Puntua todos los elementos de la poblacion (population) y se queda con los mejores
        guardandolos dentro de 'selected'.
        Despues mezcla el material genetico de los elegidos para crear nuevos individuos y
        llenar la poblacion (guardando tambien una copia de los individuos seleccionados sin
        modificar).
  
        Por ultimo muta a los individuos.
  
    """
    
    pressure=int(paises/3)
    if(pressure<2):
        pressure=2
  
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


def cooldown(population, paises, colores):

    pressure=int(paises/3)
    if(pressure<2):
        pressure=2
    
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
    punto = random.randint(0,paises-1) #Se elgie un punto al azar
    nuevo_valor = random.randint(1,colores) #y un nuevo valor para este punto
    #Es importante mirar que el nuevo valor no sea igual al viejo
    while nuevo_valor == ind[punto]:
        nuevo_valor = random.randint(1,colores)
    #Se aplica la mutacion
    ind[punto] = nuevo_valor
    return ind


def final(population):
    res = False
    for p in population:
        if p[0]==0:
            res=True
            break
    return res


def get_best(population, paises):
    pressure=int(paises/3)
    if(pressure<2):
        pressure=2
    
    fitness = [ (get_fitness(i), i) for i in population] #Calcula el fitness de cada individuo, y lo guarda en pares ordenados de la forma (5 , [1,2,1,1,4,1,8,9,4,1])
    fitness = [i[1] for i in sorted(fitness, reverse=True)] #Ordena los pares ordenados y se queda solo con el array de valores
    population = fitness
  
    selected =  fitness[(len(fitness)-pressure):] #Esta linea selecciona los 'n' individuos del final, donde n viene dado por 'pressure'
    
    return selected


def algoritmo_random(paises, colores):
    toplevel = Toplevel()
    text = Text(toplevel)
    
    population = create_population(paises, colores)#Inicializar una poblacion
    pprint =[(get_fitness(i), i) for i in population]
    print("Poblacion Inicial:\n%s"%(pprint)) #Se muestra la poblacion inicial
    print("\n")
    
    text.insert(INSERT, "Numero de Paises = "+str(paises)+"\nNumero de Colores = "+str(colores))
    text.insert(INSERT, "\nPoblacion Inicial:\n")
    for row in pprint:
        text.insert(INSERT, row)
        text.insert(INSERT,"\n")
    
    #Se evoluciona la poblacion
    for i in range(100):
        population = selection_and_reproduction(population, paises)
        population = cooldown(population, paises, colores)
     
        pprint =[(get_fitness(j), j) for j in population]
        print("Generacion "+str(i+1)+":\n%s"%(pprint))
        if final(pprint):
            break
    
    print("\nPoblacion Final:\n%s"%(pprint)) #Se muestra la poblacion evolucionada
    print("\nMejores soluciones:\n%s"%([(get_fitness(j), j) for j in get_best(population, paises)]))
    print("\n\n")
    
    text.insert(INSERT, "Mejores Soluciones con "+str(i+1)+" iteraciones:\n")
    text.insert(INSERT, "")
    
    for row in get_best(population, paises):         
        text.insert(INSERT, row)
        fitness = get_fitness(row)
        text.insert(INSERT, " Fiteness = "+str(fitness)+"\n")

    text.pack()
    toplevel.mainloop()
    

def algoritmo_variable():
    
    busqueda = Toplevel()
    label1 = Label(busqueda, text="Numero de paises: ")
    label2 = Label(busqueda, text="Numero de colores: ")
    entrada1=Entry(busqueda, bd=5)
    entrada2=Entry(busqueda, bd=5)

    def buttCallBack():
        paises=entrada1.get()
        colores=entrada2.get()
        if paises=='':
            paises=10
        if colores=='':
            colores=3
        algoritmo_random(int(paises), int(colores))
        
        
    butt=Tkinter.Button(busqueda, text="Ejecutar", command = buttCallBack)
    
    label1.pack(side=LEFT)
    entrada1.pack(side=LEFT)
    
    label2.pack(side=LEFT)
    entrada2.pack(side=LEFT)
    
    butt.pack(side=LEFT)
    
    busqueda.mainloop()
    

def principal():
    top = Tkinter.Tk()
     
    menubar = Menu(top)
    
    dm = Menu(menubar, tearoff=0)
    dm.add_command(label="Estandar", command=lambda: algoritmo_random(10, 3)) #, command=
    dm.add_command(label="Variable", command=algoritmo_variable)
    dm.add_command(label="Salir", command=top.destroy)
    menubar.add_cascade(label="Algoritmo", menu=dm)
    
    top.config(menu=menubar)
    
    top.mainloop()
    
    
if __name__=="__main__":
    principal()
