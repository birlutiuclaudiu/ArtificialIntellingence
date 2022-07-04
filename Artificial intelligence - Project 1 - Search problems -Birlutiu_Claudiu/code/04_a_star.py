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