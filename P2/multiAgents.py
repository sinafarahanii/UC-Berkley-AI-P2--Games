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
import random, util

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

    def evaluationFunction(self, currentGameState, action):
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        foodlist = newFood.asList()
        food_dist = []
        ghost_dist = []
        for food in foodlist:
            food_dist.append(manhattanDistance(newPos, food))
        if len(foodlist) != 0:
            closest_food = min(food_dist)
            furthest_food = max(food_dist)
        else:
            return successorGameState.getScore()
        for ghost in newGhostStates:
            ghost_dist.append(manhattanDistance(newPos, ghost.getPosition()))
        if len(ghost_dist) != 0:
            closest_ghost = min(ghost_dist)
        if newScaredTimes[0] == 0:
            if len(foodlist) == 1:
                score = closest_ghost - closest_food
            else:
                score = closest_ghost - (furthest_food + closest_food)
        else:
            score = closest_ghost
        return successorGameState.getScore() + score

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

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        "*** YOUR CODE HERE ***"
        def max_value(game_state, depth):
            if game_state.isWin() or game_state.isLose() or depth == 0:
                return self.evaluationFunction(game_state)
            max_node = float('-inf')
            for action in game_state.getLegalActions(0):
                max_node = max(max_node, min_value(game_state.generateSuccessor(0, action), depth, 1))

            return max_node
        def min_value(game_state, depth, number_of_agents):
            if game_state.isWin() or game_state.isLose():
                return self.evaluationFunction(game_state)
            min_node = float('inf')
            for action in game_state.getLegalActions(number_of_agents):
                if number_of_agents == game_state.getNumAgents() -1:
                    min_node = min(min_node, max_value(game_state.generateSuccessor(number_of_agents, action), depth-1))
                else:
                    min_node = min(min_node, min_value(game_state.generateSuccessor(number_of_agents, action), depth, number_of_agents+1))
            return min_node

        def minimax(game_state):
            current_max = float('-Inf')
            for action in gameState.getLegalActions(0):
                min_node = min_value(gameState.generateSuccessor(0, action), self.depth, 1)
                if min_node > current_max:
                    current_max = min_node
                    move = action
            return move
        return minimax(gameState)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        def max_value(game_state, depth, alpha, beta):
            if game_state.isWin() or game_state.isLose() or depth == self.depth:
                return self.evaluationFunction(game_state), ""
            v = (float('-inf'), "")
            for action in game_state.getLegalActions(0):
                max_node = min_value(game_state.generateSuccessor(0, action), depth, 1, alpha, beta)
                if v[0]<max_node[0]:
                    v = (max_node[0], action)
                if v[0] > beta:
                    return v
                alpha = max(alpha, v[0])
            return v

        def min_value(game_state, depth, number_of_agents, alpha, beta):
            if game_state.isWin() or game_state.isLose():
                return self.evaluationFunction(game_state), ""
            v = (float('inf'), "")
            for action in game_state.getLegalActions(number_of_agents):
                if number_of_agents == game_state.getNumAgents() -1:
                    min_node = max_value(game_state.generateSuccessor(number_of_agents, action), depth+1, alpha, beta)
                else:
                    min_node = min_value(game_state.generateSuccessor(number_of_agents, action), depth,number_of_agents + 1, alpha, beta)
                if v[0] > min_node[0]:
                    v = (min_node[0], action)
                if v[0] < alpha:
                    return v
                beta = min(beta, v[0])
            return v
        result = max_value(gameState, 0, float('-inf'), float('inf'))
        return result[1]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        def max_value(game_state, depth):
            if game_state.isWin() or game_state.isLose() or depth == 0:
                return self.evaluationFunction(game_state)
            max_node = float('-inf')
            for action in game_state.getLegalActions(0):
                max_node = max(max_node, expected_value(game_state.generateSuccessor(0, action), depth, 1))

            return max_node
        def expected_value(game_state, depth, number_of_agents):
            if game_state.isWin() or game_state.isLose():
                return self.evaluationFunction(game_state)
            exp_value = 0
            for action in game_state.getLegalActions(number_of_agents):
                if number_of_agents == game_state.getNumAgents() - 1:
                    exp_value += max_value(game_state.generateSuccessor(number_of_agents, action), depth-1)/len(game_state.getLegalActions(number_of_agents))
                else:
                    exp_value += expected_value(game_state.generateSuccessor(number_of_agents, action), depth, number_of_agents+1)/len(gameState.getLegalActions(number_of_agents))
            return exp_value

        def expectimax(game_state):
            current_max = float('-Inf')
            for action in gameState.getLegalActions(0):
                exp_node = expected_value(gameState.generateSuccessor(0, action), self.depth, 1)
                if exp_node > current_max:
                    current_max = exp_node
                    move = action
            return move
        return expectimax(gameState)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    Don't forget to use pacmanPosition, foods, scaredTimers, ghostPositions!
    DESCRIPTION: <write something here so we know what you did>
    """

    pacmanPosition = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimers = [ghostState.scaredTimer for ghostState in ghostStates]
    ghostPositions = currentGameState.getGhostPositions()
    
    "*** YOUR CODE HERE ***"
    food_list = foods.asList()
    food_dist = float('inf')
    for food in food_list:
        f = manhattanDistance(pacmanPosition, food)
        if f < food_dist:
            food_dist = f
    nearest_ghost = manhattanDistance(pacmanPosition, min(ghostPositions))
    if scaredTimers == 0:
        return currentGameState.getScore() + (nearest_ghost / food_dist)
    else:
        return currentGameState.getScore() + (nearest_ghost / food_dist) + sum(scaredTimers)
# Abbreviation
better = betterEvaluationFunction
