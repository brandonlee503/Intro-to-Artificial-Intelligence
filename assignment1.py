import sys
import collections

# Global Variables
depthLimit        = 0
nodeCount         = 0
lastExpansion     = 0
totalNodesCreated = 0
supportedModes = ["bfs", "dfs", "iddfs", "a*"]

# Actions a state may take in the form of [missionary, cannibal]
possibleActions = [[1,0],[2,0],[0,1],[1,1],[0,2]]


# TODO: Update class
class Node():
    """An abstract entity representing a single state"""
    def __init__(self, leftSide, rightSide, parent, action, depth, pathcost):
        global totalNodesCreated
        self.leftSide = leftSide
        self.rightSide = rightSide
        self.parent = parent
        self.action = action
        self.depth = depth
        self.pathcost = pathcost
        self.key = tuple(self.leftSide + self.rightSide)
        totalNodesCreated += 1

# TODO: Update class
class PriorityQueue:
    """An abstract entity representing a priority queue"""
    def __init__(self):
        self._queue = []
        self._index = 0

    def __len__(self):
        return len(self._queue)

    def push(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]

    def __len__(self):
        return len(self._queue)

# TODO: Update class
class Result():
    """An abstract entity representing a Result"""
    def __init__(self, startSide, endSide, action, endBoatSide):
        startSide[0] = startSide[0] - action[0]
        startSide[1] = startSide[1] - action[1]
        endSide[0] = endSide[0] + action[0]
        endSide[1] = endSide[1] + action[1]
        if endBoatSide == "right":
            self.rightSide = endSide
            self.leftSide = startSide
            self.rightSide[2] = 1
            self.leftSide[2] = 0
        else:
            self.rightSide = startSide
            self.leftSide = endSide
            self.rightSide[2] = 0
            self.leftSide[2] = 1
        self.action = action

def getFileState(file):
    with open(file) as theFile:
        stateData = theFile.readlines()
    return stateData

# Check to see if current node is in the closed list
# TODO: Find a way to update this
def checkClosedList(node, closedList):
    if node.key in closedList:
        if node.depth >= closedList[node.key]:
            return True
    else:
        return False

# Expand the current node
def expandNode(node):
    successorNodes = []
    for result in checkSuccessors(node):
        updatedNode = Node(result.leftSide, result.rightSide, node, result.action, node.depth + 1, node.depth + 1)
        successorNodes.append(updatedNode)
    return successorNodes

    # successors = []
    # for result in successor_fn(node):
    #     newNode = Node(result.leftSide, result.rightSide, node, result.action, node.depth + 1, node.depth + 1)
    #     successors.append(newNode)
    # return successors

# Checks all possible successors
def checkSuccessors(node):
    global possibleActions
    #TODO: Update this
    # if mode == "iddfs":
    #     if node.depth == depthLimit:
    #         return []
    allowedActions = filter(lambda x: checkAction(x, node), possibleActions)
    results = map(lambda y: executeAction(y, node), allowedActions)
    return results

def checkSuccessorsIDDFS(node):
    global possibleActions
    if node.depth == depthLimit:
        return []
    allowedActions = filter(lambda x: checkAction(x, node), possibleActions)
    results = map(lambda y: executeAction(y, node), allowedActions)
    return results

# Check if action is valid within game
def checkAction(action, node):
    # Check which side boat is
    if node.leftSide[2] == 1:
        startSide = list(node.leftSide)
        endSide = list(node.rightSide)
    else:
        startSide = list(node.rightSide)
        endSide = list(node.leftSide)

    # Perform action and check result
    startSide[0] = startSide[0] - action[0]
    endSide[0] = endSide[0] + action[0]
    startSide[1] = startSide[1] - action[1]
    endSide[1] = endSide[1] + action[1]

    # If there's more cannibals on one side than missionaries, stop.
    if ((startSide[0] == 0) or (startSide[1] <= startSide[0])) and (endSide[0] == 0 or (endSide[1] <= endSide[0])):
        return True
    else:
        return False

    # Correct implementation
    # if (startSide[0] < 0) or (startSide[1] < 0) or (endSide[0] < 0) or (endSide[1] < 0):
    #     return False
    # elif ((startSide[0] == 0) or (startSide[0] >= startSide[1])) and (endSide[0] == 0 or (endSide[0] >= endSide[1])):
    #     return True
    # else:
    #     return False

# Perform the action and update state
def executeAction(action , node):
    if node.leftSide[2] == 1:
        result = Result(list(node.leftSide), list(node.rightSide), action, "right")
    else:
        result = Result(list(node.rightSide), list(node.leftSide), action, "left")

    return result

# Based off of Graph Search
def breathFirstSearch(initialState, goalState, fringe):
    global nodeCount, lastExpansion, depthLimit, totalNodesCreated
    closedList = {}
    fringe.append(initialState)
    while True:
        if len(fringe) == 0:
            sys.exit("No solution found!")

        # BFS
        currentNode = fringe.popleft()

        # Check if we're in the goal state
        if (currentNode.leftSide == goalState.leftSide) and (currentNode.rightSide == goalState.rightSide):
            return currentNode

        if not checkClosedList(currentNode, closedList):
            nodeCount += 1
            closedList[currentNode.key] = currentNode.depth
            map(fringe.append, expandNode(currentNode))

# Trace through parents to find path of solution node
def findSolutionPath(node):
    pathToSolution = []
    current = node
    while True:
        try:
            if current.parent != None:
                pathToSolution.append(current.action)
        except:
            break
        current = current.parent
    return pathToSolution #pathToSolution[::-1]

def printToFile(file, solutionPath):
    f = open(file, 'w')
    f.write(str(solutionPath))
    f.write('\n')
    f.close()

def main():

    # http://stackoverflow.com/questions/4033723/how-do-i-access-command-line-arguments-in-python
    # Get command line arguments
    fileInitialState = sys.argv[1]
    fileGoalState    = sys.argv[2]
    mode             = sys.argv[3]
    fileOutput       = sys.argv[4]

    # File IO
    initialStateData = getFileState(fileInitialState)
    initialState = Node(map(int, initialStateData[0].strip('\n').split(',')), map(int, initialStateData[1].strip('\n').split(',')), None, None, 0, 0)
    goalStateData = getFileState(fileGoalState)
    goalState = Node(map(int, goalStateData[0].strip('\n').split(',')), map(int, goalStateData[1].strip('\n').split(',')), None, None, 0, 0)

    # Execute based on mode
    if mode in supportedModes:
        if mode == "a*":
            # TODO: Change datastructure if possible
            fringe = PriorityQueue()
        if mode == "bfs":
            fringe = collections.deque()
            resultState = breathFirstSearch(initialState, goalState, fringe)
    else:
        sys.exit("Mode not supported!")

    print "Total Expanded Nodes: {0}".format(nodeCount)
    print "Solution Path Length: {0}".format(len(findSolutionPath(resultState)))
    print findSolutionPath(resultState)
    printToFile(fileOutput, findSolutionPath(resultState))

main()
