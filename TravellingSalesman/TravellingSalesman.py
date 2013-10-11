import math
import itertools
## Dynamic Programming approach to finding the soltuon to the
## traveling salesman problem

cities = {}
edges = {}
solved = {}
maxValue = 0

    
def readInData (fileToRead):
## This reads the cities with x and y coordinates from the file and puts
## them into the data structures. 

    i = 0

    for line in fileToRead:
            
        if i != 0:
            tempLine = line.split()
            x = float(tempLine[0])
            y = float(tempLine[1])

            cities[i] = (x, y)
            
        else:
            tempLine = line.split()
            numCities = int(tempLine[0])
            print "Expecting ", numCities, " cities"
                            
        i += 1

    print "Found ", len(cities), " cities"
            
    print "After reading file, found %d lines" % (i)
    
    return 

def computeEdges ():
##    This computes the edge weight = Euclidean distance between each pair
##    of cities.  It then converts this to an integer keeping 2 decimal
##    places, because that is more than enough accuracy for this algorithm.
##    Remember to divide by 100 later!

    global edges

    for i in range (1,len(cities)+1):
        x1 = cities[i][0]
        y1 = cities[i][1]
        for j in range (1,i):
            x2 = cities[j][0]
            y2 = cities[j][1]
            
            distance = math.hypot(x2 - x1, y2 - y1)
            edges[(i,j)] = int(distance*100)
            edges[(j,i)] = int(distance*100)
            
    return 

def initializeSolutions (cities, initValue, m):
##    Initialize the solutions for this iteration.  
    global solved

    subsets = itertools.combinations(cities, m)

    for s in subsets:
        solved[s] = []
        for j in range (1, len(cities)+2):
            solved[s].append(initValue)

##    for x in solved:
##        print x, solved[x]

    return 

def deleteSolutions (m):
    global solved

    if (m > 2):
        subsets = itertools.combinations(cities, m-2)
        for s in subsets:
            solved.pop(s, None)
            
##        print "deleted solutions for k = ", k

    return 


def solveAProblem (s, j):

    prevSet = tuple(y for y in s if (y != j))

    bestSoFar = maxValue

    for k in prevSet:
        current = solved[prevSet][k] + edges[(j,k)]
        if current < bestSoFar:
            bestSoFar = current

    return bestSoFar
         
    
def computeAllShortest ():

    global edges
    global maxValue
    
                    
    print "About to open  file "
    f = open ("tsp.Txt", 'r')
    f = open ("test.Txt", 'r')

##  Read the data file 
    readInData (f)
    print cities

    edges = {}
    computeEdges()

##    print edges
    print "num cities is ", len(cities)
    print "num edges is ", len(edges)

    maxValue = 0;
    for edge in edges:
        maxValue += edges[edge]

    print "maxValue is ", maxValue

##    OK here is the basic algorithm.
##
##    We have a set of cities {1, 2, ...., n}
##    We have a set of edges { (i, j): dist }
##    It is a complete undirected graph, so that there is an edges
##    between each pair of cities
##    The goal is to get the shortest tour of the cities starting at
##    city 1 and ending back up at city 1.
##    
##    Let A be a 2-d array indexed by subsets S of {1, 2, ..., n} that
##    contain 1 and destinations j in {1, 2, ..., n}
##
##    Base Case:
##
##    A [S, i] = 0 if S = {1}
##              = plus infinity otherwise (we use a max constant)
##
##    For m = 2, 3, ..., n:
##        For each set S of size m that contains 1:
##            For each j in S, j != 1:
##                A [S, k] is the min over k in S, k != j of A[S-{j}, k] +
##                  cost of edge (k, j)
##
##    To get the final solution: basically the last hop:
##
##        min over j = 2, ..., n of A[{1,2,...,n},j] + cost(j,1)
##        
    
    initializeSolutions (cities, maxValue, 1)
    initializeSolutions (cities, maxValue, 2)
##    for x in solved:
##        print x, solved[x]
    print "init done"

    solved[(1,)][1] = 0


    for m in range (2, len(cities)+1):
        print "starting iteration m = ", m
        initializeSolutions (cities, maxValue, m)
        subsets = itertools.combinations(cities, m)
##        print "init done for this m"
        for s in subsets:
            if 1 in s:
                for j in s:
                    if j != 1:
                        solved[s][j] = solveAProblem (s, j)
        deleteSolutions (m)


    finalSubsets = itertools.combinations(cities, len(cities))
    for finalSet in finalSubsets:
##        print "finalset ", finalSet
        bestSoFar = maxValue
        for j in finalSet:
            if j != 1:
                edgeCost = edges[(j,1)]
                current = solved[finalSet][j] + edgeCost
                if current < bestSoFar:
                    bestSoFar = current
                
        print bestSoFar//100


    return bestSoFar


    return





if (__name__ == "__main__"):

    computeAllShortest();

            

    
    import doctest
    doctest.testmod()

