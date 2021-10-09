
# a1-forrelease

# Part-1 The 2021 Puzzle
The program implements an A* search with a Priority Queue. It maintains a visited array and keeps appending the successor states to the fringe based on the heursitic function until it finds the goal state. 

<b>State-space:</b> Set of all possible permutations of an array from 1 to 25<br>
<b>Successor function:</b> the states are obtained after making any of the valid 24 moves on a state.<br>
<b>Goal state:</b> the state with sorted numbers from 1 to 25.<br>


Heuristic function used in this problem is manhattan distance.

The priority queue takes a tuple with 3 elements, the first one being f(n), second one h(n) and the child with its path.

The main challenge in this problem was to scale the heuristic function and to avoid priority collision, which are implemented by using a scaling factor and an extra element in queue.

The queue uses `h(n)` to avoid priority collisions, so if two states have same priority then the one with lower heuristic is popped from the queue.

Other heuristic function we tried was the combination of manhatten and misplaced tiles (`h(n) = (manhatten*0.25 + misplaced_tiles*0.125)/2`) which was working well for most of the boards but was taking too long to solve board1.txt. 

Average branching factor for the graph will be 2.4.<br>
If the solution takes 7 moves with A*, it would require about 24^7 states for a simple BFS. (i.e b^n 'b' is branching factor and n is depth of the graph)

# Part-2: Road trip!

For all the parts of this problem, we used PriorityQueue to implement the A* search. After calculating the heuristic value, we put `f(n) = g(n) + h(n)` as cost in the priority queue with other relevant data.

### <b>Parsing Road Segments</b>
While parsing the road-segments.txt file, we are creating a list of dictionary which contains all the successors of a particular node. For that we make a list of all edges which contains a particular node. So that would look something like this...
```
[
    {
        node1: [
            [node1, node2, distance, speed_limit, highway_name],
            [node1, node3, distance, speed_limit, highway_name]
        ]
    }
]
```
### <b>Parsing GPS Coordinates</b>
For parsing city-gps.txt, we created a list of dictionary which contains tuple of coordinates for each city.
```
[
    {
        node1: (lat, long),
        node2: (lat, long),
        node3: (lat, long)
    }
]
```
    

### <b>Distance Part</b>
This part tries to minimize the distance between two cities.<br>
Now, information available with us:
- Possible Edges between two cities/intersections with distance, speed limit and highway name
- GPS coordinates of the all the cities

Looking at the GPS coordinates, the first thing came in our mind was to use haversine distance between two nodes as a heurisitc. For Calculating haversine distance we have to do some complex mathematical operations, that's why we refered that calculation from this source (https://janakiev.com/blog/gps-points-distance-python/).

Haversine determines the great circle distance between two cities using the latitudes and longitudes. After using this as a heuristic, we got some good results, but not the best ones. 
According to us, haversine must be overestimating values for very small edges. To overcome that we scaled the heuristic by dividing it by 2. After changing this, the algorithm started giving optimal solutions.
<br>
> Heuristic used: `haversine_distance/2` where 2 is scaling factor

### <b>Segments Part</b>
This part tries to minimize the number of segments between two cities.<br>
For getting the approximate number of segments to reach the goal, we tried to divide the haverine distance by the average segment distance. But that will also overestimate for some cases. So we came up with another approach, in which we divide the haversine distance with the largest segment distance. So this will never overestimate.
<br>
> Heuristic used: `haversine_distance/923` where 923 is largest segment distance

### <b>Time Part</b>
This part tries to minimize time taken to travel between two cities assuming that the driver drives at the speed limit.<br>
So to calculate time, we need distance and speed. Distance we can consider haversine but speed we cannot know beforehand. Therfore, we took the same approach as segments part, which is to divide the haversine distance by the highest speed (which is 65). But that didn't work well in some of the cases.<br>
So after trying to come up with another heuristic for time and failing, we thought to scale the previous heuristic because it might be overestimating some values. Therefore scaled the heuristic by 1.5.
<br>
> Heuristic used: `(haversine_distance/65)/1.5` where 65 is the maximum speed limit and 1.5 is scaling factor


### <b>Delivery Part</b>
This part tries to minimize time for a delivery person who drops the package sometimes if the speed limit is more than 50.<br>
Coming up with heuristic for this part was the most difficult. We were not able to think of a way to calculate approximate number of times when there would be speed limit greater than 50. So what we thought, anyway we are trying to minimize time here. So why not use the same heuristic we used for time and change the `g(n)` for this case.<br>
So it would be... `h(n) = haversine_distance/90` and `g(n) = actual_delivery_hours_till_now`. After trying these values, the algorithm is giving optimal solutions.
<br>
> Heuristic used: `(haversine_distance/65)/1.5` where 65 is the maximum speed limit and 1.5 is scaling factor.
<br>
<br>
---
<b>State-space:</b> All the possible cities we can reach from the start city.<br>
<b>Successor function:</b> All the possible segments which has the current city as one of the node. (Considering two way roads)<br>
<b>Edge weights:</b> Edge weights here are the distances between two nodes.<br>
<b>Goal state:</b> Goal state is the end city<br>
<b>How the search algorithm works:</b><br>
> 1. Calculate `f(n)` using the actual cost and heuristic
> 2. Put it in priority queue with other relavant data
> 3. Pop the lowest cost item from the priority queue
> 4. Get successors and check for goal state
> 5. Put the successor in priority queue
> 6. Repeat until goal state is found
<br>

# Part-3: Choosing teams

## Initial thoughts on the problem
The question implicitly states that it is an optimization problem. There are many valid combination of members into teams of different team sizes and there exisits a minimum cost which we have to find. 
Since we don't know the goal state, we thought this can be solved using a local search.
Tried different variations of local search, however we couldn't realise what are the neighboring state for a given random start state. 
Then, we adopted randomised search approach to solve this problem with some optimization and a better state to start with.
## Problem formulation

1. State Space - All possible combination of members into teams such that each team has maximum 3 members in a team.
2. Successor Function - Takes any combination of teams -> yield cost, if the combination is valid and cost lesser than the recorded minimum.
3. Goal state - unknown 


## Our solution 

The process to move towards a optimized team consist of 4 major steps

1. Expand all combination of members in all possible team sizes
2. Calculate how fit/unfit is every combination we made in the step 1.
3. Sort the cost-user-map in ASC order of cost 

4. Repeat Forever -- >
                    <br>- take the first element from the cost-user-map 
                    <br>- Form valid teams
                    <br>- yield the cost if it is least cost found till now
                    <br>- shuffle the cost-user-map
                

Here the idea for search and optimization is that we start with a least probable cost combination and then randomise the search. 