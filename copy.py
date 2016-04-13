import sys, collections, heapq

# Rename
# Add helper functions
# Restructure
# Add references

# Global Variables
fileInitialState  = None
fileGoalState     = None
mode              = None
outputFile        = None
possibleActions   = [[1,0],[2,0],[0,1],[1,1],[0,2]]
depthLimit        = 0
nodeCount         = 0
lastExpansion     = 0
numOfNodesCreated = 0
goalState = None

# Node that represents a state
class Node():
    def __init__(self, leftSide, rightSide, parent, action, depth, pathcost):
        global numOfNodesCreated
        self.leftSide = leftSide
        self.rightSide = rightSide
        self.parent = parent
        self.action = action
        self.depth = depth
        self.pathcost = pathcost
        self.key = tuple(self.leftSide + self.rightSide)
        numOfNodesCreated += 1

# Class to implement a priority queue
class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]

    def __len__(self):
        return len(self._queue)

# Stores the result of a given action
class Result():
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

# Main function that executes the search, both uninformed and informed
# regardless of the name. Based off the pseudocode for GraphSearch
def uninformedSearch(initialNode, goalNode, fringe):
    global nodeCount, lastExpansion, depthLimit, numOfNodesCreated
    closedList = {}
    if mode == "a*":
        fringe.push(initialNode, initialNode.pathcost)
    else:
        fringe.append(initialNode)
    while True:
        if len(fringe) == 0:
            # When in iddfs mode, increment depthLimit and restart search
            if mode == "iddfs":
                if depthLimit > 500:
                    exit(1)
                lastExpansion = 0
                fringe.append(initialNode)
                depthLimit += 1
                numOfNodesCreated = 0
                closedList = {}
                continue
            else:
                sys.exit("No solution found!")

        if mode == "bfs":
            currentNode = fringe.popleft()
        else:
            currentNode = fringe.pop()

        if goalTest(currentNode, goalNode):
            return currentNode

        if not inClosedList(currentNode, closedList):
            if mode == "dfs" and currentNode.depth >= 500:
                continue
            nodeCount += 1
            closedList[currentNode.key] = currentNode.depth
            if mode == "a*":
                map(lambda x: fringe.push(x, x.pathcost + getHueristic(x, goalState)), expand(currentNode))
            else:
                map(fringe.append, expand(currentNode))

# Checks to see if a given node is in the closed list or not
def inClosedList(node, closedList):
    if node.key in closedList:
        if node.depth >= closedList[node.key]:
            return True
    else:
        return False

# For each success node, expand
def expand(node):
    successors = []
    for result in successor_fn(node):
        newNode = Node(result.leftSide, result.rightSide, node, result.action, node.depth + 1, node.depth + 1)
        successors.append(newNode)
    return successors

# Checks to see if the given node matches our goal state
def goalTest(node, goalNode):
    if (node.leftSide == goalNode.leftSide) and (node.rightSide == goalNode.rightSide):
        return True
    else:
        return False

# Checks to see all successors
def successor_fn(node):
    global possibleActions
    if mode == "iddfs":
        if node.depth == depthLimit:
            return []
    allowedActions = filter(lambda x: testAction(x, node), possibleActions)
    results = map(lambda y: applyAction(y, node), allowedActions)
    return results

# Given an action it applies that action and updates the new states/nodes
def applyAction(action, node):
    # if node.rightSide[2] == 1:
    #     result = Result(list(node.rightSide), list(node.leftSide), action, "left")
    # else:
    #     result = Result(list(node.leftSide), list(node.rightSide), action, "right")
    # return result

    if node.leftSide[2] == 1:
        result = Result(list(node.leftSide), list(node.rightSide), action, "right")
    else:
        result = Result(list(node.rightSide), list(node.leftSide), action, "left")
    return result

