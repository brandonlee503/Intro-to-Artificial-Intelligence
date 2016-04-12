import sys
import collections

# Global Variables
depthLimit        = 0
nodeCount         = 0
lastExpansion     = 0
totalNodesCreated = 0

# Actions a state may take in the form of [missionary, cannibal]
possibleActions = [[1,0],[2,0],[0,1],[1,1],[0,2]]
supportedModes = ["bfs", "dfs", "iddfs", "a*"]

# TODO: Update class
class Node():
    """An Abstract entity representing a single state"""
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
    """An Abstract entity representing a priority queue"""
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

def getFileState(file):
    with open(file) as theFile:
        stateData = theFile.readlines()
    return stateData

def uninformedSearch(initialState, goalState, fringe):
    global nodeCount, lastExpansion, depthLimit, totalNodesCreated
    closedList = {}

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
        else:
            # TODO: Change datastructure if possible
            fringe = collections.deque
    else:
        sys.exit("Mode not supported!")

    resultState = uninformedSearch(initialState, goalState, fringe)


main()
