# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""
from sets import Set
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    frontior = util.Stack()
    #print("start point", problem.getStartState())
    startPosition = problem.getStartState()
    frontior.push([(startPosition,None,0)])
    # [(startPosition,None,0)] is the initial nodePath, each node has position, action and cost
    # nodePath will get longer when more nodes are explored
    while not frontior.isEmpty():
        #print("frontior: "+str([[node[1] for node in path] for path in frontior.list]))
        current = frontior.pop()
        if problem.isGoalState(current[-1][0]):
            return [node[1] for node in current][1:]
        for idx,child in enumerate(problem.getSuccessors(current[-1][0])):
            #print("got child "+str(child))
            if child[0] not in [node[0] for node in current]:
                frontior.push(current+[child])
                #explored.add(child[0])
                #print('child added to fronitor')
            #else:
                #print('child '+str(child)+' explored, discarding')
    #util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    explored = []
    frontior = util.Queue()
    #print("start point", problem.getStartState())
    startPosition = problem.getStartState()
    frontior.push([(startPosition,None,0)])
    explored.append(startPosition)
    # [(startPosition,None,0)] is the initial nodePath, each node has position, action and cost
    # nodePath will get longer when more nodes are explored
    while not frontior.isEmpty():
        #print([[node[0] for node in path] for path in frontior.list])
        #print([path[-1] for path in frontior.list])
        #print("frontior size "+str(len(frontior.list)))
        currentPath = frontior.pop()
        currentNode = currentPath[-1][0]

        #print("Popping"+str(currentNode))
        #print([x[1] for x in currentPath][1:])
        #print('current',current)
        if problem.isGoalState(currentNode):
            #print([x[1] for x in currentPath][1:])
            return [x[1] for x in currentPath][1:]
        for child in problem.getSuccessors(currentNode):
            #print("got child "+str(child))
            if child[0] not in explored:
                #print("added")
                frontior.push(currentPath+[child])
                explored.append(child[0])
        #print(explored)
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # priority function return the total cost of a given nodePath
    explored = Set()
    pFunction = lambda nodePath: sum([node[-1] for node in nodePath])
    frontior = util.PriorityQueueWithFunction(pFunction)
    #print("start point", problem.getStartState())
    startPosition = problem.getStartState()
    frontior.push([(startPosition,None,0)])
    explored.add(startPosition)
    # [(startPosition,None,0)] is the initial nodePath
    # each node has position, action and cost
    # nodePath will get longer when more nodes are explored
    def findSameNodeOnHeap(node, cost):
        for entry in frontior.heap:
            if node[0] == entry[-1][-1][0] and cost < entry[0]:
                return True
    while not frontior.isEmpty():
        #print(str(frontior))
        currentPath = frontior.pop()
        #print("Popping "+str(currentPath[-1][0]))
        currentNode = currentPath[-1][0]
        #print('got'+str(currentNode))
        if problem.isGoalState(currentNode):
            result = [x[1] for x in currentPath]
            result.remove(None)
            return result
        #print('current',current)
        explored.add(currentNode)
        for child in problem.getSuccessors(currentNode):
            stateSet = [path[-1][0] for path in [entry[-1] for entry in frontior.heap]]
            # stateSet is the set of state that are currently in the fronitor
            if child[0] not in explored:
                if child[0] not in stateSet or findSameNodeOnHeap(child[0],pFunction(currentPath+[child])):
                    frontior.push(currentPath+[child])

                #print('discarding it')
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    explored = Set()
    # priority function return the total cost + heuristic of a given nodePath
    pFunction = lambda nodePath: sum([node[-1] for node in nodePath])+heuristic(nodePath[-1][0],problem)
    frontior = util.PriorityQueueWithFunction(pFunction)
    startPosition = problem.getStartState()
    frontior.push([(startPosition,None,0)])
    explored.add(startPosition)
    replacement = []
    def findSameNodeOnHeap(node, cost):
        for entry in frontior.heap:
            if node[0] == entry[-1][-1][0] and cost < entry[0]:
                replacement.append(entry)
                return True
    while not frontior.isEmpty():
        #print(str(frontior))
        currentPath = frontior.pop()
        #print("Popping "+str(currentPath[-1][0]))
        currentNode = currentPath[-1][0]
        if problem.isGoalState(currentNode):
            result = [x[1] for x in currentPath]
            result.remove(None)
            return result
        explored.add(currentNode)

        for child in problem.getSuccessors(currentNode):
            #print("got child"+str(child))
            stateSet = [path[-1][0] for path in [entry[-1] for entry in frontior.heap]]
            # stateSet is the set of state that are currently in the fronitor
            if child[0] not in explored:
                if child[0] not in stateSet:
                    frontior.push(currentPath+[child])
                elif findSameNodeOnHeap(child[0],pFunction(currentPath+[child])):
                    frontior.push(currentPath+[child])
                    #print("replacing "+str(bad)+" with "+str(currentPath+[child]))
                    frontior.heap.remove(replacement.pop())
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
