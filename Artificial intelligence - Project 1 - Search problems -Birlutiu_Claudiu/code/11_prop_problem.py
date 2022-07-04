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