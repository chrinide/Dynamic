
## Graph operations
items = []
solved = []
numItems = 0

    
def readInData (fileToRead):
## This reads the items with  values and weights from the file and puts
## them into the items list. 

    i = 0

    for line in fileToRead:

        thisItem = 0
        thisItemWeight = 0
        tempLine = line.split()
        thisItem = int(tempLine[0])
        thisItemWeight = int(tempLine[1])
        items.append (thisItemWeight)

        if i < 10:
            print i, " : ", items[i]
                            
        i += 1
            
    print "After reading file, found %d lines" % (i)
    
    return 

def initializeSolutions (n):
    for i in range (0, n+1):
        solved.append([])
        for j in range (0, n+1):
            solved[i].append(0)

    return 

def findSolution (i, j):
    solution = 0

    if (i <= j):
        if (i <= len(solved) and j <= len(solved[i])):
            solution = solved[i][j]
    
    return solution

def rememberSolution (i, j, solution):
    solved[i][j] = solution
    return 


def solveAProblem (i, s, n):

    if i + s > n:
        return

    print "solving i, s : ", i, s
    print "item weights : ", items[i-1:i+s]
    
    guesses = []
    bestGuess = 0

    psum = 0
    for k in range (i-1, i+s):
        psum += items[k]

    print "psum : ", psum

    for r in range (i, i+s+1):
        term1 = findSolution(i, r-1) 
        term2 = findSolution(r+1, i+s)
        thisSol = psum + term1 + term2
        print " - r = ", r, " term1 = ", term1, " term2 = ", term2, "guess = ", thisSol
        guesses.append(thisSol)

    print "pre-sorted guesses : ", guesses
    guesses.sort()
##    print "post-sorted guesses : ", guesses
    if len(guesses) > 0:
        bestGuess = guesses.pop(0)
        
##        rememberSolution (i, i+s, guesses.pop())
    else:
        bestGuess = psum
        
##        rememberSolution (i, i+s, psum)

    print "best guess is ", bestGuess

    rememberSolution (i, i+s, bestGuess)

    print "-----"

    return 
     
    
def computeTree ():
    
                    
    print "About to open  file "
    f = open ("bintree.Txt", 'r')

##  Read the data file 
    readInData (f)
    numItems = len(items)

    items.sort()
    
    print "len items is ", len(items)
    print "items ", items
    print
    

    initializeSolutions (numItems)

    for s in range (0, numItems):
        print " ====  s = ", s, " ===="
        for i in range (1, numItems+1):
            print "i = ", i
            if (i+s < numItems+1):
                solveAProblem (i, s, numItems)

##    for i in range (1, numItems+1):
##        for j in range(1, numItems+1):
##            solveAProblem (i, j)

    print items
    
    for row in solved:
        print row
##    print solved


        
    print
    print "final solution " , findSolution(1,numItems)
    print solved[1]
    print "numItems = ", numItems



if (__name__ == "__main__"):

    computeTree();

            

    
    import doctest
    doctest.testmod()

