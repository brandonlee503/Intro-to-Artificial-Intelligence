import sys
import collections
import heapq

# Global Variables
# TODO: Change these names
depthLimit        = 0
nodeCount         = 0
lastExpansion     = 0
totalNodesCreated = 0
supportedModes = ["bfs", "dfs", "iddfs", "astar"]

# Actions a state may take in the form of [missionary, cannibal]
possibleActions = [[1,0],[2,0],[0,1],[1,1],[0,2]]

# TODO: Update class
class Node():
    """An abstract entity representing a single state"""
    def __init__(self, leftBank, rightBank, depth, cost, parent, action):
        global totalNodesCreated
        totalNodesCreated += 1
        self.leftBank = leftBank
        self.rightBank = rightBank
        self.key = tuple(self.leftBank + self.rightBank)

        self.parent = parent
        self.action = action
        self.depth = depth
        self.cost = cost

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

# TODO: Update class
class Result():
    """An abstract entity representing a Result"""
    def __init__(self, startBank, endBank, action, endBoatSide):
        startBank[0] = startBank[0] - action[0]
        endBank[0] = endBank[0] + action[0]
        startBank[1] = startBank[1] - action[1]
        endBank[1] = endBank[1] + action[1]
        if endBoatSide == "left":
            self.rightBank = startBank
            self.leftBank = endBank
            self.rightBank[2] = 0
            self.leftBank[2] = 1
        else:
            self.rightBank = endBank
            self.leftBank = startBank
            self.rightBank[2] = 1
            self.leftBank[2] = 0
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
        updatedNode = Node(result.leftBank, result.rightBank, node.depth + 1, node.depth + 1, node, result.action)
        successorNodes.append(updatedNode)
    return successorNodes

    # successors = []
    # for result in successor_fn(node):
    #     newNode = Node(result.leftBank, result.rightBank, node, result.action, node.depth + 1, node.depth + 1)
    #     successors.append(newNode)
    # return successors

# Expand the current node
def expandNodeIDDFS(node):
    successorNodes = []
    for result in checkSuccessorsIDDFS(node):
        updatedNode = Node(result.leftBank, result.rightBank, node.depth + 1, node.depth + 1, node, result.action)
        successorNodes.append(updatedNode)
    return successorNodes

    # successors = []
    # for result in successor_fn(node):
    #     newNode = Node(result.leftBank, result.rightBank, node, result.action, node.depth + 1, node.depth + 1)
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
    if node.leftBank[2] == 1:
        startBank = list(node.leftBank)
        endBank = list(node.rightBank)
    else:
        startBank = list(node.rightBank)
        endBank = list(node.leftBank)

    # Perform action and check result
    startBank[0] = startBank[0] - action[0]
    endBank[0] = endBank[0] + action[0]
    startBank[1] = startBank[1] - action[1]
    endBank[1] = endBank[1] + action[1]

    # TODO: MAYBE ITS THIS?
    # If there's more cannibals on one side than missionaries, stop.
    # if ((startBank[0] == 0) or (startBank[1] <= startBank[0])) and (endBank[0] == 0 or (endBank[1] <= endBank[0])):
    #     return True
    # else:
    #     return False

    # Correct implementation
    if (startBank[0] < 0) or (startBank[1] < 0) or (endBank[0] < 0) or (endBank[1] < 0):
        return False
    elif ((startBank[0] == 0) or (startBank[0] >= startBank[1])) and (endBank[0] == 0 or (endBank[0] >= endBank[1])):
        return True
    else:
        return False

# Perform the action and update state
def executeAction(action, node):
    if node.leftBank[2] == 1:
        result = Result(list(node.leftBank), list(node.rightBank), action, "right")
    else:
        result = Result(list(node.rightBank), list(node.leftBank), action, "left")

    return result

# Based off of Graph Search
def breathFirstSearch(fringe, initialState, goalState):
    # TODO Change these names
    global nodeCount, lastExpansion, depthLimit, totalNodesCreated
    closedList = {}
    fringe.append(initialState)
    # TODO:
    print "fringe length: {0}".format(len(fringe))
    while True:
        if len(fringe) == 0:
            sys.exit("No Solution Path Found")

        # BFS
        current = fringe.popleft()

        # Check if we're in the goal state
        if (current.leftBank == goalState.leftBank) and (current.rightBank == goalState.rightBank):
            return current

        if not checkClosedList(current, closedList):
            nodeCount += 1
            closedList[current.key] = current.depth
            map(fringe.append, expandNode(current))

def depthFirstSearch(fringe, initialState, goalState):
    global nodeCount, lastExpansion, depthLimit, totalNodesCreated
    closedList = {}
    fringe.append(initialState)
    while True:
        if len(fringe) == 0:
            sys.exit("No Solution Path Found")

        # DFS
        current = fringe.pop()

        # Check if we're in the goal state
        if (current.leftBank == goalState.leftBank) and (current.rightBank == goalState.rightBank):
            return current

        if not checkClosedList(current, closedList):
            # Find better implementation
            if current.depth > 250:
                continue
            nodeCount += 1
            closedList[current.key] = current.depth
            map(fringe.append, expandNode(current))