# Check to see if the given action is allowed
def testAction(action, node):
    # Determine which side the boat is on
    if node.rightSide[2] == 1:
        startSide = list(node.rightSide)
        endSide = list(node.leftSide)
    else:
        startSide = list(node.leftSide)
        endSide = list(node.rightSide)
    # Make perform the action and see results
    startSide[0] = startSide[0] - action[0]
    endSide[0] = endSide[0] + action[0]
    startSide[1] = startSide[1] - action[1]
    endSide[1] = endSide[1] + action[1]
    # If results cause more cannibals than missionaires, return false
    if (startSide[0] < 0) or (startSide[1] < 0) or (endSide[0] < 0) or (endSide[1] < 0):
        return False
    elif ((startSide[0] == 0) or (startSide[0] >= startSide[1])) and (endSide[0] == 0 or (endSide[0] >= endSide[1])):
        return True
    else:
        return False
    # # If there's more cannibals on one side than missionaries, stop.
    # if ((startSide[0] == 0) or (startSide[1] <= startSide[0])) and (endSide[0] == 0 or (endSide[1] <= endSide[0])):
    #     return True
    # else:
    #     return False

# Returns the hueristic to get added to the pathcost
def getHueristic(currentNode, goalNode):
    # Determine which side the boat is on
    if goalNode.rightSide[2] == 1:
        retval = (currentNode.leftSide[0] + currentNode.leftSide[1]) - 1
    else:
        retval = (currentNode.rightSide[0] + currentNode.rightSide[1]) - 1
    return retval

# Given the result node, trace back through parents to find path.
def getNodePath(node):
    currentNode = node
    pathToNode = []
    while True:
        try:
            if currentNode.parent == None:
                break
            pathToNode.append(currentNode.action)
        except:
            break
        currentNode = currentNode.parent
    return pathToNode[::-1]

# Read state to node from file
def getFileState(file):
    with open(file) as f:
        content = f.readlines()
    # TODO: Return just content, play around with this in main
    #return Node(map(int, content[0].strip('\n').split(',')), map(int, content[1].strip('\n').split(',')), None, None, 0, 0)
    return content

# Save node path to a file
def outputPathToFile(file, path):
    f = open(file, 'w')
    f.write(str(path))
    f.write('\n')
    f.close()

# Print state given a node
def printState(state):
    print str(state.leftSide)[1:-1].replace(" ", "")
    print str(state.rightSide)[1:-1].replace(" ", "")

# Main function, code starts here
def main():
    # global goalState
    initialStateData = getFileState(fileInitialState)
    initialState = Node(map(int, initialStateData[0].strip('\n').split(',')), map(int, initialStateData[1].strip('\n').split(',')), None, None, 0, 0)
    goalStateData = getFileState(fileGoalState)
    goalState = Node(map(int, goalStateData[0].strip('\n').split(',')), map(int, goalStateData[1].strip('\n').split(',')), None, None, 0, 0)

    # initialStateData = getStateFromFile(initialStateFile)
    # goalState    = getStateFromFile(goalStateFile)

    # Choose data structure based on mode
    if (mode == "bfs") or (mode == "dfs") or (mode == "iddfs"):
        # TODO: Change data structure to different deque if possible
        fringe = collections.deque()
    elif (mode == "a*"):
        # TODO: Change datastructure if possible
        fringe = PriorityQueue()
    else:
        sys.exit('Selected mode not supported')

    resultNode = uninformedSearch(initialState, goalState, fringe)

    outputPathToFile(outputFile, getNodePath(resultNode))
    print getNodePath(resultNode)
    print "Expanded %d nodes" % nodeCount
    print "Length of Solution Path: %d" % len(getNodePath(resultNode))

# Check for correct arguments

# TODO: Change this if possible
if __name__ == "__main__":

    # TODO: Change this method
    if len(sys.argv) < 5:
        sys.exit('Incorrect number of arguments:\n<initial> <goal> <mode> <output>')
    fileInitialState = sys.argv[1]
    fileGoalState    = sys.argv[2]
    mode             = sys.argv[3]
    outputFile       = sys.argv[4]
    main()
