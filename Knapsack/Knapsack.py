
## Graph operations
items = []
solvedA = {}
solvedB = {}


    
def readInData (fileToRead):
## This reads the items with  values and weights from the file and puts
## them into the nodes dictionary and the edges list. 

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
    for w in range (0, size+1):
        solvedA[w] = 0
        solvedB[w] = 0
    return 

def findSolution (i, w, usingA):
    solution = 0

    if usingA:
        solution = solvedA[w]
    else:
        solution = solvedB[w]

    
    return solution

def rememberSolution (i, w, solution, usingA):
    if usingA:
        solvedA[w] = solution
    else:
        solvedB[w] = solution
    return 


def solveAProblem (i, w, usingA):

    itemValue, itemWeight = items[i]
    choice1 = findSolution (i-1, w, not usingA)
    choice2 = 0
    if (w - itemWeight >= 0):
        choice2 = findSolution (i-1, w-itemWeight, not usingA) + itemValue
            
    choice = max(choice1, choice2)
    rememberSolution(i, w, choice, usingA)


    return 


       
    
def fillKnapsack ():
    
                    
    print "About to open  file "
##    f = open ("knapsack_big.Txt", 'r')
    f = open ("knapsack1.Txt", 'r')
##    f = open ("knaptest1.Txt", 'r')

##  Read the data file 
    kSize = readInData (f)
    numItems = len(items)
    print "len items is ", len(items)
    print "knapsack size is ", kSize

    initializeSolutions (numItems, kSize)

    usingA = False


    for itemNumber in range (1, numItems):
        usingA = not usingA
        for residualWeight in range(kSize):
            solveAProblem (itemNumber, residualWeight, usingA)
        if (itemNumber % 20 == 0):
            print "Still working, itemNumber ", itemNumber
        


        
    print findSolution(numItems-1,kSize-1, usingA)



if (__name__ == "__main__"):

    fillKnapsack();

            

    
    import doctest
    doctest.testmod()

