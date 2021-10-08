#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: name IU ID
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#
import sys
from itertools import combinations
import random


def differenceOfLists(list1, list2):
    return (list(set(list1) - set(list2)))

# fitness = how expensive is a person/combination

def fitnessFunction(team,rTeam):
    aTeam=team.split('-')
    fitness=0
    for member in aTeam:
        userMap=list(filter(lambda user:user['user']==member,rTeam))[0]
        love=len(differenceOfLists(list(filter(lambda x:x not in ['xxx','zzz'],userMap['workWith'])),aTeam))*3
        hate=len([ member for member in aTeam if member in userMap['notWorkWith'] ])*10
        sizeAnomaly = 2 if len(userMap['workWith'])!=len(aTeam) else 0
        fitness += love + hate + sizeAnomaly
    return fitness
    
def solver(input_file):
    """
    1. This function should take the name of a .txt input file in the format indicated in the assignment.
    2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
        - "total-cost" : total cost (time spent by instructors in minutes) in the group assignment
    3. Do not add any extra parameters to the solver() function, or it will break our grading and testing code.
    4. Please do not use any global variables, as it may cause the testing code to fail.
    5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
       much time it will take to find the best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
       our test program will take the last answer you 'yielded' once time expired.
    """

    preferences = readInputFiles(input_file)
    names_comb = []
    names = [res.get('user') for res in preferences]
    # create every possible combination of names of sizes (1,2,3)
    names_comb = list(combinations(names,3))+list(combinations(names,2))+list(combinations(names,1))
    all_cost_combs = []
    # map combos with respective fitness
    for comb in names_comb:
        all_cost_combs.append((comb, fitnessFunction('-'.join(comb), preferences)))

    # sort the name combination in ASC of fitness 
    all_cost_combs = sorted(all_cost_combs,key=lambda x:x[1])
    final_combs = []
    final_names =[]
    final_cost = sys.float_info.max
    while True:
        for cost_comb in all_cost_combs:
                lowest_cost_comb = list(cost_comb)
                if not any([name in final_names for name in lowest_cost_comb[0]]):
                    final_combs.append(lowest_cost_comb)
                    final_names += lowest_cost_comb[0]

                # if a valid team 
                # yield if least cost till now
                if sorted(final_names)==sorted(names): 
                            current_groups = list(map(lambda x:'-'.join(x[0]),final_combs))
                            current_cost = sum(list(map(lambda x:x[1],final_combs)))+len(current_groups)*5
                            final_names = []
                            final_combs = []
                            if final_cost>current_cost:
                                final_cost = current_cost
                                yield {"assigned-groups":current_groups,"total-cost":final_cost}
        random.shuffle(all_cost_combs)

def parse_responses(path):
    names_dict = {}
    with open(path, "r") as f:
                for line in f.read().rstrip("\n").split("\n"):
                    names_dict[line.split()[0]] = line.split()[1:] 
    return names_dict

def readInputFiles(input_file):
    data = []
    with open(input_file, 'r') as file:
        for line in file:
            data.append([user for user in line.split()])

    def mapUserData(user):
        workWith = user[1].split('-')
        return {'user': user[0], 'workWith': workWith, 'notWorkWith': user[2].split(',')}
    return list(map(mapUserData, data))

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])
    
