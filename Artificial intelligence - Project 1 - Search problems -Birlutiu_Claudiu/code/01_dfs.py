def depthFirstSearch(problem):
    from game import Directions
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