#
# For example, if the input graph was
# [(1, 2), (2, 3), (3, 1)]
# A possible Eulerian tour would be [1, 2, 3, 1]
# 3 nodes,
nodes = list()
edges = list()
#6 pontos
#11 vertices
#Solução  vertices + 1
#3 pontos
#3 vertices

def find_eulerian_tour(graph):
    visited = list()
    counter =0
    solution = list()
    solution.append(-1)
    for x in graph:
        solution.append(-1)
        visited.append(0)
        if x[0] not in edges:
            nodes.append(x[0])
        if x[1] not in nodes:
            nodes.append(x[1])
        edges.append(x)
        counter+=1

    bt(solution,0, visited)
solved=0
def bt(solution, curr, visited):
    if (curr==0):
        for x in nodes:
            solution[curr] = x
            bt(solution, curr+1,visited)
    elif curr+1 == len(visited):
        print("x:",solution)
    else:
        for i in range(0, len(edges)):
            if solution[curr -1] in edges[i] and (visited[i]==0):
                print()


find_eulerian_tour([(1, 2), (2, 3), (3, 1)])