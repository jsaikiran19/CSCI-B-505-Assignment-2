#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: name IU ID
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#

from itertools import combinations, permutations
from os import name
import sys
import time
from queue import PriorityQueue

def differenceOfLists(list1, list2):
    return (list(set(list1) - set(list2)))

def fitnessFunction(team,rTeam):
    aTeam=team.split('-')
    fitness=0
    for member in aTeam:
        userMap=list(filter(lambda user:user['user']==member,rTeam))[0]
        love=3 if any((pref not in ['xxx', 'zzz'] and pref not in aTeam) for pref in userMap['workWith']) else 0
        hate=len([ member for member in aTeam if member in userMap['notWorkWith'] ])*10
        sizeAnomaly = 2 if len(userMap['workWith'])==len(aTeam) else 0
        fitness += love + hate + sizeAnomaly + (3 - len(aTeam)) * 5
    return fitness

def calculateCost(teams, rTeam):
    # 1. grading time
    grading = len(teams) * 5

    # 2. Size mismatch time
    totalMissedSizes = 0
    totalMissFav = 0
    totalDeanTime=0

    for user in rTeam:
        for team in teams:
            if user['user'] in team:
                thisTeam = team.split('-')
                if len(thisTeam) != len(user['workWith']):
                    totalMissedSizes += 1
                # user fav team will not have user itself, and no preference is not considered
                userFavTeam = [member for member in user['workWith']
                               if member != user['user'] and member not in ['xxx', 'zzz']]
                # #people with whom the user may share code. 
                totalMissFav += len(differenceOfLists(userFavTeam,
                                    thisTeam))
                # #people with whom the user got assigned, against his choice
                userHateTeam = [ member for member in thisTeam if member in user['notWorkWith'] ]
                totalDeanTime += len(userHateTeam)
    

    return (totalDeanTime * 10 + totalMissedSizes * 2 + grading + totalMissFav * 3)


        

# def comput_cost(comb, preferences,costs = {}):
#         pref = preferences[comb[0]]
#         pref_list = pref[0].split('-')
#         comb_str = "-".join(comb)
#         cost = 0
        
#         if any([user not in comb and user not in ['xxx', 'zzz'] for user in pref[0].split('-')]):
#                 if comb[0] not in costs.keys():
#                     costs[comb[0]] = {comb_str:3}
#                 else:
#                     costs[comb[0]][comb_str] = costs[comb[0]][comb_str] + 3 if comb_str in costs[comb[0]].keys() else 3
#         if len(pref_list) == len(comb):
#             if all(user in pref[0] or 'xxx' in pref[0] for user in comb):
#                 if comb[0] not in costs.keys():
#                     # c = 0
#                     costs[comb[0]] = {comb_str:0}
#                 else:
#                     costs[comb[0]][comb_str] = costs[comb[0]][comb_str] if comb_str in costs[comb[0]].keys() else 0
#             # else:
#             #     # c = 3
#             #     if comb[0] not in costs.keys():
#             #         costs[comb[0]] = {comb_str:3}
#             #     else:
#             #         costs[comb[0]][comb_str] = costs[comb[0]][comb_str] + 3 if comb_str in costs[comb[0]].keys() else 3
#         else:
#             # c = 2
#             if comb[0] not in costs.keys():
#                 costs[comb[0]] = {comb_str:2}
#             else:
#                 costs[comb[0]][comb_str] = costs[comb[0]][comb_str] + 2 if comb_str in costs[comb[0]].keys() else 2
#         not_work_list = pref[1].split(',')
#         if any(p in comb for p in not_work_list):
#             # c = 10
#             if comb[0] not in costs.keys():
#                 costs[comb[0]] = {comb_str:10}
#             else:
#                 costs[comb[0]][comb_str] = costs[comb[0]][comb_str] + 10 if comb_str in costs[comb[0]].keys() else 10
#         return costs

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

    from itertools import combinations
    preferences = readInputFiles(input_file)
    names_comb = []
    names = [res.get('user') for res in preferences]
    names_comb = list(combinations(names,3))+list(combinations(names,2))+list(combinations(names,1))
    all_cost_combs = []
    for comb in names_comb:
        all_cost_combs.append((comb, fitnessFunction('-'.join(comb), preferences)))
    all_cost_combs = sorted(all_cost_combs,key=lambda x:x[1])
    final_combs = []
    final_names =[]
    import random
    final_cost = sys.float_info.max
    while True:
        for cost_comb in all_cost_combs:
                lowest_cost_comb = list(cost_comb)
                if not any([name in final_names for name in lowest_cost_comb[0]]):
                    final_combs.append(lowest_cost_comb)
                    final_names += lowest_cost_comb[0]
                if sorted(final_names)==sorted(names):
                            current_groups = list(map(lambda x:'-'.join(x[0]),final_combs))
                            current_cost = calculateCost(current_groups, preferences)
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
        # workWith.remove(user[0])
        return {'user': user[0], 'workWith': workWith, 'notWorkWith': user[2].split(',')}
    return list(map(mapUserData, data))

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])
    
