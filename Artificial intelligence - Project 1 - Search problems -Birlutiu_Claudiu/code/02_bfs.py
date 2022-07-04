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