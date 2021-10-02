#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: name IU ID
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#

import sys
import time
from queue import PriorityQueue

def comput_cost(comb, preferences,costs = {}):
        pref = preferences[comb[0]]
        pref_list = pref[0].split('-')
        comb_str = "-".join(comb)
        cost = 0
        # if comb == ['fanjun', 'djcran']:
        #     print(pref_list, comb)
        
        if any([user not in comb and user != 'xxx' for user in pref[0].split('-')]):
                if comb[0] not in costs.keys():
                    costs[comb[0]] = {comb_str:3}
                else:
                    costs[comb[0]][comb_str] = costs[comb[0]][comb_str] + 3 if comb_str in costs[comb[0]].keys() else 3
        if len(pref_list) == len(comb):
            if all(user in pref[0] or 'xxx' in pref[0] for user in comb):
                if comb[0] not in costs.keys():
                    # c = 0
                    costs[comb[0]] = {comb_str:0}
                else:
                    costs[comb[0]][comb_str] = costs[comb[0]][comb_str] if comb_str in costs[comb[0]].keys() else 0
            # else:
            #     # c = 3
            #     if comb[0] not in costs.keys():
            #         costs[comb[0]] = {comb_str:3}
            #     else:
            #         costs[comb[0]][comb_str] = costs[comb[0]][comb_str] + 3 if comb_str in costs[comb[0]].keys() else 3
        else:
            # c = 2
            if comb[0] not in costs.keys():
                costs[comb[0]] = {comb_str:2}
            else:
                costs[comb[0]][comb_str] = costs[comb[0]][comb_str] + 2 if comb_str in costs[comb[0]].keys() else 2
        not_work_list = pref[1].split(',')
        if any(p in comb for p in not_work_list):
            # c = 10
            if comb[0] not in costs.keys():
                costs[comb[0]] = {comb_str:10}
            else:
                costs[comb[0]][comb_str] = costs[comb[0]][comb_str] + 10 if comb_str in costs[comb[0]].keys() else 10
        return costs

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
    import copy
    from itertools import permutations
    preferences = parse_responses(input_file)
    names_comb = []
    fringe = PriorityQueue()
    names = [res for res in preferences.keys()]
    names_comb = list(permutations(names,3))+list(permutations(names,2))+list(permutations(names,1))
    # for i in range(len(names)):
    #     names_copy = copy.deepcopy(names)
    #     names_copy.remove(names[i])
    #     for j in range(len(names_copy)-1):
    #         pref = preferences[names[i]][0].split('-')
    #         names_comb.append([names[i],names_copy[j],names_copy[j+1]])
    #         if len(pref)==1:
    #            names_comb.append([names[i]])
    #         elif len(pref)==2:
    #             names_comb.append([names[i],names_copy[j]])
    # print(len(names_comb))
    costs = {}
    for comb in names_comb:
        costs = comput_cost(comb,preferences)
    final_combs = []
    final_names =[]
    all_cost_combs = []
    all_solutions = []
    for user in costs.keys():
        sorted_cost_combs = list(costs[user].items())
        all_cost_combs+=sorted_cost_combs
    # print(all_cost_combs)
    import random
    final_cost = sys.float_info.max
    while True:
        for cost_comb in all_cost_combs:
                lowest_cost_comb = list(cost_comb)
                if all([name not in final_names for name in lowest_cost_comb[0].split('-')]):
                    lowest_cost_comb_list = lowest_cost_comb[0].split('-')
                    if len(lowest_cost_comb_list) == 3:
                        lowest_cost_comb[1] += costs[lowest_cost_comb_list[1]][f'{lowest_cost_comb_list[1]}-{lowest_cost_comb_list[0]}-{lowest_cost_comb_list[2]}']
                        lowest_cost_comb[1] += costs[lowest_cost_comb_list[2]][f'{lowest_cost_comb_list[2]}-{lowest_cost_comb_list[0]}-{lowest_cost_comb_list[1]}']
                    if len(lowest_cost_comb_list) == 2:
                        lowest_cost_comb[1] += costs[lowest_cost_comb_list[1]][f'{lowest_cost_comb_list[1]}-{lowest_cost_comb_list[0]}']
                    final_combs.append(lowest_cost_comb)
                    final_names += lowest_cost_comb[0].split('-')
                if sorted(final_names)==sorted(names):
                            current_groups = list(map(lambda x:x[0],final_combs))
                            current_cost = sum(list(map(lambda x:x[1],final_combs)))+len(current_groups)*5
                            if final_cost>current_cost:
                                final_cost = current_cost
                                final_names = []
                                final_combs = []
                                yield {"assigned-groups":current_groups,"total-cost":final_cost}
        random.shuffle(all_cost_combs)
            # c =0
            # for name in lowest_cost_comb[0].split('-'):
            #     if name in final_names:
            #         break
            #     else:
            #         c+=1
            # if c==len(lowest_cost_comb[0].split('-')):
            #     final_combs.append(lowest_cost_comb)
            #     final_names+=lowest_cost_comb[0].split('-')
    # print(final_names)
    # print(final_combs)

    # print((costs))
        # if True:
        #     if comb[1] in pref[0] and comb[2] in pref[0]:
        #         print('if1')
        #         if comb[0] not in costs.keys():
        #             costs[comb[0]] = {"-".join(comb):0}
        #         else:
        #             costs[comb[0]][comb_str] = costs[comb[0]][comb_str] if comb_str in costs[comb[0]].keys() else 0 
        #     elif comb[1] in pref[0] or comb[2] in pref[0]:
        #         print('if2')
        #         if comb[0] not in costs.keys():
        #             costs[comb[0]] = {"-".join(comb):2}
        #         else:
        #             costs[comb[0]][comb_str] = costs[comb[0]][comb_str] + 2 if comb_str in costs[comb[0]].keys() else 2
        #     else:
        #         if comb[0] not in costs.keys():
        #             costs[comb[0]] = {"-".join(comb):4}
        #         else:
        #             costs[comb[0]][comb_str] = costs[comb[0]][comb_str] + 4 if comb_str in costs[comb[0]].keys() else 4
        #     if pref[1] in comb:
        #         if comb[0] not in costs.keys():
        #             costs[comb[0]] = {"-".join(comb):10}
        #         else:
        #             costs[comb[0]][comb_str] = costs[comb[0]][comb_str] + 10 if comb_str in costs[comb[0]].keys() else 10
        
    # print(len(names_comb))
    # Simple example. First we yield a quick solution
    # yield({"assigned-groups": ["vibvats-djcran-zkachwal", "shah12", "vrmath"],
    #            "total-cost" : 12})

    # # Then we think a while and return another solution:
    # time.sleep(10)
    # yield({"assigned-groups": ["vibvats-djcran-zkachwal", "shah12-vrmath"],
    #            "total-cost" : 10})

    # This solution will never befound, but that's ok; program will be killed eventually by the
    #  test script.
    # while True:
    #     pass
    
    # yield({"assigned-groups": ["vibvats-djcran", "zkachwal-shah12-vrmath"],
    #            "total-cost" : 9})

def parse_responses(path):
    names_dict = {}
    with open(path, "r") as f:
                for line in f.read().rstrip("\n").split("\n"):
                    names_dict[line.split()[0]] = line.split()[1:] 
    return names_dict

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])
    
