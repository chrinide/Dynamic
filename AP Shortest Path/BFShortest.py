
## Dynamic Programming approach to finding the shortest paths in a
## graph that contains negative edge lengths

nodes = {}
inNodes = {}
solved = []
maxValue = 0
shortestPerNode = []
negativeCycle = False

    
def readInData (fileToRead):
## This reads the edges with  nodes and weights from the file and puts
## them into the data structures. 

    i = 0
    numNodes = 0
    numEdges = 0
    global maxValue
    maxEdgeWeight = 0

    for line in fileToRead:
            
        if i != 0:
            tempLine = line.split()
            source = int(tempLine[0])
            dest = int(tempLine[1])
            weight = int(tempLine[2])
            if weight > maxEdgeWeight:
                maxEdgeWeight = weight

            if dest not in inNodes:
                inNodes[dest] = []

            inNodes[dest].append( (source, weight) )
            nodes[source] = 1
            nodes[dest] = 1
            
##            if i < 10:
##                print dest, " : ", inNodes[dest]

        else:
            tempLine = line.split()
            numNodes = int(tempLine[0])
            numEdges = int(tempLine[1])
            print ("Expecting ", numNodes, " nodes and ", numEdges, " edges")
                            
        i += 1

    if (maxEdgeWeight < 0):
        maxEdgeWeight = -maxEdgeWeight
    maxValue = maxEdgeWeight * numEdges
    print "Found ", len(nodes), " nodes"
    print "Found ", numEdges, " edges"
    print "Max path len is under ", maxValue
            
    print "After reading file, found %d lines" % (i)
    
    return 

def initializeSolutions (n, initValue):
    global solved
    solved = []

    for i in range (0, 2):
        solved.append([])
        for j in range (0, n+2):
            solved[i].append(initValue)

    for j in range (0, n+2):
        shortestPerNode.append(initValue)

    return 

def resetSolutions (n, initValue):
    global solved

    for i in range (0, 2):
        for j in range (0, n+2):
            solved[i][j] = initValue
        
    return 

# Compute the set of shortest paths from sourceNode to the rest
# of the nodes in the graph.  Use initValue as an upper bound to
# compare path lengths to.
def computeOneShortest (sourceNode, initValue):

    global negativeCycle

    numNodes = len(inNodes)
    resetSolutions (numNodes+1, initValue)
    solved[0][sourceNode] = 0
    solved[1][sourceNode] = 0

##    For each node, find the shortest path from sourceNode to that node
##    This algorithm builds up shortest paths of length i, using the
##    information about shortest paths of length i-1.  The longest path
##    has n-1 edges, unless there is a negative cycle, so we iterate to
##    that path length.  Then we do one more to check for negative cycles.
    for i in range (numNodes+1):
        for destNode in inNodes:
            if (destNode != sourceNode):
                solveAProblem (i, sourceNode, destNode, numNodes)
        
##    Check for negative cycles.  Compare the iteration for
##    numNodes-1 with the iteration for numNodes.  They should be
##    the same.  If they differ at any node, there is a negative cycle!
    for i in range ( numNodes ):
        if solved [0][i] != solved[1][i]:
            negativeCycle = True
    
##    Now we have the set of shortest paths lengths from this
##    to all destNodes.  Just save the shortest path length to a
##    different node.  First set the path length to the same node
##    to the max, then find the shortest.

    bestSoFar = maxValue
    currentArray = (numNodes-1)%2
    solved [currentArray][sourceNode] = maxValue
    
    thisSol = maxValue
    for i in range ( numNodes+2 ):
        thisSol = solved [currentArray][i]
        if thisSol < bestSoFar:
            bestSoFar = thisSol
        
    shortestPerNode[sourceNode] = bestSoFar
    return

def solveAProblem (i, sourceNode, destNode, n):

    bestSoFar = solved[(i-1)%2][destNode]
        
    for inNode, weight in inNodes[destNode]:
        currentSol = solved[(i-1)%2][inNode] + weight 
        if currentSol < bestSoFar:
            bestSoFar = currentSol

    solved[i%2][destNode] = bestSoFar
    return 
     
    
def computeAllShortest ():
    
                    
    print "About to open  file "
##    f = open ("g3.Txt", 'r')
    f = open ("test.Txt", 'r')

##  Read the data file 
    readInData (f)
    numNodes = len(inNodes)
    
    print "len inNodes is ", len(inNodes)
##    print "inNodes ", inNodes
    print

    initializeSolutions (numNodes+1, maxValue)

    print "Initialization done, starting outer loop"

    doneNodes = 0
    for currentNode in nodes:
        computeOneShortest (currentNode, maxValue)
        doneNodes += 1
        if doneNodes % 10 == 0:
            print "Still working, done up to node ", doneNodes
    


    if negativeCycle:
        print "Found a negative cycle"
    else:
##        print "shortest per node is ", shortestPerNode
        shortestPerNode.sort()
        print "shortest on graph is ", shortestPerNode[0]




if (__name__ == "__main__"):

    computeAllShortest();

            

    
    import doctest
    doctest.testmod()

