#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: name IU ID
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#


# !/usr/bin/env python3
import sys
import math
from queue import PriorityQueue

def get_route(start, end, cost):
    
    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

    # route_taken = [("Martinsville,_Indiana","IN_37 for 19 miles"),
    #                ("Jct_I-465_&_IN_37_S,_Indiana","IN_37 for 25 miles"),
    #                ("Indianapolis,_Indiana","IN_37 for 7 miles")]
    path = []
    route_taken = []
    total_miles = 0.00
    total_hours = 0.00

    if cost == 'distance':
        path = shortest_distance(start, end)
        print(path)
    if cost == 'segments':
        path = least_segments(start, end)
    if cost == 'time':
        path = least_time(start, end)

    for p in path:
            total_miles += float(p[2])
            total_hours += (float(p[2])/float(p[3]))
            route_taken.append((p[1], f'{p[4]} for {p[2]} miles'))
    
    return {"total-segments" : len(route_taken), 
            "total-miles" : total_miles, 
            "total-hours" : total_hours, 
            "total-delivery-hours" : 1.1364, 
            "route-taken" : route_taken}

def shortest_distance(start, end):
    city_gps = parse_city_gps()
    end_city_coord = city_gps.get(end)

    road_segments = parse_road_segments()

    fringe_queue = PriorityQueue()
    fringe_queue.put((0, start, []))
    visited = []

    while not fringe_queue.empty():
        (cost, curr_city, path) = fringe_queue.get()
        if curr_city == end:
            return path
        for segment in road_segments:
            if segment in visited:
                continue
            if segment[1] == curr_city:
                segment[0], segment[1] = segment[1], segment[0]
            if segment[0] == curr_city:
                succ_city_coord = city_gps.get(segment[1])
                new_succ = (cost + haversine(succ_city_coord, end_city_coord), segment[1], path + [segment])
                fringe_queue.put(new_succ)
                visited.append(segment)
                print('FRINGE_SIZE:', fringe_queue.qsize())

    return []

def least_segments(start, end):
    city_gps = parse_city_gps()
    end_city_coord = city_gps.get(end)

    road_segments = parse_road_segments()

    fringe_queue = PriorityQueue()
    fringe_queue.put((0, start, []))
    visited = []

    while not fringe_queue.empty():
        (no_of_segments, curr_city, path) = fringe_queue.get()
        if curr_city == end:
            return path
        for segment in road_segments:
            if segment in visited:
                continue
            if segment[1] == curr_city:
                segment[0], segment[1] = segment[1], segment[0]
            if segment[0] == curr_city:
                succ_city_coord = city_gps.get(segment[1])
                new_succ = (no_of_segments + (haversine(succ_city_coord, end_city_coord)/25), segment[1], path + [segment])
                fringe_queue.put(new_succ)
                visited.append(segment)
                print('FRINGE_SIZE:', fringe_queue.qsize())

    return []

def least_time(start, end):
    city_gps = parse_city_gps()
    end_city_coord = city_gps.get(end)

    road_segments = parse_road_segments()

    fringe_queue = PriorityQueue()
    fringe_queue.put((0, start, []))
    visited = []

    while not fringe_queue.empty():
        (no_of_segments, curr_city, path) = fringe_queue.get()
        if curr_city == end:
            return path
        for segment in road_segments:
            if segment in visited:
                continue
            if segment[1] == curr_city:
                segment[0], segment[1] = segment[1], segment[0]
            if segment[0] == curr_city:
                succ_city_coord = city_gps.get(segment[1])
                new_succ = (no_of_segments + (haversine(succ_city_coord, end_city_coord)/50), segment[1], path + [segment])
                fringe_queue.put(new_succ)
                visited.append(segment)
                print('FRINGE_SIZE:', fringe_queue.qsize())

    return []
    



    



def parse_city_gps():
        with open('part2/city-gps.txt', "r") as f:
                return {line.split()[0]: tuple(line.split()[1:]) for line in f.read().rstrip("\n").split("\n")}

def parse_road_segments():
        with open('part2/road-segments.txt', "r") as f:
                return [line.split() for line in f.read().rstrip("\n").split("\n")]

# Calculate distance between two coordinates (Ref: https://janakiev.com/blog/gps-points-distance-python/)
def haversine(coord1, coord2):
    if coord1 == None or coord2 == None:
        return 0
    R = 6371  # Earth radius
    lat1, lon1 = (float(x) for x in coord1)
    lat2, lon2 = (float(x) for x in coord2)
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2) 
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))


# Please don't modify anything below this line
#
if __name__ == "__main__":
    
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])


