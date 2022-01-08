import heapq
import random
import math
import json

with open('data_original.json') as inputFile:
    data = json.load(inputFile)

#Constants
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.7
POPULATION_SIZE = 100
FITNESS = 0
TRUCKS = 7
DEPOT = None
CAPACITY = 100
INF = float("inf")

#Genetic Algorithm Classes
class PrioritySet(object):
    def __init__(self):
        self.heap = []
        self.set = set()
    def push(self, d):
        if not d in self.set:
            heapq.heappush(self.heap, d)
            self.set.add(d)
    def pop(self):
        d = heapq.heappop(self.heap)
        self.set.remove(d)
        return d
    def poop(self):
        d = self.heap[-1]
        self.heap = self.heap[:-1]
        self.set.remove(d)
        return d
    def size(self):
        return len(self.heap)
    def __str__(self):
        op = ""
        for i in self.heap:
            op += str(i[0]) + " : " + i[1].__str__()
            op += "\n"
        return op
    def __getitem__(self, index):
        return self.heap[index]

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ") "
    def x_coor(self):
        return self.x
    def y_coor(self):
        return self.y

class Vehicle:
    def __init__(self, capacity):
        self.capacity = capacity
    def capacity(self):
        return self.capacity

class Customer:
    pos = Position(-1, -1)
    demand = 0
    def __init__(self, name):
        self.name = name
    def setPosition(self, x, y):
        self.pos = Position(x, y)
    def setDemand(self, d):
        self.demand = d
    def __str__(self):
        # return str(self.name) #+ " -> (" + str(self.pos.x) + ", " + \
        # str(self.pos.y) + ") -> " + str(self.demand)
        return "(" + str(self.pos.x) + ", " + \
               str(self.pos.y) + " )"

#Utility Functions
def copy(li):
    return [i for i in li]

def getProb():
    return random.random()

def get_random(li):
    index = random.randint(0, len(li) - 1)
    return li[index]

def get_distance(cus1, cus2):
    dist = math.sqrt(((cus1.pos.x - cus2.pos.x) ** 2) + ((cus1.pos.y - cus2.pos.y) ** 2))
    return dist

def print_tuple(t):
    print("0"),
    for i in t:
        print(i),
    print("0"),
    print(" -> f: " + str(get_fitness(t)))

def print_population(p):
    for i in p:
        for c in i:
            print(c),
        print("\n")

def print_population_heap(p):
    count = 1
    for i in p:
        print(count), (" )  ")
        print_tuple(i[1])
        count += 1
        print("\n")

#Helper Functions
def mutate(chromosome):
    temp = [i for i in chromosome]

    if getProb() < MUTATION_RATE:
        left = random.randint(1, len(temp) - 2)
        right = random.randint(left, len(temp) - 1)
        temp[left], temp[right] = temp[right], temp[left]

    return temp

def crossover(a, b):
    if getProb() < CROSSOVER_RATE:
        left = random.randint(1, len(a) - 2)
        right = random.randint(left, len(a) - 1)
        c1 = [c for c in a[0:] if c not in b[left:right + 1]]
        a1 = c1[:left] + b[left:right + 1] + c1[left:]
        c2 = [c for c in b[0:] if c not in a[left:right + 1]]
        b1 = c2[:left] + a[left:right + 1] + c2[left:]
        return a1, b1
    return a, b

def get_fitness(li):
    num_custo = len(li)
    fitness = 0

    for i in range(num_custo - 1):
        fitness += get_distance(li[i], li[i + 1])

    fitness += get_distance(DEPOT, li[0])
    fitness += get_distance(li[-1], DEPOT)

    temp = copy(li)
    temp.insert(0, DEPOT)
    temp.append(DEPOT)
    valid = 1
    curr_demand = 0
    for i in range(len(temp)):
        if temp[i] == DEPOT and curr_demand > CAPACITY:
            fitness = INF
        elif temp[i] == DEPOT:
            curr_demand = 0
        else:
            curr_demand += temp[i].demand

    return fitness

def getPopulationFitness(p):
    h = PrioritySet()
    for i in p:
        h.push((get_fitness(i), i))
    return h

def create_new():
    TempSet = copy(Customers)
    chromosome = []
    while len(TempSet) > 0:
        index = (int)(getProb() * len(TempSet))
        chromosome.append(TempSet.pop(index))

    return chromosome

#Genetic Algorithm
def Genetic_Algorithm():
    print("Population Generated, Evolution Beginning.")
    minimum_chrom = h[0]
    print("Current Minimum Chromosome: ", minimum_chrom[0])
    count = 0
    while count < 1000:
        ax = h.pop()
        bx = h.pop()
        a, b = crossover(list(ax[1]), list(bx[1]))
        a = mutate(a)
        while get_fitness(a) == INF:
            a = create_new()
        b = mutate(b)
        while get_fitness(b) == INF:
            b = create_new()
        if get_fitness(a) != INF:
            h.push((get_fitness(a), tuple(a)))
        else:
            h.push(ax)
        if get_fitness(b) != INF:
            h.push((get_fitness(b), tuple(b)))
        else:
            h.push(bx)

        while h.size() < POPULATION_SIZE:
            TempSet = copy(Customers)
            chromosome = []
            count += 1
            while len(TempSet) > 0:
                index = (int)(getProb() * len(TempSet))
                chromosome.append(TempSet.pop(index))
            h.push((get_fitness(chromosome), tuple(chromosome)))
        count = count + 1

        if count % 1000 == 0:
            print(count),
            print("Generation done")

        if h[0][0] < minimum_chrom[0]:
            minimum_chrom = h[0]
            print("Current Minimum Chromosome: ", minimum_chrom[0])

    print_tuple(minimum_chrom[1])
    print(count)

#Initializing Function
def initialize_population():
    while len(population) < POPULATION_SIZE:
        TempSet = copy(Customers)
        chromosome = []
        while len(TempSet) > 0:
            index = (int)(getProb() * len(TempSet))
            chromosome.append(TempSet.pop(index))

        if get_fitness(chromosome) != INF:
            population.add(tuple(chromosome))

#Data
def create_data_array():

    noOfCustomers = len(data["nodes"])
    customerPosDemand = dict()
    for i in range(noOfCustomers):
        customerPosDemand[data["nodes"][i]["x"], data["nodes"][i]["y"]] = data["nodes"][i]["demand"]
    locations = list(customerPosDemand.keys())
    print(f'고객위치: {locations}')

    demands = []
    for i in range(noOfCustomers):
        demands.append(data['nodes'][i]['demand'])
    print(f'고객 수요: {demands}')

    for i in range(0, len(locations)):
        c = Customer(i)
        c.setPosition(locations[i][0], locations[i][1])
        c.setDemand(demands[i])
        Customers.append(c)

    i = 0
    c = Customer(i)
    c.setPosition(data["depot"]["x"], data["depot"]["y"])
    c.setDemand(0)
    global DEPOT
    DEPOT = c
    print(DEPOT)

    for j in range(TRUCKS - 1):
        Customers.append(DEPOT)

Customers = []
population = set()

if __name__ == '__main__':
    create_data_array()
    initialize_population()
    h = getPopulationFitness(population)
    Genetic_Algorithm()