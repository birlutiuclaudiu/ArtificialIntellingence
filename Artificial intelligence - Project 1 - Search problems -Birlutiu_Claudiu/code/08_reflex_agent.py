    def evaluationFunction(self, currentGameState, action):
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        foodList = newFood.asList()
        score = sum([1 / util.manhattanDistance(newPos, food) if foodList else 0 for food in newFood.asList()])

        score += sum([util.manhattanDistance(newPos, ghost) / 100 if util.manhattanDistance(newPos,
                                                                                            ghost) / 1000 >= 2 else -9999999
                      for ghost in childGameState.getGhostPositions()])
        score += sum([time / 100 if newScaredTimes else 0 for time in newScaredTimes])

        return childGameState.getScore() + score
