# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util, game

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        oldFood = currentGameState.getFood()
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        ghostStates = [(state.getPosition(),
                        state.getDirection(),
                        state.scaredTimer) for state in newGhostStates]
        #print("ghostState "+str(ghostStates))
        manD = util.manhattanDistance
        foodList = newFood.asList()
        if len(foodList)==0:
            return 10000

        def findFoodCost():
            foodValue = 0
            current = -1
            start = (0,0)
            def foodFindFoodChain(start,foods):
                # foods does not include the starting point
                if len(foods)==0:
                    return []
                i,distance = min([(idx,manD(food,start)) for idx,food in enumerate(foods)],key = lambda t: t[1])
                s = foods.pop(i)
                return foodFindFoodChain(s,foods)+ [distance]
            if len(foodList)>0:
                i,distance = min([(idx,manD(newPos,food)) for idx,food in enumerate(foodList)],key = lambda t: t[1])
                foodValue += distance
                current = i
                start = foodList.pop(current)

            if current>-1 and len(foodList)>1:
                a = foodFindFoodChain(start,foodList)
                a.remove(max(a))
                foodValue += sum(a)
            return foodValue

        def facingPacman(direction, location):
            # return True iff an direction at location1 is facing toward pacman
            step = game.Actions.getSuccessor(location,direction)
            return manD(step, newPos) < manD(location, newPos)

        def ghostThreateness(ghostPos, ghostDir, scaredTimer):
            if scaredTimer > 6:
                return -1000*manD(ghostPos, newPos)
            if manD(ghostPos, newPos) <= 3:
                ghostPresent =  manD(ghostPos, newPos)
                return 10*ghostPresent + ghostPresent *facingPacman(ghostDir, ghostPos)
            else:
                return 0
        # Useful information you can extract from a GameState (pacman.py)
        #print("newPos"+str(newPos))
        #print("newFood"+str(newFood))
        #print("newScaredTimes"+str(newGhostStates))
        #print("newScaredTimes"+str(newScaredTimes))
        ghostThreat = max([ghostThreateness(l,d,s) for l,d,s in ghostStates])
        "*** YOUR CODE HERE ***"
        nearestDistance = min([manD(newPos,food) for food in foodList])
        #print(action+":")
        #print("getScore"+str(successorGameState.getScore()))
        #print("foodCost"+str(findFoodCost()))
        #print("ghostThreat"+str(ghostThreat))

        total = successorGameState.getScore() - nearestDistance - findFoodCost() - ghostThreat

        #print("total: "+str(total))
        return total

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        self.callTime = 0

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        def bestAction(gameState, myDepth, agentIndex):
            # return (utility, action)
            self.callTime+=1
            if gameState.isWin() or gameState.isLose():
                return (self.evaluationFunction(gameState),"terminal")

            if agentIndex==gameState.getNumAgents()-1:
                agentIndex = 0
                myDepth+=1
            else:
                agentIndex+=1

            if myDepth >= self.depth:
                return (self.evaluationFunction(gameState),"reached depth limit")

            legalActions = gameState.getLegalActions(agentIndex)

            minimax = max if agentIndex == self.index else min
            actionResults = []
            for index,action in enumerate(legalActions):
                bA = bestAction(gameState.generateSuccessor(agentIndex, action), myDepth, agentIndex)
                actionResults.append((bA[0],action))

            return minimax(actionResults,key = lambda x:x[0])

        #print(self.depth)
        utility,action = bestAction(gameState, 0, -1)
        #print(utility,action)
        return action

        util.raiseNotDefined()




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxValue(gameState, myDepth, agentIndex, alpha, beta):
            assert(agentIndex == 0)
            if gameState.isWin() or gameState.isLose():
                return (self.evaluationFunction(gameState),"terminal")
            if myDepth >= self.depth:
                return (self.evaluationFunction(gameState),"reached depth limit")

            legalActions = gameState.getLegalActions(agentIndex)
            actionResults = []
            for action in legalActions:
                bA = minValue(gameState.generateSuccessor(agentIndex, action),
                                myDepth, agentIndex+1, alpha, beta)
                if bA[0] > beta:
                    return bA
                alpha = max(bA[0],alpha)
                actionResults.append((bA[0],action))

            return max(actionResults,key = lambda x:x[0])


        def minValue(gameState, myDepth, agentIndex, alpha, beta):
            if gameState.isWin() or gameState.isLose():
                return (self.evaluationFunction(gameState),"terminal")
            minimax = minValue
            isMax = False
            if myDepth >= self.depth:
                return (self.evaluationFunction(gameState),"reached depth limit")

            legalActions = gameState.getLegalActions(agentIndex)

            if agentIndex==gameState.getNumAgents()-1:
                isMax = True
                minimax = maxValue

            actionResults = []
            for action in legalActions:
                bA = minimax(gameState.generateSuccessor(agentIndex, action),
                                (myDepth+1 if isMax else myDepth),
                                (agentIndex+1 if not isMax else 0), alpha, beta)
                if bA[0] < alpha:
                    return bA
                beta = min(bA[0],beta)
                actionResults.append((bA[0],action))

            return min(actionResults,key = lambda x:x[0])


        def bestAction(gameState, myDepth, agentIndex, alpha, beta):
            # return (utility, action)
            if gameState.isWin() or gameState.isLose():
                return (self.evaluationFunction(gameState),"terminal")

            if agentIndex==gameState.getNumAgents()-1:
                agentIndex = 0
                myDepth+=1
            else:
                agentIndex+=1

            if myDepth >= self.depth:
                return (self.evaluationFunction(gameState),"reached depth limit")

            legalActions = gameState.getLegalActions(agentIndex)

            isMax = True if agentIndex == self.index else False
            minimax = max if isMax else min
            focus = (alpha if isMax else beta)
            actionResults = []
            for index,action in enumerate(legalActions):
                self.callTime+=1
                bA = bestAction(gameState.generateSuccessor(agentIndex, action),
                                myDepth, agentIndex,
                                (focus if isMax else alpha), (beta if isMax else focus))
                if isMax:
                    if bA[0] > beta:
                        return bA
                else:
                    if bA[0] < alpha:
                        return bA
                focus = minimax(bA[0],(alpha if isMax else beta))
                actionResults.append((bA[0],action))

            return minimax(actionResults,key = lambda x:x[0])


        #print(self.depth)
        utility,action = maxValue(gameState, 0,0, float('-inf'), float('inf'))
        #utility,action = bestAction(gameState, 0, -1, float('-inf'), float('inf'))
        #print(utility,action)
        #print(self.callTime)
        return action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def bestAction(gameState, myDepth, agentIndex):
            # return (utility, action)
            self.callTime+=1
            if gameState.isWin() or gameState.isLose():
                return (self.evaluationFunction(gameState),"terminal")

            if agentIndex==gameState.getNumAgents()-1:
                agentIndex = 0
                myDepth+=1
            else:
                agentIndex+=1
            if myDepth >= self.depth:
                return (self.evaluationFunction(gameState),"reached depth limit")

            legalActions = gameState.getLegalActions(agentIndex)
            expectedValue = lambda lst, key: (float(sum([x[0] for x in lst]))/len(lst), legalActions[0])
            expectimax = max if agentIndex == self.index else expectedValue
            actionResults = []
            for index,action in enumerate(legalActions):
                bA = bestAction(gameState.generateSuccessor(agentIndex, action), myDepth, agentIndex)
                actionResults.append((bA[0],action))

            return expectimax(actionResults,key = lambda x:x[0])

        utility,action = bestAction(gameState, 0, -1)
        return action

