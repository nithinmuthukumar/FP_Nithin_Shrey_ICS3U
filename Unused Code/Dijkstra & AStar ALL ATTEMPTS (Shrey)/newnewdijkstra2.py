"""
Testing using online pathfinding that I modified to work with our game.
Never Used.
"""
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
    print(nodes_to_visit)
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

        edges = weighted_graph[current]
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


A="A"
B="B"
C="C"
D="D"

##graph = ({A, B, C, D},
##         {(A, B, 5), (B, A, 5), (B, C, 10), (B, D, 6), (C, D, 2), (D, C, 2)})

graph1 = {A:{B:5},B:{A:5},B:{C:10},B:{D:6},C:{D:2},D:{C:2}}

print(get_shortest_path(graph1,A,D))

##x = 1
##y = 2
##z = 3
##
##graph2 = {x:{z:1},z:{y:1}}
##
##print(get_shortest_path(graph2,x,y))

grid3 = []
for x in range(20):
    for y in range(10):
        grid3.append([x, y])

def neighbors(node):
    dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    result = []
    for dir in dirs:
        neighbor = [node[0] + dir[0], node[1] + dir[1]]
        if neighbor in grid3:
            result.append(neighbor)
    return result

##for i in range(len(grid3)):
##    print(neighbors(grid3[i]))
#print(grid3)

#grid4 = {chr(65+i) : {chr(65+i+1) : 1} if i%2==0 and i<4 else chr(65+i) : {chr() :1} for i in range(26)}
#print(get_shortest_path(grid4,'A','Z'))
#print(grid4)


#grid5 = {"(%i,%i)"%(x,y) : {} for x in range(10) for y in range(10)}
