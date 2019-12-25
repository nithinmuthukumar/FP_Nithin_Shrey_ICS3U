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
Copy/Pasting Online Logic to Test Something.
"""
from collections import defaultdict
import pickle
def get_shortest_path(weighted_graph, start, end):
    """

    start is starting node
    end is ending node
    weighted_graph is {"node1": {"node2": "weight", ...}, ...}
    returns path ["START", ... nodes between ..., "END"] or None, if there is no
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
        #print(current)
        # The end was reached
        if current == end:
            break

        nodes_to_visit.discard(current)
        visited_nodes.add(current)

        edges = weighted_graph[current]#.get(current)
        #print(edges)
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

##def neighbors(grid,node):
##    dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
##    result = []
##    for dir in dirs:
##        neighbor = [node[0] + dir[0], node[1] + dir[1]]
##        print(node[0])
##        if neighbor in grid:
##            result.append(neighbor)
##    return result

##    for dir in dirs:
##        if node[0]+dir[0] in grid and node[1]+dir[1] in grid:
##            neighbor = [node[0] + dir[0], node[1] + dir[1]]
##            #print(node[0],dir[0],node[1],dir[1])
##            result.append(neighbor)
##            #if neighbor in grid:
##            #    result.append(neighbor)
##    return result

def neighbors(x,y,width,height):
    neighborlist = []
    width,height = width-1,height-1
    for x2 in range(x-1,x+2):
        for y2 in range(y-1,y+2):
            if -1<x<=width and -1<y<=height and (x!=x2 or y!=y2) and 0<=x2<=width and 0<=y2<=height:
                neighborlist.append((x2,y2))
    return neighborlist


grid5 = [
        [1],[0],[0],[0],[0],[0],[0],[0],[0],[0],
        [0],[0],[0],[0],[0],[0],[0],[0],[0],[0],
        [0],[0],[0],[0],[0],[0],[0],[0],[0],[0],
        [0],[0],[0],[0],[0],[0],[0],[0],[0],[0],
        [0],[0],[0],[0],[0],[0],[0],[0],[0],[0],
        [0],[0],[0],[0],[0],[0],[0],[0],[0],[0],
        [0],[0],[0],[0],[0],[0],[0],[0],[0],[0],
        [0],[0],[0],[0],[0],[0],[0],[0],[0],[0],
        [0],[0],[0],[0],[0],[0],[0],[0],[0],[0],
        [0],[0],[0],[0],[0],[0],[0],[0],[0],[2]
        ]

grid6 = [
        1,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,2
        ]

##grid7 = [
##        [1,0,0,0,0,0,0,0,0,0],
##        [0,0,0,0,0,0,0,0,0,0],
##        [0,0,0,0,0,0,0,0,0,0],
##        [0,0,0,0,0,0,0,0,0,0],
##        [0,0,0,0,0,0,0,0,0,0],
##        [0,0,0,0,0,0,0,0,0,0],
##        [0,0,0,0,0,0,0,0,0,0],
##        [0,0,0,0,0,0,0,0,0,0],
##        [0,0,0,0,0,0,0,0,0,0],
##        [0,0,0,0,0,0,0,0,0,2]
##        ]

grid7 = [
        [1,3,3,3,3,3,3,3,3,3],
        [3,3,3,3,3,3,3,3,3,3],
        [3,3,3,3,3,3,3,3,3,3],
        [3,3,3,3,3,3,3,3,3,3],
        [3,3,3,3,3,3,3,3,3,3],
        [3,3,3,3,3,3,3,3,3,3],
        [3,3,3,3,3,3,3,3,3,3],
        [3,3,3,3,3,3,3,3,3,3],
        [3,3,3,3,3,3,3,3,3,3],
        [3,3,3,3,3,3,3,3,3,2]
        ]

##print(neighbors(grid7[0],grid7[0][0],10,10))
##for x in range(10):#len(grid7)):
##    for y in range(10):#grid7[x]:
##        print(neighbors(x,y,10,10))
##print(neighbors(9,9,9,9))

#https://stackoverflow.com/questions/36154563/how-to-create-nested-dictionaries-with-duplicate-keys-in-python
##def items_in(d):
##    res = []
##    if isinstance(d, list):
##        res.extend(d)
##    elif isinstance(d, dict):
##        for k, v in d.items():
##            res.extend([k] * len(items_in(v)))
##    else:
##        raise ValueError('Unknown data')
##    return res

class add():    #lets me add additional duplicate keys
    def __init__(self,name):
      self.name = name
    def __repr__(self):
        return str(self.name)

##x = "x"
##xdict = {}
##xdict[add(x)] = 1
##print(xdict)
##y=1
##print(str(y))

def gridtodict(grid,rowlen=10,weight=1):
    pathdict = {}
#    pathdict = defaultdict(lambda:defaultdict(list))
    for x in range(len(grid[0])):
        for y in range(len(grid[0])):
            neighbor = neighbors(x,y,len(grid[0]),len(grid[0]))
            for neighbor in neighbors(x,y,rowlen,rowlen):
                key = x,y
                val = neighbor[0],neighbor[1]
                pathdict[(add(key))] = {(add(val)):weight}#pathdict[key] = {val:weight}#.append({val:weight})
##        try:
##            pathdict[x] = {x+1:weight}
##        except:
##            pass
##        try:
##            pathdict[x] = {x-1:weight}
##        except:
##            pass

##    for x in range(0,len(grid),rowlen):
##        for y in range(rowlen):
##            try:
##                pathdict[x] = {y+1:weight}
##            try:
##                pathdict[x] = {y+1:weight}
##            try:
##                pathdict[x] = {y+1:weight}
##            try:
##                pathdict[x] = {y+1:weight}
    return pathdict

##if grid==grid7:

grid7todict = gridtodict(grid7)
#pickle.dump(grid7todict,open('mapdict.p','wb'))    #write mode changed from w to wb as w raises TypeError

#Sprint(grid7todict)
#print(neighbors(8,7,10,10))
#print(str(list(grid7todict.keys())[0]))

start = list(grid7todict.keys())[0]
end = list(grid7todict.keys())[-1]
#print(start,end)

#print((9, 9) in grid7todict)
#print(grid7todict.get(start))
#print(grid7todict.get('(0, 0)'))
#print((0,7) in grid7todict.keys())#[v for k,v in grid7todict.items()])
print(get_shortest_path(grid7todict,start,end))
#gridtodict(grid6)
#print(gridtodict(grid6))

mapdict = []

##pathdict = {}
##pathdict["A"] = 5
##print(pathdict)
##pathdict["B"] = 6
##print(pathdict)
