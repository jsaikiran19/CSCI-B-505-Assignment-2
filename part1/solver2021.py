#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by: name IU ID
#
# Based on skeleton code by D. Crandall & B551 Staff, September 2021
#
from queue import PriorityQueue
import copy
import math
import sys

ROWS=5
COLS=5

def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]

def move_outer_clockwise(board):
    n = len(board)
    size = int(math.sqrt(len(board)))
    temp = 0
    for i in range(len(board)):
        if i==0:
            temp = board[i]    
            board[i] = board[i+size]
        elif i<size:
            a = board[i]
            board[i] = temp
            temp = a
        elif i>(size-1)*size - 1:
            if i+1<n:
                board[i] = board[i+1]
        elif i%size==0:
            if i+size<n:
                board[i] = board[i+size]
        elif i%size==size-1:
            a = board[i]
            board[i] = temp
            temp = a
    board[-1] = temp
    return board


def move_outer_cclockwise(board):
    temp = board[0]
    n = len(board)
    size = int(math.sqrt(len(board)))
    for i in range(len(board)):
        if i<size-1:
            board[i] = board[i+1]
        elif i%size==size-1:
            if i+size<n:
                board[i] = board[i+size]
        elif i%size==0:
            a = board[i]
            board[i] = temp
            temp = a
        elif i>(size-1)*size - 1:
            a = board[i]
            board[i] = temp
            temp = a
    board[-1] = temp
    return board

def get_inner_ring(board):
    ring = []
    for i in range(len(board)):
        if i%5!=0 and i%5!=4 and i>5 and i<19:
            ring.append(board[i])
    return (ring)

def rotate_inner_ring(board,direction = 'c'):
    inner_ring = get_inner_ring(board)
    inner_rotated = move_outer_clockwise(inner_ring) if direction =='c' else move_outer_cclockwise(inner_ring)
    for i in range(len(board)):
        if i%5!=0 and i%5!=4 and i>5 and i<19:
            board[i] = inner_rotated.pop(0)
    return board

def get_goal_position(n):
    if n%5==0:
        return (n//5-1,4)
    return (n//5,n%5-1)

def move_down(board,c):
    temp = board[c]
    board[c] = board[c+20]
    for i in range(c+5,25,5):
        a = board[i]
        board[i] = temp
        temp = a
    return board

def move_up(board,c):
    temp = board[c]
    for i in range(c,20,5):
        board[i] = board[i+5]
    board[c+20] = temp
    return board

# return a list of possible successor states
def successors(board,path=[]):
    states = []
    for i in range(0,len(board),5):
        states.append((board[0:i]+board[i+1:i+5]+[board[i]]+board[i+5:],path+['L'+str(i//5+1)]))
        states.append((board[0:i]+[board[i+4]]+board[i:i+4]+board[i+5:],path+['R'+str(i//5+1)]))
    for i in  range(5):
        states.append((move_down(copy.deepcopy(board),i),path+['D'+str(i+1)]))
        states.append((move_up(copy.deepcopy(board),i),path+['U'+str(i+1)]))

    states.append((move_outer_clockwise(copy.deepcopy(board)), path+['Oc']))
    states.append((move_outer_cclockwise(copy.deepcopy(board)),path+['Occ']))
    states.append((rotate_inner_ring(copy.deepcopy(board),'c'),path+['Ic']))
    states.append((rotate_inner_ring(copy.deepcopy(board),'cc'),path+['Icc']))
    return states

def manhattan_distance(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])

def heuristic_function(state):
    cost = 0
    for i in range(len(state)):
        pos = (i//5,i%5)
        goal_pos = get_goal_position(state[i])
        cost += manhattan_distance(pos,goal_pos)
    return cost
# check if we've reached the goal
def is_goal(state):
    for i in range(len(state)):
        if state[i]!=i+1:
            return False        
    return True

def solve(initial_board):
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return 
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    fringe = PriorityQueue()
    fringe.put((0,(list(initial_board),[])))
    visited = []
    while fringe:
        (cost,board_map) = fringe.get()
        # print(board_map[0],len(board_map[1]))
        visited.append(board_map[0])
        for child in successors(board_map[0],board_map[1]):
            child_in_fringe = list(filter(lambda n: n[1][0]==child[0] and n[1][1]>child[1],(fringe.queue)))
            if is_goal(child[0]):
                return child[1]
            if child in visited:
                continue
            if child_in_fringe:
                updated_fringe = list(fringe.queue)
                for c in child_in_fringe:
                    updated_fringe.remove(c)
                fringe.queue = updated_fringe
            elif not list(filter(lambda n:n[1][0]==child[0],list(fringe.queue))):
                fringe.put((heuristic_function(child[0])+len(child[1]),child))
    return False

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
