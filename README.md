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