def getLine(start, end):
    """Bresenham's Line Algorithm"""
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    is_steep = abs(dy) > abs(dx)
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    dx = x2 - x1
    dy = y2 - y1
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    if swapped:
        points.reverse()
    return points


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    ghostStates = [(state.getPosition(),
                    state.getDirection(),
                    state.scaredTimer) for state in newGhostStates]
    #print("ghostState "+str(ghostStates))
    walls = currentGameState.getWalls().asList()

    manD = util.manhattanDistance
    def hasWall(a,b):
        return any((x in walls) for x in getLine(a,b))
    def myD(a,b):
        x,y = a
        a = (int(x),int(y))
        x,y = b
        b = (int(x),int(y))
        return manD(a,b)+hasWall(a,b)*5

    foodList = newFood.asList()

    if currentGameState.isLose():
        return -100000000
    if currentGameState.isWin():
        return 100000000

    def findFoodCost():
        foodValue = 0
        current = -1
        start = (0,0)
        def foodFindFoodChain(start,foods):
            # foods does not include the starting point
            if len(foods)==0:
                return []
            i,distance = min([(idx,manD(food,start)) for idx,food in enumerate(foods)],key = lambda t: t[1])
            s = foods.pop(i)
            return foodFindFoodChain(s,foods)+ [distance]
        if len(foodList)>0:
            i,distance = min([(idx,manD(newPos,food)) for idx,food in enumerate(foodList)],key = lambda t: t[1])
            foodValue += distance
            current = i
            start = foodList.pop(current)

        if current>-1 and len(foodList)>1:
            a = foodFindFoodChain(start,foodList)
            a.remove(max(a))
            foodValue += sum(a)
        return foodValue

    def facingPacman(direction, location):
        # return True iff an direction at location1 is facing toward pacman
        step = game.Actions.getSuccessor(location,direction)
        return myD(step, newPos) < myD(location, newPos)

    def ghostThreateness(ghostPos, ghostDir, scaredTimer):
        scaryness = myD(ghostPos, newPos)
        if scaredTimer > 1 and  scaryness <= 5:
            return -2*scaryness
        if scaryness <= 2:
            return scaryness + scaryness *facingPacman(ghostDir, ghostPos)
        else:
            return 0

    ghostThreat = reduce(lambda x, y: x*y, [ghostThreateness(l,d,s) for l,d,s in ghostStates])
    nearestDistance = min([manD(newPos,food) for food in foodList])
    total = 5*currentGameState.getScore() - nearestDistance - findFoodCost() - ghostThreat
    return total



# Abbreviation
better = betterEvaluationFunction
