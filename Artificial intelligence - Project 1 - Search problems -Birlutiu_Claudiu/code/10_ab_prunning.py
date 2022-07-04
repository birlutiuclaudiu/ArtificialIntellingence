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
        #Daca e randul lui MAX sa ia o dezcizie, atunci se incrementeaza adancimea doarece s-a ajuns
        # ca Max sa ia o noua decizie
        (agentIndex, depth) = ((0, depth + 1) if agentIndex == state.getNumAgents() else (agentIndex, depth))


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