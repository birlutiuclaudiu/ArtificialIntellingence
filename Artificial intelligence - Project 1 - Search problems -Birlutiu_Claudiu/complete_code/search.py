# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""
import copy
import math
from random import random

import game
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

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


class DataStructure:
    """
        Crearea unui nod de forma ( name, cost)
    """

    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

    def getName(self):
        return self.name

    def getCost(self):
        return self.cost


class Node:
    """
        Clasa folosita pentru structura de date necesara pentru nodurile arborilor
    """

    def __init__(self, state, parent, action, cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost

    def getState(self):
        return self.state

    def getParent(self):
        return self.parent

    def getAction(self):
        return self.action

    def getCost(self):
        return self.cost

    # sprascirere metoda de equal
    def __eq__(self, obj):
        return isinstance(obj, Node) and obj.getState == self.state


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def randomSearch(problem):
    """
        Random search Agent
        -it just picks onel legal action at each step of search
    """
    posCurrent = problem.getStartState()
    solution = []
    while (not (problem.isGoalState(posCurrent))):
        successors = problem.expand(posCurrent)
        nbSuccessors = len(successors)
        random_succ = int(random() * nbSuccessors)
        next = successors[random_succ]
        posCurrent = next[0]  # se ia doar pozitia succesorului
        solution.append(next[1])  # se va adauga directia la solutie

    print("The solution is:", solution)
    return solution


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    "*** YOUR CODE HERE ***"
    """
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start successors", problem.expand(problem.getStartState()))
    print ("Initial state: ", problem.getStartState())
    for (state, action , cost) in problem.expand(problem.getStartState()):
        print("   Possible next state:", state, " Action:", action, " Cost:", cost)
    util.raiseNotDefined()
    """
    from game import Directions
    from util import Stack
    # se obtin doua variante posibile
    """dir1 = problem.expand(problem.getStartState())[0]
    dir2 = problem.expand(dir1[0])[0]

    #crearea unor tuple (name, cost)
    node1 = DataStructure('west', 3)
    node2 = DataStructure('south', 1)
    stack = util.Stack()
    stack.push(node1)
    stack.push(node2)
    element = stack.pop()
    print("Elementul returnat:", element.getName(), " Cost:", element.getCost())
    return [dir1[1], dir2[1]]
    solution = []
    node = TreeNode(problem.getStartState(), None, None, 0)
    if problem.isGoalState(node.getState()): return node
    return solution
    """
    """ALGORTIMUL PROPRIU ZIS"""

    from util import Stack  # este nevoie de o stiva pentru a implementa iterativ algoritmul
    frontier = Stack()
    # starile parcurse
    reached = []
    node = Node(problem.getStartState(), None, [], 0)
    frontier.push(node)
    # se intra in iteratie; cat timp nu mai exista noduri candidat in frontiera
    while not frontier.isEmpty():
        node = frontier.pop()

        # daca nodul a fost explorat inainte, nu va mai fi expandats
        if node in reached:
            continue
        if problem.isGoalState(node.getState()):
            return construct_path(node)
        # se adauga la noduri explorate
        reached.append(node.getState())
        for (state, action, cost) in problem.expand(node.getState()):  # se cauta in lista de succesori
            childNode = Node(state, node, action, node.getCost() + cost)
            if state not in reached:
                # se adauga nodul copil la frontiera
                frontier.push(childNode)

    return construct_path(node)


def construct_path(node):
    solution = []
    while node:
        if node.getParent():
            solution.append(node.getAction())
        node = node.getParent()
    solution.reverse()
    return solution


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # se bazeaza pe codul din AIMA
    from util import Queue

    # va stoca nodurilor parcurse
    reached = []
    # frontiera de explorat
    frontier = Queue()

    node = Node(problem.getStartState(), None, [], 0)  # radacina
    frontier.push(node)  # se pune in coada nodul parinte

    # se intra in iteratie; cat timp nu mai exista noduri candidat in frontiera
    while not frontier.isEmpty():
        node = frontier.pop()
        # daca noudul a fost vizitat, se va continua iteratia si nu se va expanda din nou
        if node.getState() in reached:
            continue
        if problem.isGoalState(node.getState()):
            return construct_path(node)
        # se adauga nodul in noduri explorate
        reached.append(node.getState())
        for (state, action, cost) in problem.expand(node.getState()):  # se cauta in lista de succesori
            if state not in reached:
                childNode = Node(state, node, action, node.getCost() + cost)
                frontier.push(childNode)

    return construct_path(node)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    """from util import PriorityQueue"""

    from util import PriorityQueue

    # va stoca nodurilor parcurse
    reached = []
    # frontiera de explorat
    frontier = PriorityQueue()

    node = Node(problem.getStartState(), None, [], 0)  # radacina
    frontier.push(node, heuristic(node.getState(), problem))  # se pune in coada nodul parinte

    # se intra in iteratie; cat timp nu mai exista noduri candidat in frontiera
    while not frontier.isEmpty():
        node = frontier.pop()
        # daca noudul a fost vizitat, se va continua iteratia; aceasta e cazul in care e pus de mai multe ori in frontiera
        if node.getState() in reached:
            continue
        if problem.isGoalState(node.getState()):
            return construct_path(node)
        reached.append(node.getState())
        for (state, action, cost) in problem.expand(node.getState()):  # se cauta in lista de succesori
            # daca nodul nu a fost deja extras si expandat din frontiera
            if state not in reached:
                childNode = Node(state, node, action, node.getCost() + cost)
                frontier.update(childNode, heuristic(childNode.getState(), problem) + childNode.getCost())
    return construct_path(node)


# problema propusa este bidirectional best search
def bidirectional_best_first_search(problem, terminated):
    from util import PriorityQueue

    startNode = problem.getStartState()
    nodeF = Node(startNode, None, [], 0)
    # deoarece ne punem problema inversa, nodul de start pentru back este goal-ul problemei
    nodeB = Node(problem.goal, None, [], 0)
    # definim problema inversa pentru situatia in care mergem invers
    problem2 = copy.copy(problem)
    problem2.goal = problem.getStartState()

    frontierF = PriorityQueue()
    frontierB = PriorityQueue()
    # deoarece este implementata pentru ucs, vom alege ca si prioritate costul
    frontierF.push(nodeF, function(nodeF, problem))
    frontierB.push(nodeB, function(nodeB, problem2))

    # crearea unor dictionare state : node
    reachedF = {nodeF.getState(): nodeF}
    reachedB = {nodeB.getState(): nodeB}

    solution = Node('failure', None, [], math.inf)
    while (not frontierF.isEmpty()) and (not frontierB.isEmpty()) and not terminated(solution, frontierF,
                                                                                     frontierB, problem, problem2):
        # o metoda prin care sa extrag fara a sterge top-ul din cozile de prioritati
        top_f = frontierF.pop()
        frontierF.push(top_f, function(nodeF, problem))
        top_g = frontierB.pop()
        frontierB.push(top_g, function(nodeB, problem2))
        # se va decide pe care dintre probleme se va continua: forward sau backward in functie de evaluarea in cele doua noduri
        # respective
        if function(top_f, problem) < function(top_g, problem2):
            solution = proceed('F', problem, frontierF, reachedF, reachedB, solution)
        else:
            solution = proceed('B', problem, frontierB, reachedB, reachedF, solution)
    return solution


def join_nodes(nf, nb):
    """Se va face joinul intre cele doua cai gasite; se va atasa caii nf, calea nb dar inversata"""
    entirePath = nf
    while nb.parent is not None:
        cost = entirePath.getCost() + nb.getCost() - nb.parent.getCost()
        if nb.getAction() == game.Directions.WEST:
            action = game.Directions.EAST
        elif nb.getAction() == game.Directions.EAST:
            action = game.Directions.WEST
        elif nb.getAction() == game.Directions.SOUTH:
            action = game.Directions.NORTH
        elif nb.getAction() == game.Directions.NORTH:
            action = game.Directions.SOUTH
        else:
            action = nb.getAction()
        entirePath = Node(nb.parent.getState(), entirePath, action, cost)
        nb = nb.parent
    return entirePath


def proceed(dir, problem, frontier, reached, reached2, solution):
    """Aceasta metoda va determina succesorii nodului din frontiera"""
    node = frontier.pop()
    for (state, action, cost) in problem.expand(node.getState()):
        childNode = Node(state, node, action, node.getCost() + cost)
        if state not in reached or childNode.getCost() < reached[state].getCost():
            frontier.push(childNode, function(childNode, problem))
            reached[state] = childNode
            # se verifica daca frontierele colizioneaza ceea ce va duce la o noua solutie si se va actualiza solutia
            # finala daca este mai buna cea nou obtinuta
            if state in reached2:
                if dir == 'F':
                    solution2 = join_nodes(childNode, reached2[state])
                else:
                    solution2 = join_nodes(reached2[state], childNode)
                if solution2.getCost() < solution.getCost():
                    solution = solution2
    return solution

#se va decide cand se va termina iteratia din while
def terminated(solution, frontier_f, frontier_b, problem, problem2):
    nodeF, nodeB = frontier_f.pop(), frontier_b.pop()
    frontier_f.push(nodeF, function(nodeF, problem))
    frontier_b.push(nodeB, function(nodeB, problem2))
    return nodeF.getCost() + nodeB.getCost() > solution.getCost()


# evaluarea costului unui nod in functie de problema si euirstica
def function(node, problem, heuristic=util.manhattanDistance):
    return node.getCost() + heuristic(node.getState(), problem.goal)


def a_star_bidirectional(problem_f):
    solution = construct_path(bidirectional_best_first_search(problem_f, terminated))
    print(solution)
    return solution


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
rs = randomSearch
bis = a_star_bidirectional
