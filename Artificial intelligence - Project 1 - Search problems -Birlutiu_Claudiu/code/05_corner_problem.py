class CornersProblem(search.SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.
    You must select a suitable state space and child function
    """

    def __init__(self, startingGameState):
        """
        Stores the walls, pacman's starting position and corners.
        """
        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top, right = self.walls.height - 2, self.walls.width - 2
        self.corners = ((1, 1), (1, top), (right, 1), (right, top))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                print('Warning: no food in corner ' + str(corner))
        self._expanded = 0  # DO NOT CHANGE; Number of search nodes expanded
        # Please add any code here which you would like to use
        # in initializing the problem
        """*** YOUR CODE HERE ***"""

        # initializam un dictionar ce contine informatia de corner; tine evidenta colturilor vizitate
        self.visitedCorners = {self.corners[0]: False,
                               self.corners[1]: False,
                               self.corners[2]: False,
                               self.corners[3]: False}

        # verificam pentru fiecare colt daca e pozitia de start sau e zid in locul respectiv si nu va pute ajunge pacman
        for corner in self.corners:
            if self.startingPosition == corner or corner in self.walls:
                self.visitedCorners[corner] = True

        # setam pozitia de start ca o tupla ce contine pozitia de start si dictionarul cu ccolturile
        # initial am creat o clasa CornerState care imi descria structura pentru o stare din aceasta problema
        # apoi am vazut ca se doreste folosirea unei tuple, deoarece cand se prelua pozitia se folosea state[0]
        self.currentState = (self.startingPosition, self.visitedCorners)

    def getStartState(self):
        """
        Returns the start state (in your state space, not the full Pacman state
        space)
        """
        "*** YOUR CODE HERE ***"
        return self.currentState

    def isGoalState(self, state):
        """
        Returns whether this search state is a goal state of the problem.
        """
        "*** YOUR CODE HERE ***"
        # se ia dictionarul cu colturile si se verifica daca toate colturile au fost vizitate
        for values in state[1].values():
            if not values:
                return False
        return True

    def expand(self, state):
        """
        Returns child states, the actions they require, and a cost of 1.

         As noted in search.py:
            For a given state, this should return a list of triples, (child,
            action, stepCost), where 'child' is a child to the current
            state, 'action' is the action required to get there, and 'stepCost'
            is the incremental cost of expanding to that child
        """

        children = []
        for action in self.getActions(state):
            # Add a child state to the child list if the action is legal
            # You should call getActions, getActionCost, and getNextState.
            "*** YOUR CODE HERE ***"
            nextState = self.getNextState(state, action)
            cost = self.getActionCost(state, action, nextState)
            children.append((nextState, action, cost))

        self._expanded += 1  # DO NOT CHANGE
        return children

    def getActions(self, state):
        possible_directions = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]
        valid_actions_from_state = []
        for action in possible_directions:
            x, y = state[0]
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                valid_actions_from_state.append(action)
        return valid_actions_from_state

    def getActionCost(self, state, action, next_state):
        assert next_state == self.getNextState(state, action), (
            "Invalid next state passed to getActionCost().")
        return 1

    def getNextState(self, state, action):
        assert action in self.getActions(state), (
            "Invalid action passed to getActionCost().")
        x, y = state[0]
        dx, dy = Actions.directionToVector(action)
        nextx, nexty = int(x + dx), int(y + dy)
        "*** YOUR CODE HERE ***"
        # se ia un dictionar pentru colturi si se actualizeaza
        visitedCorners = {}
        for corner in state[1]:
            if corner[0] == nextx and corner[1] == nexty:
                visitedCorners[corner] = True
            else:
                visitedCorners[corner] = state[1][corner]
        # se va returna pozitia si dictionarul cu colturile vizitate
        return (nextx, nexty), visitedCorners
    def getCostOfActionSequence(self, actions):
        """
        Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999.  This is implemented for you.
        """
        if actions == None: return 999999
        x, y = self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
        return len(actions)       