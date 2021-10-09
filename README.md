# a1-forrelease
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