def iterativeDeepeningDFS(fringe, initialState, goalState):
    global nodeCount, lastExpansion, depthLimit, totalNodesCreated
    closedList = {}
    fringe.append(initialState)
    while True:
        if len(fringe) == 0:
            if depthLimit > 250:
                sys.exit("Depth Limit Reached!")
            lastExpansion = 0
            fringe.append(initialState)
            depthLimit += 1
            totalNodesCreated = 0
            closedList = {}
            continue

        # IDDFS
        current = fringe.pop()

        # Check if we're in the goal state
        if (current.leftBank == goalState.leftBank) and (current.rightBank == goalState.rightBank):
            return current

        if not checkClosedList(current, closedList):
            nodeCount += 1
            closedList[current.key] = current.depth
            # TODO: This represents reference.py correctly, maybe change it?g
            map(fringe.append, expandNodeIDDFS(current))

def aStarSearch(fringe, initialState, goalState):
    global nodeCount, lastExpansion, depthLimit, numOfNodesCreated
    closedList = {}
    fringe.push(initialState, initialState.cost)

    while True:
        if len(fringe) == 0:
            sys.exit("No Solution Path Found")

        # A*
        current = fringe.pop()

        # Check if we're in the goal state
        if (current.leftBank == goalState.leftBank) and (current.rightBank == goalState.rightBank):
            return current

        if not checkClosedList(current, closedList):
            nodeCount += 1
            closedList[current.key] = current.depth
            map(lambda i: fringe.push(i, i.cost + aStarHueristic(i, goalState)), expandNode(current))
# map(lambda x: fringe.push(x, x.cost + getHueristic(x, goalState)), expand(currentNode))

# Find hueristic to add with path cost
def aStarHueristic(current, goalState):
    # Check boat bank
    # TODO CHANGE ME
    if goalState.rightBank[2] == 1:
        hueristic = (current.leftBank[0] + current.leftBank[1]) - 1
    else:
        hueristic = (current.rightBank[0] + current.rightBank[1]) - 1
    return hueristic

# # Returns the hueristic to get added to the pathcost
# def getHueristic(currentNode, goalNode):
#     # Determine which side the boat is on
#     if goalNode.rightSide[2] == 1:
#         retval = (currentNode.leftSide[0] + currentNode.leftSide[1]) - 1
#     else:
#         retval = (currentNode.rightSide[0] + currentNode.rightSide[1]) - 1
#     return retval
#####

# def uninformedSearch(initialNode, goalNode, fringe):
#     global nodeCount, lastExpansion, depthLimit, numOfNodesCreated
#     closedList = {}
#     if mode == "a*":
#         fringe.push(initialNode, initialNode.cost)
#     else:
#         fringe.append(initialNode)
#     while True:
#         if len(fringe) == 0:
#             # When in iddfs mode, increment depthLimit and restart search
#             if mode == "iddfs":
#                 if depthLimit > 500:
#                     exit(1)
#                 lastExpansion = 0
#                 fringe.append(initialNode)
#                 depthLimit += 1
#                 numOfNodesCreated = 0
#                 closedList = {}
#                 continue
#             else:
#                 sys.exit("No Solution Path Found")
#
#         if mode == "bfs":
#             currentNode = fringe.popleft()
#         else:
#             currentNode = fringe.pop()
#
#         if goalTest(currentNode, goalNode):
#             return currentNode
#
#         if not inClosedList(currentNode, closedList):
#             if mode == "dfs" and currentNode.depth >= 500:
#                 continue
#             nodeCount += 1
#             closedList[currentNode.key] = currentNode.depth
#             if mode == "a*":
#                 map(lambda x: fringe.push(x, x.cost + getHueristic(x, goalState)), expand(currentNode))
#             else:
#                 map(fringe.append, expand(currentNode))

##########
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
    # TODO: Change
    initialState = Node(map(int, initialStateData[0].strip('\n').split(',')), map(int, initialStateData[1].strip('\n').split(',')), 0, 0, None, None)
    goalStateData = getFileState(fileGoalState)
    goalState = Node(map(int, goalStateData[0].strip('\n').split(',')), map(int, goalStateData[1].strip('\n').split(',')), 0, 0, None, None)

    # Execute based on mode
    if mode in supportedModes:
        if mode == "bfs":
            # TODO: Change datastructure if possible
            fringe = collections.deque()
            resultState = breathFirstSearch(fringe, initialState, goalState)
        if mode == "dfs":
            fringe = collections.deque()
            resultState = depthFirstSearch(fringe, initialState, goalState)
        if mode == "iddfs":
            fringe = collections.deque()
            resultState = iterativeDeepeningDFS(fringe, initialState, goalState)
        if mode == "astar":
            # TODO: Change datastructure if possible
            fringe = PriorityQueue()
            resultState = aStarSearch(fringe, initialState, goalState)
    else:
        sys.exit("Mode not supported!")

    print "Total Expanded Nodes: {0}".format(nodeCount)
    print "Solution Path Length: {0}".format(len(findSolutionPath(resultState)))
    print findSolutionPath(resultState)
    printToFile(fileOutput, findSolutionPath(resultState))

main()
