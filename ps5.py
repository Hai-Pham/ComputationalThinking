# 6.00.2x Problem Set 5
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
# This imports everything from `graph.py` as if it was defined in this file!
from graph import * 

#
# Problem 2: Building up the Campus Map
#
# Before you write any code, write a couple of sentences here 
# describing how you will model this problem as a graph. 

# Each line in mit_map.txt has 4 pieces of data in it in the following order separated by a single space
# (space-delimited): the start building, the destination building, the distance in meters between the two buildings,
# and the distance in meters between the two buildings that must be spent outdoors.
# For example, suppose the map text file contained the following line:

# 10     32     200     40

# as a result, we can model the Campus Map as a Weighted Digraph, each edge has the following format
# source: [ [dest1,(totalDistance, outdoorDistance)], [dest2,(totalDistance, outdoorDistance)], ...]


def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    print "Loading map from file..."

    try:
        inFile = open(mapFilename, 'r')
    except IOError as e:
        print ("Cannot open file" + e)

    map = WeightedDigraph()

    for line in inFile:
        fr, to, d, o = line.split()
        # print fr, to, d, o
        na = Node(fr)
        nb = Node(to)
        if not map.hasNode(na): map.addNode(na)
        if not map.hasNode(nb): map.addNode(nb)
        map.addEdge(WeightedEdge(na, nb, float(d), float(o)))
    # print map
    return map


        


