# Brandon Lee
# CS 331 Intro to Artificial Intelligence
# Assignment 1 - Cannibals and Missionaries Puzzle
import sys
import collections
import heapq

# Rename x1
# Add helper functions x2
# Restructure (top down and maybe more) x3
# Add references x2
# Change it up x3

# Global Variables
totalNodesCreated  = 0
totalExpandedNodes = 0
maximumDepth       = 0

# Actions a state may take in the form of [missionary, cannibal]
possibleMoves = [[1,0],[2,0],[0,1],[1,1],[0,2]]
supportedModes = ["bfs", "dfs", "iddfs", "astar"]

# https://www.safaribooksonline.com/library/view/python-cookbook-3rd/9781449357337/ch01s05.html
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

class Node():
    """An abstract entity representing a single state"""
    def __init__(self, leftBank, rightBank, depth, cost, parent, action):

        # Global counter
        global totalNodesCreated
        totalNodesCreated += 1

        # Puzzle banks
        self.leftBank = leftBank
        self.rightBank = rightBank
        self.state = tuple(self.leftBank + self.rightBank)

        # Other attributes
        self.depth = depth
        self.cost = cost
        self.parent = parent
        self.action = action

# x3
class Result():
    """An abstract entity representing a result"""
    def __init__(self, startBank, endBank, action, boatEndBank):

        startBank[0] = startBank[0] - action[0]
        endBank[0] = endBank[0] + action[0]
        startBank[1] = startBank[1] - action[1]
        endBank[1] = endBank[1] + action[1]

        if boatEndBank == "left":
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
    """Read test files for data"""
    with open(file) as theFile:
        stateData = theFile.readlines()
    return stateData

def expandNode(node):
    """Expand the current node"""
    global possibleMoves
    successorNodes = []

    validAction = filter(lambda i: checkAction(i, node), possibleMoves)
    expandedNodes = map(lambda j: executeAction(j, node), validAction)

    for successor in expandedNodes:
        updatedNode = Node(successor.leftBank, successor.rightBank, node.depth + 1, node.depth + 1, node, successor.action)
        successorNodes.append(updatedNode)
    return successorNodes

def expandNodeIDDFS(node):
    """Expand the current node (IDDFS Version)"""
    global possibleMoves
    successorNodes = []

    if node.depth == maximumDepth:
        expandedNodes = []
    else:
        validAction = filter(lambda i: checkAction(i, node), possibleMoves)
        expandedNodes = map(lambda j: executeAction(j, node), validAction)

    for successor in expandedNodes:
        updatedNode = Node(successor.leftBank, successor.rightBank, node.depth + 1, node.depth + 1, node, successor.action)
        successorNodes.append(updatedNode)
    return successorNodes

def checkAction(action, node):
    """Check if action is valid within game"""
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

    # Compare number of missionaires versus cannibals
    if (startBank[0] < 0) or (startBank[1] < 0) or (endBank[0] < 0) or (endBank[1] < 0):
        return False
    elif ((startBank[0] == 0) or (startBank[0] >= startBank[1])) and (endBank[0] == 0 or (endBank[0] >= endBank[1])):
        return True
    else:
        return False

def executeAction(action, node):
    """Perform the action and update state"""
    if node.leftBank[2] == 1:
        result = Result(list(node.leftBank), list(node.rightBank), action, "right")
    else:
        result = Result(list(node.rightBank), list(node.leftBank), action, "left")
    return result

def breathFirstSearch(fringe, initialState, goalState):
    """BFS Implmentation - Based off of Graph Search pseudocode"""
    global totalNodesCreated, totalExpandedNodes, maximumDepth
    closedList = {}
    fringe.append(initialState)
    while True:
        if len(fringe) == 0:
            sys.exit("No Solution Path Found")

        # Remove from fringe
        current = fringe.popleft()

        # Check if we're in the goal state
        if (current.leftBank == goalState.leftBank) and (current.rightBank == goalState.rightBank):
            return current

        # Check if in closed list and expand when necessary
        if current.state in closedList and current.depth >= closedList[current.state]:
            continue
        else:
            closedList[current.state] = current.depth
            map(fringe.append, expandNode(current))
            totalExpandedNodes += 1

def depthFirstSearch(fringe, initialState, goalState):
    """DFS Implmentation - Based off of Graph Search pseudocode"""
    global totalNodesCreated, totalExpandedNodes, maximumDepth
    closedList = {}
    fringe.append(initialState)
    while True:
        if len(fringe) == 0:
            sys.exit("No Solution Path Found")

        # Remove from fringe
        current = fringe.pop()

        # Check if we're in the goal state
        if (current.leftBank == goalState.leftBank) and (current.rightBank == goalState.rightBank):
            return current

        # Check if in closed list and expand when necessary
        if current.state in closedList and current.depth >= closedList[current.state]:
            continue
        else:
            if current.depth > 400:
                continue
            closedList[current.state] = current.depth
            map(fringe.append, expandNode(current))
            totalExpandedNodes += 1

