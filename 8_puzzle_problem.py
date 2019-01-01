import heapq

inpFile = input('Enter the name of an input file: ')
# open file for reading
f = open(inpFile, 'r')

# initialize matrices to store positions of coordinates
# map number with coordinate
initialMatrix = []
goalMatrix = []

# insert coordinates
for x in range(3):
    line = f.readline().split()
    initialMatrix.append(line)

f.readline()

for x in range(3):
    line = f.readline().split()
    goalMatrix.append(line)

# helper function to create dictionary of state
def makeDict(matrix):
    coordinate_dict = {}
    for x, row in enumerate(matrix):
        for y, val in enumerate(row):
            coordinate_dict[val] = (x, y)
    return coordinate_dict

goalMap = makeDict(goalMatrix) # create map to avoid repeated calculations

# function for calculating manhattan distance
def manDist(interMatrix, goalMatrix):
    totalDist = 0
    interMap = makeDict(interMatrix)
    for key in interMap:
        if key != '0':
            totalDist += abs(interMap[key][0] - goalMap[key][0])
            totalDist += abs(interMap[key][1] - goalMap[key][1])

    return totalDist

# write file
# writeFile(initialMatrix,goalMatrix, 5, 'N', ['U','U','L','D','R'])
def writeFile(initialMatrix, goalMatrix, depth, nodesGen, moves):
    file = open('output.txt', 'w')
    for line in initialMatrix:
        file.write(' '.join(line) + '\n')
    file.write('\n')

    for line in goalMatrix:
        file.write(' '.join(line) + '\n')
    file.write('\n')

    file.writelines(map(lambda s: s + '\n', [str(depth), str(nodesGen),\
        ' '.join(moves)]))

# expand function takes in matrix and location of zero (y,x)
def expand(matrix, locZero):
    neighbors = []
    y = locZero[0]
    x = locZero[1]
    # if neighbor is valid, add it to return list
    if 0 <= y - 1 < 3: # up
        # create matrix with swapped coordinates, append
        UMatrix = [row[:] for row in matrix]
        UMatrix[y-1][x],UMatrix[y][x] = UMatrix[y][x],UMatrix[y-1][x]
        neighbors.append([UMatrix,'U'])

    if 0 <= x + 1 < 3: # right
        RMatrix = [row[:] for row in matrix]
        RMatrix[y][x+1],RMatrix[y][x] = RMatrix[y][x],RMatrix[y][x+1]
        neighbors.append([RMatrix,'R'])

    if 0 <= y + 1 < 3: # down
        DMatrix = [row[:] for row in matrix]
        DMatrix[y+1][x],DMatrix[y][x] = DMatrix[y][x],DMatrix[y+1][x]
        neighbors.append([DMatrix,'D'])

    if 0 <= x - 1 < 3: # left
        LMatrix = [row[:] for row in matrix]
        LMatrix[y][x-1],LMatrix[y][x] = LMatrix[y][x],LMatrix[y][x-1]
        neighbors.append([LMatrix,'L'])

    return neighbors

def func(initialMatrix, goalMatrix):
    # variables
    nodeGen = 1 # 1 for root node
    depth = 0
    explored = set() # set of explored states
    frontier = [] # heap of tuples(number,matrix)
    
    # f(n) = g(n) + h(n)
    # initialize frontier with f(n), initialMatrix and additional info
    heapq.heappush(frontier, (manDist(initialMatrix, goalMatrix), initialMatrix, depth,\
            []))

    # while true
    while True:
        if len(frontier) == 0: return False
        currMatrix = heapq.heappop(frontier)

        # check if goal state
        if currMatrix[1] == goalMatrix:
            writeFile(initialMatrix, goalMatrix, currMatrix[2], nodeGen,\
                    currMatrix[3])
            return True

        # store current matrix in explored set
        explored.add(str(currMatrix[1]))

        # find child nodes of curr
        currMap = makeDict(currMatrix[1])
        locZero = currMap['0']

        neighbors = expand(currMatrix[1], locZero)

        for neighbor in neighbors:
            # make copy of current directions to append to
            currDirections = list(currMatrix[3])

            if str(neighbor[0]) in explored: continue


            #calculate neighbors man dist
            neighborDist = manDist(neighbor[0], goalMatrix)
            flag = False # tracks if neighbor is in frontier

            # if already in frontier, then get man dist and depth
            # calculate f(n) and replace explored or frontier value if better
            for entry in range(len(frontier)):
                if neighbor[0] == frontier[entry][1]: 
                    flag = True
                    f = neighborDist + currMatrix[2] + 1 # man dist + depth
                    if f < frontier[entry][0]:
                        del frontier[entry]
                        nodeGen += 1
                        currDirections.append(neighbor[1])
                        heapq.heappush(frontier, (f, neighbor[0],\
                            currMatrix[2]+1, currDirections))
                    break

            # else if not in explored or frontier, then calculate f(n), and
            # place on frontier
            if flag == False:
                nodeGen += 1
                currDirections.append(neighbor[1])
                f = manDist(neighbor[0],goalMatrix) + currMatrix[2] + 1 
                heapq.heappush(frontier, (f, neighbor[0], currMatrix[2] + 1,\
                    currDirections))

func(initialMatrix, goalMatrix)
