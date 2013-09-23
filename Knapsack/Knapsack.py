
## Graph operations
items = []
solved = {}


    
def readInData (fileToRead):
## This reads the nodes and edges from the given file and puts
## them into the nodes dictionary and the edges list.  Initially set
## all of the leader nodes to the negative of the node number
## so each node is in its own cluster

    i = 0
    numItems = 0
    knapsackSize = 0

    for line in fileToRead:
        if (i == 0):
            tempLine = line.split()
            knapsackSize = int(tempLine[0])
            numItems = int(tempLine[1])
            print ("Knapsack size is ", knapsackSize, " for ", numItems, " items")
            items.append( (0, 0) )

        else:
            thisItem = 0
            thisItemSize = 0
            tempLine = line.split()
            thisItem = int(tempLine[0])
            thisItemSize = int(tempLine[1])
            items.append ( (thisItem, thisItemSize) )

##            if i < 10:
##                print i, " : ", items[i]
                            
        i += 1
            
    print "After reading file, found %d lines" % (i)
    
    return knapsackSize

def initializeSolutions (n, size):
    for itemNumber in range (0, n):
        solved[itemNumber] = []
    for w in range (0, size+1):
        solved[0].append(0)
    return 

def findSolution (i, w):
    solution = 0
    itemValue, itemWeight = items[i]
    iSolutions = solved[i]
##    if w in iSolutions:
    solution = iSolutions[w]
    return solution

def rememberSolution (i, w, solution):
##    if solution != 0:
    iSolutions = solved[i]
    iSolutions.insert(w, solution)
##        solved[i][w] = solution
    return 


def solveAProblem (i, w):

    itemValue, itemWeight = items[i]
    choice1 = findSolution (i-1, w)
    choice2 = 0
    if (w - itemWeight > 0):
        choice2 = findSolution (i-1, w-itemWeight) + itemValue
            
    choice = max(choice1, choice2)
    rememberSolution(i, w, choice)


    return 


       
    
def fillKnapsack ():
    
                    
    print "About to open  file "
##    f = open ("knapsack_big.Txt", 'r')
    f = open ("knapsack1.Txt", 'r')

##  Read the data file 
    kSize = readInData (f)
    numItems = len(items)
    print "len items is ", len(items)
    print "knapsack size is ", kSize

    initializeSolutions (numItems, kSize)


    for itemNumber in range (1, numItems):
        for residualWeight in range(kSize):
            solveAProblem (itemNumber, residualWeight)

    
    print solved[numItems-1][kSize-1]



if (__name__ == "__main__"):

    fillKnapsack();

            

    
    import doctest
    doctest.testmod()

