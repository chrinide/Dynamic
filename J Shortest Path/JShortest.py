
## Dynamic Programming approach to finding the shortest paths in a
## graph that contains negative edge lengths

nodes = {}
inNodes = {}
nodeWeights = []
maxValue = 0
shortestPerNode = []
negativeCycle = False
shortest = []

edges = []

    
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
            if weight * weight > maxEdgeWeight * maxEdgeWeight:
                maxEdgeWeight = weight

            if dest not in inNodes:
                inNodes[dest] = {}

            inNodes[dest][source] = weight
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
    global nodeWeights
    nodeWeights = []

    for i in range (0, 2):
        nodeWeights.append([])
        for j in range (0, n+2):
            nodeWeights[i].append(initValue)

    for j in range (0, n+2):
        shortestPerNode.append(initValue)
        shortest.append(initValue)

    return 

def resetSolutions (n, initValue):
    global nodeWeights

    for i in range (0, 2):
        for j in range (0, n+2):
            nodeWeights[i][j] = initValue
        
    return 

def resetShortest (n, initValue):
    global shortest

    for i in range (0, n+2):
        shortest[i] = initValue
        
    return 

# Compute the set of shortest paths from sourceNode to the rest
# of the nodes in the graph, as compared to zero.  These are the
# node weights to use.
def computeNodeWeights ():

    global negativeCycle

    numNodes = len(inNodes)
    resetSolutions (numNodes+1, 0)

##    For each node, find the shortest path from phantom vertex s, which
##    has a phatnom edge of length 0 to every node in the graph.
##    This algorithm builds up shortest paths of length i, using the
##    information about shortest paths of length i-1.  The longest path
##    has n-1 edges, unless there is a negative cycle, so we iterate to
##    that path length.  Then we do one more to check for negative cycles.
    for i in range (numNodes+1):
        for destNode in inNodes:
            solveAProblem (i, destNode, numNodes)
        
##    Check for negative cycles.  Compare the iteration for
##    numNodes-1 with the iteration for numNodes.  They should be
##    the same.  If they differ at any node, there is a negative cycle!
    for i in range ( numNodes ):
        if nodeWeights [0][i] != nodeWeights[1][i]:
            negativeCycle = True
    
    return

# Compute the set of shortest paths from sourceNode to the rest
# of the nodes in the graph. 
def computeOneShortest (sourceNode):

    global shortest
    resetShortest(len(nodes), maxValue)
    nodesProcessed = {}
    nodesToGo = {}
    
    for n in nodes:
        nodesToGo[n] = 1

    # Set up initial state, with just the source node in the
    # already processed list, with path of length 0.

    nodesProcessed[sourceNode] = 1
    del nodesToGo[sourceNode]
    shortest[sourceNode] = 0
    temp = 0
    done = False

    if len(nodes) < 200:
        print "Note: under 200 nodes"
    if len(edges) < 200:
        print "Note: under 200 edges"

    while (nodesToGo and not done):
        currentShortest = -1
        thisPathDist = -1
        edgeToChoose = -1
##        print "to go: ", nodesToGo

        for edge in edges:
            source, dest, weight = edge
            if (source in nodesProcessed) and (dest in nodesToGo):
                thisPathDist = shortest[source] + weight
                if (currentShortest < 0) or (currentShortest > thisPathDist):
                    edgeToChoose = edge
                    currentShortest = thisPathDist
                

        if edgeToChoose != -1:
            source, dest, weight = edgeToChoose
            weight += shortest[source]
            nodesProcessed[dest] = weight
            shortest[dest] = weight
            del nodesToGo[dest]
        else:
##            print "could not reach nodes ", nodesToGo, " from node ", sourceNode
            done = True

##    print "after loop shortest is ", shortest

##    return shortest
    return 


def solveAProblem (i, destNode, n):

    bestSoFar = nodeWeights[(i-1)%2][destNode]
        
    for inNode in inNodes[destNode]:
        currentSol = nodeWeights[(i-1)%2][inNode] + inNodes[destNode][inNode]
        if currentSol < bestSoFar:
            bestSoFar = currentSol

    nodeWeights[i%2][destNode] = bestSoFar
    return 
     
    
def computeAllShortest ():
    
                    
    print "About to open  file "
    f = open ("g2.Txt", 'r')
##    f = open ("test.Txt", 'r')

##  Read the data file 
    readInData (f)
    numNodes = len(inNodes)
    
    print "len inNodes is ", len(inNodes)
##    print "inNodes ", inNodes
    print

    initializeSolutions (numNodes+1, maxValue)

##    First, run Bellman-Ford once to get the vertex weights.  Pretending
##    there is a phantom vertex s with an edge of length zero to every
##    node, run from sourceNode s.  Use those shortest path lengths as the
##    vertex weights.  Also, check for a negative cycle.
##
    computeNodeWeights ()

    if negativeCycle:
        print "Found a negative cycle"
        return

    
##    Now that we have the vertex weights, adjust the edge weights
##    accordingly.  Add each edge to the edges list.

    for destNode in inNodes:
        for inNode in inNodes[destNode]:
            weight = inNodes[destNode][inNode] + \
                nodeWeights[0][inNode] - nodeWeights[0][destNode]
            inNodes[destNode][inNode] = weight
            edges.append ( (inNode, destNode, weight) )

    print "Done with computing vertex weights and adjusting edges"
    inNodes.clear()


##    Now we have an adjusted graph with non-negative edge weights.  Run
##    Dijkstra's algorithm on this graph to get the all-pairs shortest
##    path lengths.

    i = 0

    for sourceNode in nodes:
        computeOneShortest(sourceNode)
        bestSoFar = maxValue
        for dest in nodes:
            # readjust path cost
            adjustedWeight = shortest[dest] - \
                                nodeWeights[0][sourceNode] + \
                                nodeWeights[0][dest]
            if adjustedWeight < bestSoFar:
                bestSoFar = adjustedWeight
                
        shortestPerNode[sourceNode] = bestSoFar
##        print " Shortest for node ", sourceNode, " : ", bestSoFar
        i += 1
        if i % 10 == 0:
            print "still working, i is now ", i

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

