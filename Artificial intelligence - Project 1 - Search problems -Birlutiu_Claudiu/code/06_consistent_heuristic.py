def cornersHeuristic(state, problem):
    """
    A heuristic for the CornersProblem that you defined.

      state:   The current search state
               (a data structure you chose in your search problem)

      problem: The CornersProblem instance for this layout.

    This function should always return a number that is a lower bound on the
    shortest path from the state to a goal of the problem; i.e.  it should be
    admissible (as well as consistent).
    """
    corners = problem.corners  # These are the corner coordinates
    walls = problem.walls  # These are the walls of the maze, as a Grid (game.py)
    "*** YOUR CODE HERE ***"
    # se va construi o lista cu colturile neexplorate
    unvisitedCorners = []
    for corner in state[1].keys():
        if not state[1][corner]:
            unvisitedCorners.append(corner)
    # goal test - se va returna 0 pentru aceasta heuristica
    if not unvisitedCorners:
        return 0

    # se va calcula distanta Manhatten pana la coltul neexplorat cel mai apropiat si se va determina si acel colt
    (closeCorner, dist1) = min([(corner, util.manhattanDistance(state[0], corner)) for corner in unvisitedCorners],
                               key=lambda t: t[1])

    # se calculeaza distanta de la coltul (cel mai apropiat de locatie) la coltul cel mai indepartat de acel colt
    dist2 = max([util.manhattanDistance(closeCorner, corner) for corner in unvisitedCorners])

    # euristica va fi suma dintre cele doua distante
    h = dist1 + dist2
    return h