# List all the available paths using Brute-Force method
def findAllDFS(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if not graph.hasNode(start):
            return []
        paths = []
        for node in graph.childrenOf(start):
            if node not in path:
                newpaths = findAllDFS(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths






#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and what the constraints are
# FIND the shortest path satisfying 2 constraints: <= maxTotalDist and <= maxDistOutdoors
#


from operator import itemgetter

def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.

        Note: resolve the total distance with higher priority and then outdoor distance
    """

    # convert input to node to apply functions
    startNode = Node(start)
    endNode = Node(end)
    # list all the paths
    allPaths = findAllDFS(digraph, startNode, endNode)
    if allPaths == None: raise ValueError

    num_paths = len(allPaths)
    distances = []

    # calculate distance (total and outdoor) for each path listed
    for i in range(num_paths):
        d = 0
        o = 0

        tmpPath = allPaths[i]
        l = len(tmpPath)
        # calculate the distance for each found path
        for j in range(0, l-1):
            d += digraph.totalDistance(tmpPath[j], tmpPath[j+1])
            o += digraph.outdoorDistance(tmpPath[j], tmpPath[j+1])

        # record total distance and outdoor distance for each paths
        distances.append((i, d, o))

    # print distances
    # sort Total Distance first and then the Outdoor Distance
    sortedDistances = sorted(distances, key=itemgetter(1,2))

    # found = False
    for i in range(len(sortedDistances)):
        # process
        if sortedDistances[i][2] <= maxDistOutdoors and sortedDistances[i][1] <= maxTotalDist:
            idx = sortedDistances[i][0]
            # found = True
            return [str(n) for n in allPaths[idx]]
        else:
            continue

    raise ValueError


# g = WeightedDigraph()
# n1 = Node('1')
# n2 = Node('2')
# n3 = Node('3')
# n4 = Node('4')
# n5 = Node('5')
# for i in (n1, n2, n3, n4, n5): g.addNode(i)
# e1 = WeightedEdge(n1, n2, 5, 2)
# e2 = WeightedEdge(n3, n5, 5, 1)
# e3 = WeightedEdge(n2, n3, 20, 10)
# e4 = WeightedEdge(n2, n4, 10, 5)
# e5 = WeightedEdge(n4, n3, 5, 1)
# e6 = WeightedEdge(n4, n5, 20, 1)
# for i in (e1, e2, e3, e4, e5, e6): g.addEdge(i)
#
# path = findAllDFS(g, n1, n5)
# print path
#
# # print bruteForceSearch(g, "1", "3", 100, 100)
#
# print bruteForceSearch(g, "1", "5", 35, 9)

# print bruteForceSearch(g, "1", "3", 18, 0)
# print bruteForceSearch(g, "1", "3", 10, 10)


#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#

def directedDFS_Shortest(digraph, start, end, maxTotalDist, maxDistOutdoors, path=[]):
    """
    Recursive algorithm for Shortest path in DFS

    Parameters:
        start, end: node

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k.

    """

    path = path + [start]

    if start == end:
        return path
    if not digraph.hasNode(start):
        raise ValueError

    shortest = None
    for node in digraph.childrenOf(start):
        # print "loop for children of " + start.getName()
        d = maxTotalDist
        o = maxDistOutdoors
        if node not in path:
            d -= digraph.totalDistance(start, node)
            o -= digraph.outdoorDistance(start, node)
            # print "      at " + node.getName() + ", d = " + str(d) + ", o= " + str(o)
            # print "           call path from " + node.getName() + " to " + end.getName()

            if d < 0 or o < 0:
                # print "         !!!oops, not able to cover cost, skipping ..."
                continue

            newpath = directedDFS_Shortest(digraph, node, end, d, o, path)
            if newpath:
                if not shortest or (d >= 0 and o >=0):
                    # print "OK" + str(newpath)
                    shortest = newpath

                # just receive the first path only
                if start in shortest and end in shortest: break


    # print shortest
    return shortest




def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    startNode = Node(start)
    endNode = Node(end)

    shortest = directedDFS_Shortest(digraph, startNode, endNode, maxTotalDist, maxDistOutdoors)
    # print "Main program" + str(shortest)

    if not shortest: raise ValueError
    else:
        return [str(n) for n in shortest]




# g = WeightedDigraph()
# n1 = Node('1')
# n2 = Node('2')
# n3 = Node('3')
# n4 = Node('4')
# n5 = Node('5')
#
# for i in (n1, n2, n3, n4, n5): g.addNode(i)
# e1 = WeightedEdge(n1, n2, 5, 2)
# e2 = WeightedEdge(n3, n5, 6, 3)
# e3 = WeightedEdge(n2, n3, 20, 10)
# e4 = WeightedEdge(n2, n4, 10, 5)
# e5 = WeightedEdge(n4, n3, 2, 1)
# e6 = WeightedEdge(n4, n5, 20, 10)
# for i in (e1, e2, e3, e4, e5, e6): g.addEdge(i)
#
# path = directedDFS(g, "4", "5", 21, 11)
# print path

# g = WeightedDigraph()
# n1 = Node('1')
# n2 = Node('2')
# n3 = Node('3')
# n4 = Node('4')
# for i in (n1, n2, n3, n4): g.addNode(i)
# e1 = WeightedEdge(n1, n2, 10, 5)
# e3 = WeightedEdge(n2, n3, 8, 5)
# e2 = WeightedEdge(n1, n4, 5, 1)
# e4 = WeightedEdge(n4, n3, 8, 5)
# for i in (e1, e2, e3, e4): g.addEdge(i)
#
# path = directedDFS(g, "1", "3", 18, 18)
# print path




# Uncomment below when ready to test
### NOTE! These tests may take a few minutes to run!! ####
# if __name__ == '__main__':
#     # Test cases
#     mitMap = load_map("mit_map.txt")
#     print isinstance(mitMap, Digraph)
#     print isinstance(mitMap, WeightedDigraph)
#     print 'nodes', mitMap.nodes
#     print 'edges', mitMap.edges
#
#
#     LARGE_DIST = 1000000

    # Test case 1
    # print "---------------"
    # print "Test case 1:"
    # print "Find the shortest-path from Building 32 to 56"
    # expectedPath1 = ['32', '56']
    # brutePath1 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
    # print brutePath1
    # dfsPath1 = directedDFS(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
    # print "Expected: ", expectedPath1
    # print "Brute-force: ", brutePath1
    # print "DFS: ", dfsPath1
    # print "Correct? BFS: {0}; DFS: {1}".format(expectedPath1 == brutePath1, expectedPath1 == dfsPath1)

#     Test case 2
#     print "---------------"
#     print "Test case 2:"
#     print "Find the shortest-path from Building 32 to 56 without going outdoors"
#     expectedPath2 = ['32', '36', '26', '16', '56']
#     brutePath2 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, 0)
#     dfsPath2 = directedDFS(mitMap, '32', '56', LARGE_DIST, 0)
#     print "Expected: ", expectedPath2
#     print "Brute-force: ", brutePath2
#     print "DFS: ", dfsPath2
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath2 == brutePath2, expectedPath2 == dfsPath2)

#     Test case 3
#     print "---------------"
#     print "Test case 3:"
#     print "Find the shortest-path from Building 2 to 9"
#     expectedPath3 = ['2', '3', '7', '9']
#     brutePath3 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
#     dfsPath3 = directedDFS(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
#     print "Expected: ", expectedPath3
#     print "Brute-force: ", brutePath3
#     print "DFS: ", dfsPath3
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath3 == brutePath3, expectedPath3 == dfsPath3)

#     Test case 4
#     print "---------------"
#     print "Test case 4:"
#     print "Find the shortest-path from Building 2 to 9 without going outdoors"
#     expectedPath4 = ['2', '4', '10', '13', '9']
#     brutePath4 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, 0)
#     dfsPath4 = directedDFS(mitMap, '2', '9', LARGE_DIST, 0)
#     print "Expected: ", expectedPath4
#     print "Brute-force: ", brutePath4
#     print "DFS: ", dfsPath4
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath4 == brutePath4, expectedPath4 == dfsPath4)

#     Test case 5
#     print "---------------"
#     print "Test case 5:"
#     print "Find the shortest-path from Building 1 to 32"
#     expectedPath5 = ['1', '4', '12', '32']
#     brutePath5 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
#     dfsPath5 = directedDFS(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
#     print "Expected: ", expectedPath5
#     print "Brute-force: ", brutePath5
#     print "DFS: ", dfsPath5
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath5 == brutePath5, expectedPath5 == dfsPath5)

#     Test case 6
#     print "---------------"
#     print "Test case 6:"
#     print "Find the shortest-path from Building 1 to 32 without going outdoors"
#     expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
#     brutePath6 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, 0)
#     dfsPath6 = directedDFS(mitMap, '1', '32', LARGE_DIST, 0)
#     print "Expected: ", expectedPath6
#     print "Brute-force: ", brutePath6
#     print "DFS: ", dfsPath6
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath6 == brutePath6, expectedPath6 == dfsPath6)

#     Test case 7
#     print "---------------"
#     print "Test case 7:"
#     print "Find the shortest-path from Building 8 to 50 without going outdoors"
#     bruteRaisedErr = 'No'
#     dfsRaisedErr = 'No'
#     try:
#         bruteForceSearch(mitMap, '8', '50', LARGE_DIST, 0)
#     except ValueError:
#         bruteRaisedErr = 'Yes'
    
#     try:
#         directedDFS(mitMap, '8', '50', LARGE_DIST, 0)
#     except ValueError:
#         dfsRaisedErr = 'Yes'
    
#     print "Expected: No such path! Should throw a value error."
#     print "Did brute force search raise an error?", bruteRaisedErr
#     print "Did DFS search raise an error?", dfsRaisedErr

#     Test case 8
#     print "---------------"
#     print "Test case 8:"
#     print "Find the shortest-path from Building 10 to 32 without walking"
#     print "more than 100 meters in total"
#     bruteRaisedErr = 'No'
#     dfsRaisedErr = 'No'
#     try:
#         bruteForceSearch(mitMap, '10', '32', 100, LARGE_DIST)
#     except ValueError:
#         bruteRaisedErr = 'Yes'
    
#     try:
#         directedDFS(mitMap, '10', '32', 100, LARGE_DIST)
#     except ValueError:
#         dfsRaisedErr = 'Yes'
    
#     print "Expected: No such path! Should throw a value error."
#     print "Did brute force search raise an error?", bruteRaisedErr
#     print "Did DFS search raise an error?", dfsRaisedErr
