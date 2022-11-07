# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import queue
from shutil import move
from numpy import append
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfmoves(self, moves):
        """
         moves: A list of moves to take

        This method returns the total cost of a particular sequence of moves.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import next_moves
    s = next_moves.SOUTH
    w = next_moves.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of moves that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    from util import Stack
    start = problem.getStartState()
    curr = problem.getStartState()
    visited = []
    visited.append(start)
    stk = Stack()
    state_dir = (start, [])
    stk.push(state_dir)
    while (stk.isEmpty() == False) :
        if (problem.isGoalState(curr) == True):
            break
        state = stk.pop()
        current = state[0]
        moves  = state[1]
        visited.append(current)
        successor = problem.getSuccessors(current)
        for succ in successor:
            next = succ[0]
            if next in visited:
                continue
            else:
                curr = succ[0]
                list = []
                next_move = succ[1]
                list.append(next_move)
                upd_moves = moves + list
                stk.push((next, upd_moves))
    return upd_moves

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue
    start = problem.getStartState()
    curr = problem.getStartState()
    visited = []
    visited.append(start)
    queue = Queue()
    state_dir = (start, [])
    queue.push(state_dir)
    while (queue.isEmpty() == False) :
        state = queue.pop()
        current = state[0]
        moves  = state[1]
        if (problem.isGoalState(current) == True):
            return moves
        successor = problem.getSuccessors(current)
        for succ in successor:
            next = succ[0]
            if next in visited:
                continue
            else:
                curr = succ[0]
                next_move = succ[1]
                visited.append(next)
                list = []
                list.append(next_move)
                upd_moves = moves + list
                queue.push((next, upd_moves))
    return moves 
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    start = problem.getStartState()
    visited = []
    PQueue = PriorityQueue()
    PQueue.push((start, []) ,0)
    while (PQueue.isEmpty() == False):
        state = PQueue.pop()
        current = state[0]
        moves = state[1]
        if problem.isGoalState(current):
            return moves
        if current in visited:
            continue
        else:
            successors = problem.getSuccessors(current)
            for succ in successors:
                next = succ[0]
                if next not in visited:
                    next_move = succ[1]
                    upd_moves = moves + [next_move]
                    PQueue.push((next, upd_moves), problem.getCostOfActions(upd_moves))
        visited.append(current)
    return moves
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    start = problem.getStartState()
    visited = []
    PQueue = PriorityQueue()
    PQueue.push((start, []), nullHeuristic(start, problem))
    nCost = 0
    while (PQueue.isEmpty() == False):
        state = PQueue.pop()
        current = state[0]
        moves = state[1]
        if problem.isGoalState(current):
            return moves
        if current in visited:
            continue
        else:
            successors = problem.getSuccessors(current)
            for succ in successors:
                next = succ[0]
                if next not in visited:
                    next_move = succ[1]
                    nmoves = moves + [next_move]
                    nCost = problem.getCostOfActions(nmoves) + heuristic(next, problem)
                    PQueue.push((next, moves + [next_move]), nCost)
        visited.append(current)
    return moves
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch


