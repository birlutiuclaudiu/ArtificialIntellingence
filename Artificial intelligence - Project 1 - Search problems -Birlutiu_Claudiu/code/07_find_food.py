def foodHeuristic(state, problem):
    position, foodGrid = state
    "*** YOUR CODE HERE ***"
    foodList = foodGrid.asList()
    if not foodList:
        return 0

    # ideea pentru heuristica: asemanatoare cu cea de la corner
    # o sa gasesc calea cea mai scurta pana la mancare iar apoi de la acel punct o sa gasesc distanta maxima pana la urmatoarea bucata de mancare
    (foodPos, distMin) = min([(food, util.manhattanDistance(position, food)) for food in foodList], key=lambda t: t[1])
    (foodMax, distMax) = max([(food, util.manhattanDistance(foodPos, food)) for food in foodList], key=lambda t: t[1])
    h1 = distMin + distMax
    return h1