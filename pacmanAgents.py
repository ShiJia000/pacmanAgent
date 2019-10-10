# pacmanAgents.py
# ---------------
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


from pacman import Directions
from game import Agent
from heuristics import *
import random


class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        # returns random action from all the valide actions
        return actions[random.randint(0,len(actions)-1)]

class OneStepLookAheadAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        legal = state.getLegalPacmanActions()
        # get all the successor state for these actions
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal]
        # evaluate the successor states using scoreEvaluation heuristic
        scored = [(admissibleHeuristic(state), action) for state, action in successors]
        # get best choice
        bestScore = min(scored)[0]
        # get all actions that lead to the highest score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        # return random action from the list of the best actions
        return random.choice(bestActions)

class BFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write BFS Algorithm instead of returning Directions.STOP
        queue = []
        nodes = []
        depth = 1;
        
        # get all legal actions
        legalActions = state.getLegalPacmanActions()

        for action in legalActions:
            nextState = state.generatePacmanSuccessor(action)
            queue.append((action, nextState, depth))

        # pop queue and add node to a list called nodes
        while queue:
            # add the pop thing to nodes
            popAction, popState, depth = queue.pop(0)
            nodes.append((popAction,popState, depth))

            # check if it will win the game
            if popState.isWin():
                return popAction

            # if lose
            elif popState.isLose():
                continue

            # if it will not lose the game
            else:
                # add depth
                depth += 1
                # get
                tempLegalActions = popState.getLegalPacmanActions()
                for tempAction in tempLegalActions:
                    tempNextState = popState.generatePacmanSuccessor(tempAction)
                    if tempNextState:
                        queue.append((popAction, tempNextState, depth))    

        # get best score
        scored = [(admissibleHeuristic(nextState), action, depth) for action, nextState, depth in nodes]
        bestScore = min(scored)[0]
        bestActions = [(pair[1], pair[2]) for pair in scored if pair[0] == bestScore]

        # find the minimum cost of the best score
        bestActions.sort(key = lambda x: x[1])
        return bestActions[0][0]


class DFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write DFS Algorithm instead of returning Directions.STOP
        stack = []
        nodes = []
        depth = 1
        
        # find all legal actions
        legalActions = state.getLegalPacmanActions()

        for action in legalActions:
            nextState = state.generatePacmanSuccessor(action)
            stack.append((action, nextState, depth))

        # pop queue and add node to nodes
        while stack:
            # pop the last one 
            popAction, popState, depth = stack.pop()
            nodes.append((popAction, popState, depth))

            # check if it will win the game
            if popState.isWin():
                return popAction

            # if lose
            elif popState.isLose():
                continue

            # if not lose
            else:
                # add depth
                depth += 1

                # get legal actions
                tempLegalActions = popState.getLegalPacmanActions()
                for tempAction in tempLegalActions:
                    tempNextState = popState.generatePacmanSuccessor(tempAction)
                    if tempNextState:
                        stack.append((popAction, tempNextState, depth))


        # get best score
        scored = [(admissibleHeuristic(nextState), action, depth) for action, nextState, depth in nodes]
        bestScore = min(scored)[0]
        bestActions = [(pair[1], pair[2]) for pair in scored if pair[0] == bestScore]

        # find the path that has the minimun cost
        bestActions.sort(key = lambda x: x[1])

        return bestActions[0][0]


class AStarAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write A* Algorithm instead of returning Directions.STOP
        openQueue = []
        closeQueue = []
        depth = 1

        # find the legal actions
        legalActions = state.getLegalPacmanActions()

        #find the minumum cost
        for action in legalActions:
            nextState = state.generatePacmanSuccessor(action)
            totalCost = admissibleHeuristic(nextState) + depth
            openQueue.append((action, nextState, totalCost))

        # append node to open queue
        while openQueue:
            
            # find the best score
            openQueue.sort(key = lambda x: x[2])
            popAction, popState, popCost = openQueue.pop(0)

            # add into close queue
            closeQueue.append((popAction, popState, popCost))

            # isWin
            if popState.isWin():
                return popAction

            # islose
            elif popState.isLose():
                continue

            # not lose
            else:
                # add depth
                depth += 1

                tempLegalActions = popState.getLegalPacmanActions()
                for tempAction in tempLegalActions:
                    tempNextState = popState.generatePacmanSuccessor(tempAction)
                    if tempNextState:
                        tempCost = depth + admissibleHeuristic(tempNextState)
                        openQueue.append((popAction, tempNextState, tempCost))

        # sort close queue
        scored = [(tempCost, action) for action, state, tempCost in closeQueue]
        bestScore = min(scored)[0]
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]

        return bestActions[0]

