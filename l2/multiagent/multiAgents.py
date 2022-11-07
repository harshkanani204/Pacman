# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        
        if successorGameState.isWin():
            return 999999

        positionOfGhost = []
        for x in newGhostStates:
            positionOfGhost.append(x.getPosition())

        currentPositionOfGhost = []
        for x in newGhostStates:
            currentPositionOfGhost.append(x.getPosition())

        distanceFromGhost = []
        for x in positionOfGhost:
            distanceFromGhost.append(manhattanDistance(newPos,x))
            
        currentDistanceFromGhost = []
        for x in positionOfGhost:
            currentDistanceFromGhost.append(manhattanDistance(newPos,x))

        foodDistance = [0]
        for x in newFood.asList():
            foodDistance.append(manhattanDistance(newPos,x))
            

        score = 0

        numberOfFoodLeft = len(newFood.asList())
        currentNumberOfFoodLeft = len(currentGameState.getFood().asList())
        numberofPowerPills = len(successorGameState.getCapsules())
        sumScaredTimes = sum(newScaredTimes)
            
        score = score + (successorGameState.getScore() - currentGameState.getScore())

        if action == Directions.STOP:
            score = score - 10

        if newPos in currentGameState.getCapsules():
            score = score + (150 * numberofPowerPills)
            
        if numberOfFoodLeft < currentNumberOfFoodLeft:
            score = score + 200

        score = score - (10 * numberOfFoodLeft)

        if sumScaredTimes <= 0 :
            if min(currentDistanceFromGhost) >= min(distanceFromGhost):
                score = score + 200
            else:
                score = score - 100

            
        else:
            if min(currentDistanceFromGhost) >= min(distanceFromGhost):
                score = score - 100
            else:
                score = score + 200
	    
        return score

def scoreEvaluationFunction(currentGameState: GameState):
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

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def maxLevel(gameState,depth):
            
            if gameState.isWin() or gameState.isLose() :   
                return self.evaluationFunction(gameState)
            curr= depth + 1
            if curr==self.depth:
                return self.evaluationFunction(gameState)
            maxvalue = -999999
            moves = gameState.getLegalActions(0)
            for move in moves:
                succ= gameState.generateSuccessor(0,move)
                maxvalue = max (maxvalue,minLevel(succ,curr,1))
            return maxvalue
        
        def minLevel(gameState,depth, agentIndex):
            minvalue = 999999
            if gameState.isWin() or gameState.isLose():   
                return self.evaluationFunction(gameState)
            moves = gameState.getLegalActions(agentIndex)
            for move in moves:
                successor= gameState.generateSuccessor(agentIndex,move)
                if agentIndex == (gameState.getNumAgents() - 1):
                    minvalue = min (minvalue,maxLevel(successor,depth))
                else:
                    minvalue = min(minvalue,minLevel(successor,depth,agentIndex+1))
            return minvalue

        moves = gameState.getLegalActions(0)
        currentScore = -999999
        returnAction = ''
        for move in moves:
            nextState = gameState.generateSuccessor(0,move)
            score = minLevel(nextState,0,1)
            if score > currentScore:
                Action = move
                currentScore = score
        return Action

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        import math
        def maxLevel(gameState,depth,alpha, beta):
            if gameState.isWin() or gameState.isLose() :   
                return self.evaluationFunction(gameState)
            maxvalue = -math.inf
            moves = gameState.getLegalActions(0)
            curr= depth + 1
            if curr==self.depth:
                return self.evaluationFunction(gameState)
            for move in moves:
                succ= gameState.generateSuccessor(0,move)
                maxvalue = max (maxvalue,minLevel(succ,curr,1,alpha,beta))
                if maxvalue > beta:
                    return maxvalue
                alpha = max(alpha,maxvalue)
            return maxvalue

        def minLevel(gameState,depth,agentIndex,alpha,beta):
            minvalue = math.inf
            if gameState.isWin() or gameState.isLose():   
                return self.evaluationFunction(gameState)
            moves = gameState.getLegalActions(agentIndex)
            for move in moves:
                succ= gameState.generateSuccessor(agentIndex,move)
                if agentIndex == (gameState.getNumAgents()-1):
                    minvalue = min (minvalue,maxLevel(succ,depth,alpha,beta))
                    if minvalue < alpha:
                        return minvalue
                    beta = min(beta,minvalue)
                else:
                    minvalue = min(minvalue,minLevel(succ,depth,agentIndex+1,alpha,beta))
                    if minvalue < alpha:
                        return minvalue
                    beta = min(beta,minvalue)
            return minvalue
        moves = gameState.getLegalActions(0)
        currentScore = -math.inf
        alpha = -math.inf
        beta = math.inf
        for move in moves:
            nextState = gameState.generateSuccessor(0,move)
           
            score = minLevel(nextState,0,1,alpha,beta)
            
            if score > currentScore:
                returnAction = move
                currentScore = score   
            if score > beta:
                return returnAction
            alpha = max(alpha,score)
        return returnAction
        
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def maxLevel(gameState,depth):
            
            if gameState.isWin() or gameState.isLose() :   
                return self.evaluationFunction(gameState)
            curr= depth + 1
            if curr==self.depth:
                return self.evaluationFunction(gameState)
            maxvalue = -999999
            moves = gameState.getLegalActions(0)
            for move in moves:
                succ= gameState.generateSuccessor(0,move)
                maxvalue = max (maxvalue,minLevel(succ,curr,1))
            return maxvalue
        
        def minLevel(gameState,depth, agentIndex):
            minvalue = 0
            if gameState.isWin() or gameState.isLose():   
                return self.evaluationFunction(gameState)
            moves = gameState.getLegalActions(agentIndex)
            for move in moves:
                successor= gameState.generateSuccessor(agentIndex,move)
                if agentIndex == (gameState.getNumAgents() - 1):
                    minvalue = minvalue +  maxLevel(successor,depth)
                else:
                    minvalue = minvalue + minLevel(successor,depth,agentIndex+1)
            return minvalue/len(moves)

        moves = gameState.getLegalActions(0)
        currentScore = -999999
        returnAction = ''
        for move in moves:
            nextState = gameState.generateSuccessor(0,move)
            score = minLevel(nextState,0,1)
            if score > currentScore:
                Action = move
                currentScore = score
        return Action
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
    if currentGameState.isWin():
        return 999999

    positionOfGhost = []
    for x in newGhostStates:
        positionOfGhost.append(x.getPosition())

    distanceFromGhost = []
    for x in positionOfGhost:
        distanceFromGhost.append(manhattanDistance(newPos,x))

    foodDistance = [0]
    for x in newFood.asList():
        foodDistance.append(manhattanDistance(newPos,x))
            

    score = 0

    numberOfFoodLeft = len(newFood.asList())
    currentNumberOfFoodLeft = len(currentGameState.getFood().asList())
    numberofPowerPills = len(currentGameState.getCapsules())
    sumScaredTimes = sum(newScaredTimes)
            
    score = score + (currentGameState.getScore() - currentGameState.getScore())

    if newPos in currentGameState.getCapsules():
        score = score + (150 * numberofPowerPills)
            
    if numberOfFoodLeft < currentNumberOfFoodLeft:
        score = score + 200

    score = score - (10 * numberOfFoodLeft)

    for i in distanceFromGhost:
        if sumScaredTimes == 0:
            score = score + i
    
        else:
            score = score + 1/i
 
    return score
    
    
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
