import random
from Enfriamiento.Modelo import *

n = 10 #numero de paises. Podra ser variable
k = 3 #numero de colores
#el gen sera una lista en las que i=pais y lista[i]=color

EDGE_CHANCE = 0.1

  
# modelo = [1,2,3,2,1,2,3,1,2,3] #Objetivo a alcanzar
# largo = 10 #La longitud del material genetico de cada individuo
pressure = int(n/3) #Cuantos individuos se seleccionan para reproduccion. Necesariamente mayor que 2
#pressure deber ser un 30% del total de individuos
mutation_chance = 0.1 #La probabilidad de que un individuo mute
  
# print("\n\nModelo: %s\n"%(modelo)) #Mostrar el modelo, con un poco de espaciado

def edges(paises):
    edges=[]
    for i in range(paises):
        for j in range(paises):
            if i!=j and random.random() <= EDGE_CHANCE:
                edges.append(Edge(i,j))
    return edges


def individual(paises):
    """
        Crea una poblacion nueva de individuos
    """
    graph = Graph(paises) 
    
    graph.edges=edges(paises)

    return  graph


def create_population(paises):
    return [individual(paises) for i in range(paises)]


def get_fitness(individual, n):
    """
        Calcula el fitness de un individuo concreto.
    """
    fitness = 0
    for edge in individual.edges:
        nodes = individual.nodes
        if nodes[edge.i].color!=nodes[edge.j].color:
            fitness+=1
        elif nodes[edge.i].color==nodes[edge.j].color:
            fitness-=n
            
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
    fitness = [ (get_fitness(i,n), i) for i in population] #Calcula el fitness de cada individuo, y lo guarda en pares ordenados de la forma (5 , [1,2,1,1,4,1,8,9,4,1])
    fitness = [i[1] for i in sorted(fitness)] #Ordena los pares ordenados y se queda solo con el array de valores
    population = fitness
  
    selected =  fitness[(len(fitness)-pressure):] #Esta linea selecciona los 'n' individuos del final, donde n viene dado por 'pressure'
    pprint =[(get_fitness(i,n), i) for i in selected]
    print("Seleccion:\n%s"%(pprint)) #Se muestra la poblacion inicial
    
    #Se mezcla el material genetico para crear nuevos individuos
    for i in range(len(population)-pressure):
        punto = random.randint(1,paises-1) #Se elige un punto para hacer el intercambio
        padre = random.sample(selected, 2) #Se eligen dos padres
          
        population[i].nodes[:punto] = padre[0].nodes[:punto] #Se mezcla el material genetico de los padres en cada nuevo individuo
        population[i].nodes[punto:] = padre[1].nodes[punto:]
  
    return population #El array 'population' tiene ahora una nueva poblacion de individuos, que se devuelven


def mutation(population, paises):
    """
        Se mutan los individuos al azar. Sin la mutacion de nuevos genes nunca podria
        alcanzarse la solucion.
    """
    for i in range(len(population)-pressure):
        if random.random() <= mutation_chance: #Cada individuo de la poblacion (menos los padres) tienen una probabilidad de mutar
            punto = random.randint(0,paises-1) #Se elgie un punto al azar
            nuevo_valor = random.randint(1,3) #y un nuevo valor para este punto
   
            #Es importante mirar que el nuevo valor no sea igual al viejo
            while nuevo_valor == population[i].nodes[punto]:
                nuevo_valor = random.randint(1,3)
   
            #Se aplica la mutacion
            population[i].nodes[punto].color = nuevo_valor
   
    return population


population = create_population(n)#Inicializar una poblacion
pprint =[(get_fitness(i,n), i) for i in population]
print("Poblacion Inicial:\n%s"%(pprint)) #Se muestra la poblacion inicial

   
#Se evoluciona la poblacion
for i in range(300):
    population = selection_and_reproduction(population,n)
    population = mutation(population, n)
    
    pprint =[(get_fitness(j,n), j) for j in population]
    print("Generacion "+str(i+1)+":\n%s"%(pprint))
   
   
print("\nPoblacion Final:\n%s"%(pprint)) #Se muestra la poblacion evolucionada
print("\n\n")