def iterativeDeepeningDFS(fringe, initialState, goalState):
    """IDDFS Implmentation - Based off of Graph Search pseudocode"""
    global totalNodesCreated, totalExpandedNodes, maximumDepth
    closedList = {}
    fringe.append(initialState)
    while True:
        if len(fringe) == 0:
            if maximumDepth > 400:
                sys.exit("Depth Limit Reached!")
            closedList = {}
            maximumDepth += 1
            totalNodesCreated = 0
            fringe.append(initialState)
            continue

        # Remove from fringe
        current = fringe.pop()

        # Check if we're in the goal state
        if (current.leftBank == goalState.leftBank) and (current.rightBank == goalState.rightBank):
            return current

        # Check if in closed list and expand when necessary
        if current.state in closedList and current.depth >= closedList[current.state]:
            continue
        else:
            closedList[current.state] = current.depth
            map(fringe.append, expandNodeIDDFS(current))
            totalExpandedNodes += 1

def aStarSearch(fringe, initialState, goalState):
    """A* Implmentation - Based off of Graph Search pseudocode"""
    global totalNodesCreated, totalExpandedNodes, maximumDepth
    closedList = {}
    fringe.push(initialState, initialState.cost)

    while True:
        if len(fringe) == 0:
            sys.exit("No Solution Path Found")

        # Remove from fringe
        current = fringe.pop()

        # Check if we're in the goal state
        if (current.leftBank == goalState.leftBank) and (current.rightBank == goalState.rightBank):
            return current

        # Check if in closed list and expand when necessary
        if current.state in closedList and current.depth >= closedList[current.state]:
            continue
        else:
            closedList[current.state] = current.depth
            map(lambda i: fringe.push(i, i.cost + aStarHeuristic(i, goalState)), expandNode(current))
            totalExpandedNodes += 1

# http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html#S7
def aStarHeuristic(current, goalState):
    """Find heuristic to add with path cost"""
    # Check boat bank
    if goalState.leftBank[2] == 1:
        heuristic = (current.rightBank[0] + current.rightBank[1]) / 2
    else:
        heuristic = (current.leftBank[0] + current.leftBank[1]) / 2
    return heuristic

# http://stackoverflow.com/questions/8922060/how-to-trace-the-path-in-a-breadth-first-search
def findSolutionPath(node):
    """Trace through parents to find path of solution node"""
    pathToSolution = []
    current = node
    while True:
        try:
            if current.parent != None:
                pathToSolution.append(current.action)
        except:
            break
        current = current.parent
    return pathToSolution

def printToUser(resultState):
    """Print results to console"""
    print "Total Expanded Nodes: {0}".format(totalExpandedNodes)
    print "Solution Path Length: {0}".format(len(findSolutionPath(resultState)))
    print findSolutionPath(resultState)

def createNodeWithData(data):
    return Node(map(int, data[0].strip('\n').split(',')), map(int, data[1].strip('\n').split(',')), 0, 0, None, None)

def main():
    # Get command line arguments
    fileInitialState = sys.argv[1]
    fileGoalState    = sys.argv[2]
    mode             = sys.argv[3]
    fileOutput       = sys.argv[4]

    # File IO
    initialStateData = getFileState(fileInitialState)
    goalStateData = getFileState(fileGoalState)

    # Create essential states
    initialState = createNodeWithData(initialStateData)
    goalState = createNodeWithData(goalStateData)

    # Execute based on mode
    if mode in supportedModes:
        if mode == "astar":
            fringe = PriorityQueue()
            resultState = aStarSearch(fringe, initialState, goalState)
        if mode == "bfs":
            fringe = collections.deque()
            resultState = breathFirstSearch(fringe, initialState, goalState)
        if mode == "dfs":
            fringe = collections.deque()
            resultState = depthFirstSearch(fringe, initialState, goalState)
        if mode == "iddfs":
            fringe = collections.deque()
            resultState = iterativeDeepeningDFS(fringe, initialState, goalState)
    else:
        sys.exit("Mode not supported!")

    # Show user the results
    printToUser(resultState)

    # Print the solution to a readable file
    outFile = open(fileOutput, 'w')
    outFile.write(str(findSolutionPath(resultState)))
    outFile.write('\n')
    outFile.close()

main()

# TODO: Walk through one last time for each algorithm, restructre, then test
