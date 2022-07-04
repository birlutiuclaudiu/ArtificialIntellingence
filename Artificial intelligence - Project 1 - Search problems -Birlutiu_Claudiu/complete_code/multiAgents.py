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
import math

from util import manhattanDistance
from game import Directions
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
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        """print(
            f"New Pos: {newPos}, NewFood:{newFood}, NewGhost:{childGameState.getGhostPositions()}, NewScared: {newScaredTimes}")
        distanceToGhosts = [manhattanDistance(newPos, gp) for gp in childGameState.getGhostPositions()]
        print(
            f"New Pos: {newPos}, Ghost_pos:{childGameState.getGhostPositions()}, Distance_to_ghost:{distanceToGhosts}")"""

        foodList = newFood.asList()
        score = sum([1 / util.manhattanDistance(newPos, food) if foodList else 0 for food in newFood.asList()])

        score += sum([util.manhattanDistance(newPos, ghost) / 100 if util.manhattanDistance(newPos,
                                                                                            ghost) / 1000 >= 2 else -9999999
                      for ghost in childGameState.getGhostPositions()])
        score += sum([time / 100 if newScaredTimes else 0 for time in newScaredTimes])

        return childGameState.getScore() + score


class RandomAgent(Agent):

    def getAction(self, gameState):
        legalMoves = gameState.getLegalActions()
        # Pick randomly among the legal
        chosenIndex = random.choice(range(0, len(legalMoves)))
        return legalMoves[chosenIndex]


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


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

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        (action, value) = self.h_minimax(gameState, 0, 0)
        return action

    # functie auxiliara care verifica daca se va incheia apelul lui h_minmax;
    # acesta se va termina in momentul in care se ajunge la o stare in care pacman castiga sau pacman pierde sau se ajunge
    # la adancimea setata pana la care se face evaluarea
    def _cut_off_test(self, state, depth):
        if state.isWin() or state.isLose() or depth == self.depth:
            return True
        else:
            return False

    def h_minimax(self, state, agentIndex, depth):
        # adancimea pana la care se ajunge sa se evalueze depinde de cate
        # ori pacman (MAX) are de facut o decizie; deoarece sunt mai multe fantome
        # care vor fi evaluate secvential
        #Daca e randul lui MAX sa ia o dezcizie, atunci se incrementeaza adancimea doarece s-a ajuns
        # ca Max sa ia o noua decizie
        (agentIndex, depth) = ((0, depth + 1) if agentIndex == state.getNumAgents() else (agentIndex, depth))

        # se va evalua testul de cut_off
        if self._cut_off_test(state, depth):
            return [], self.evaluationFunction(state)
        # se va decide al carui agent este randul
        # daca indexul este egal cu 0 atunci randul e a lui MAX si se va determina valoarea maxima
        if agentIndex == 0:
            return self.max_value(state, agentIndex, depth)
        else:
            # in caz contrar, e o fantoma si se calculeaza valoarea minima
            return self.min_value(state, agentIndex, depth)

    def max_value(self, state, agentIndex, depth):
        legalActions = state.getLegalActions(agentIndex)
        # daca nu sunt valori legale inseamna ca e punct terminal si se va termina si se va intoarce evaluarea
        # in acel punct
        if not legalActions:
            return [], self.evaluationFunction(state)

        (action, value) = max(
            [(action, self.h_minimax(state.getNextState(agentIndex, action), agentIndex + 1, depth)[1])
             for action in legalActions], key=lambda t: t[1])
        return action, value

    def min_value(self, state, agentIndex, depth):
        legalActions = state.getLegalActions(agentIndex)
        # daca nu sunt valori legale inseamna ca e punct terminal si se va intoarce evaloarea in acel punct
        if not legalActions:
            return [], self.evaluationFunction(state)
        # se va intoarece valoarea minima
        (action, value) = min(
            [(action, self.h_minimax(state.getNextState(agentIndex, action), agentIndex + 1, depth)[1])
             for action in legalActions], key=lambda t: t[1])
        return action, value


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        (action, value) = self.h_alpha_beta_prunning(gameState, 0, 0, -math.inf, math.inf)
        return action

    # functie auxiliara care verifica daca se va incheia apelul lui h_minmax;
    # acesta se va termina in momentul in care se ajunge la o stare in care pacman castiga sau pacman pierde sau se ajunge
    # la adancimea setata pana la care se face evaluarea
    def _cut_off_test(self, state, depth):
        if state.isWin() or state.isLose() or depth == self.depth:
            return True
        else:
            return False

    def h_alpha_beta_prunning(self, state, agentIndex, depth, alpha, beta):
        # adancimea pana la care se ajunge sa se evalueze depinde de cate
        # ori pacman (MAX) are de facut o decizie; deoarece sunt mai multe fantome
        # care vor fi evaluate secvential
        (agentIndex, depth) = ((0, depth+1) if agentIndex == state.getNumAgents() else (agentIndex, depth))
        # se va evalua testul de cut_off
        if self._cut_off_test(state, depth):
            return [], self.evaluationFunction(state)
        # se va decide al carui agent este randul
        # daca indexul este egal cu 0 atunci randul e a lui MAX si se va determina valoarea maxima
        if agentIndex == 0:
            return self.max_value(state, agentIndex, depth, alpha, beta)
        else:
            # in caz contrar, e o fantoma si se calculeaza valoarea minima
            return self.min_value(state, agentIndex, depth, alpha, beta)

    def max_value(self, state, agentIndex, depth, alpha, beta):
        legalActions = state.getLegalActions(agentIndex)
        # daca nu sunt valori legale inseamna ca e punct terminal si se va termina si se va intoarce evaluarea
        # in acel punct
        if not legalActions:
            return [], self.evaluationFunction(state)
        # initializam o valoare foarte mica
        v = -math.inf
        move = []
        for action in legalActions:
            (action2, value2) = self.h_alpha_beta_prunning(state.getNextState(agentIndex, action), agentIndex + 1,
                                                       depth, alpha, beta)
            if value2 > v:
                v, move = value2, action
                alpha = max(alpha, v)
            if v > beta:
                return move, v
        return move, v

    def min_value(self, state, agentIndex, depth, alpha, beta):
        legalActions = state.getLegalActions(agentIndex)
        # daca nu sunt valori legale inseamna ca e punct terminal si se va intoarce evaloarea in acel punct
        if not legalActions:
            return [], self.evaluationFunction(state)

        # se va initializa valoarea minima la infinit
        v = math.inf
        move = []
        for action in legalActions:
            action2, value2 = self.h_alpha_beta_prunning(state.getNextState(agentIndex, action), agentIndex + 1,
                                                         depth, alpha, beta)
            if value2 < v:
                v, move = value2, action
                beta = min(beta, v)
            if v < alpha:
                return move, v
        return move, v

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
        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
