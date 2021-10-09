
# a1-forrelease

# Part-1 The 2021 Puzzle
The program implements an A* search with a Priority Queue. It maintains a visited array and keeps appending the successor states to the fringe based on the heursitic function until it finds the goal state. 

The goal state here is the state with sorted numbers from 1 to 25.

And the successors are the states that are obtained after making any of the valid 24 moves on a state.

Heuristic function used in this problem is manhattan distance.

The priority queue takes a tuple with 3 elements, the first one being f(n), second one h(n) and the child with its path.

The main challenge in this problem was to scale the heuristic function and to avoid priority collision, which are implemented by using a scaling factor and an extra element in queue.

The queue uses h(n) to avoid priority collisions, so if two states have same priority then the one with lower heuristic is popped from the queue.

The branching factor for the graph will be 24, because from any given state there are 24 possible successor states.

If the solution takes 7 moves with A*, it would require about 24^7 states for a simple BFS. (i.e b^n 'b' is branching factor and n is depth of the graph) 

# Part-3

## Initial thoughts on the problem
The question implicitly states that it is an optimization problem. There are many valid combination of members into teams of different team sizes and there exisits a minimum cost which we have to find. 
Since we don't know the goal state, we thought this can be solved using a local search.
Tried different variations of local search, however we couldn't realise what are the neighboring state for a given random start state. 
Then, we adopted randomised search approach to solve this problem with some optimization and a better state to start with.
## Problem formulation

1. State Space - All possible combination of members into teams such that each team has maximum 3 memebers in a team.
2. Successor Function - Takes any combination of teams -> yield cost, if the combination is valid and cost lesser than the recorded minimum.
3. Goal state - unknown 


## My solution 

The process to move towards a optimized team consist of 4 major steps

1. Expand all combination of members in all possible team sizes
2. Calculate how fit/unfit is every combination we made in the step 1.
3. sort the cost-user-map in ASC order of cost 

4. Repeat Forever -- >
                    - take the first element from the cost-user-map 
                    - Form valid teams
                    - yield the cost if it is least cost found till now
                    - shuffle the cost-user-map
                

Here the idea for search and optimization is that we start with a least probable cost combination and then randomise the search. 