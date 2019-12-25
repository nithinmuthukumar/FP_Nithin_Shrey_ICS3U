"""
for x,y, in grid:
"""
"""
{A:{B:5}} --> {[x][y]:{[x+1][y]:1}}# right dir
"""
"""
        if x<=grid[-1]:
              --> {[x][y]:{[x+1][y]:1}}# right dir
        if y<=grid[x][-1]:
              --> {[x][y]:{[x][y+1]:1}}#down dir
        if x-1>=0:
              --> {[x][y]:{[x-1][y]:1}}#left dir
        if y-1>=0:
              --> {[x][y]:{[x][y-1]:1}}#up dir

BTW: Using Online Example for this Pathfinding Logic. Everything else
except the logic is mine.
"""
from collections import defaultdict
import pickle
def get_shortest_path(weighted_graph, start, end):
    """
    Calculate the shortest path for a directed weighted graph.

    Node can be virtually any hashable datatype.

    :param start: starting node
    :param end: ending node
    :param weighted_graph: {"node1": {"node2": "weight", ...}, ...}
    :return: ["START", ... nodes between ..., "END"] or None, if there is no
             path
    """

    # We always need to visit the start
    nodes_to_visit = {start}
    #print(nodes_to_visit)
    visited_nodes = set()
    # Distance from start to start is 0
    distance_from_start = {start: 0}
    tentative_parents = {}

    while nodes_to_visit:
        # The next node should be the one with the smallest weight
        current = min(
            [(distance_from_start[node], node) for node in nodes_to_visit]
        )[1]
        # The end was reached
        if current == end:
            break

        nodes_to_visit.discard(current)
        visited_nodes.add(current)

        edges = weighted_graph.get(current)
        unvisited_neighbours = set(edges).difference(visited_nodes)
        for neighbour in unvisited_neighbours:
            neighbour_distance = distance_from_start[current] + \
                                 edges[neighbour]
            if neighbour_distance < distance_from_start.get(neighbour,
                                                            float('inf')):
                distance_from_start[neighbour] = neighbour_distance
                tentative_parents[neighbour] = current
                nodes_to_visit.add(neighbour)

    return _deconstruct_path(tentative_parents, end)
def _deconstruct_path(tentative_parents, end):
    if end not in tentative_parents:
        return None
    cursor = end
    path = []
    while cursor:
        path.append(cursor)
        cursor = tentative_parents.get(cursor)
    return list(reversed(path))
def neighbors(x,y,width,height):
    neighborlist = []
    width,height = width-1,height-1
    for x2 in range(x-1,x+2):
        for y2 in range(y-1,y+2):
            if -1<x<=width and -1<y<=height and (x!=x2 or y!=y2) and 0<=x2<=width and 0<=y2<=height:
                neighborlist.append((x2,y2))
    return neighborlist
class add():    #lets me add additional duplicate keys
    def __init__(self,name):
      self.name = name
    def __repr__(self):
        return str(self.name)
def gridtodict(grid,rowlen=10,weight=1):
    pathdict = {}
    for x in range(len(grid[0])):
        for y in range(len(grid[0])):
            neighbor = neighbors(x,y,len(grid[0]),len(grid[0]))
            for neighbor in neighbors(x,y,rowlen,rowlen):
                key = x,y
                val = neighbor[0],neighbor[1]
                pathdict[(add(key))] = {(add(val)):weight}#pathdict[key] = {val:weight}#.append({val:weight})
    return pathdict
