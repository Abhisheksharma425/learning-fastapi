# A_B = {'node_name':'node_A','distance':'5', 'connected':'node_B'}
# A_C = {'node_name':'node_A','distance':'10','connected':'node_C'}

# graph = {
#     'A':[{'distance':5,'neighbour':'B'},{'distance':10,'neigbour':'C'}]
# }

# graph = {
#     'A':{'B':5,'C':10}
# }

graph = {
    'A':{'B':1,'C':4},
    'B':{'C':2,'D':5},
    'C':{'D':1},
    'D':{}
}

distances = {'A':0,'B':float('inf'),'C':float('inf'),'D':float('inf')}

visited = []
# unvisited_node = []

# # for i in 
# distances = {'A':0,'B':1,'C':4,'D':float('inf')}

# distances = {'A':0,'B':1,'C':3,'D':6} #checking the distance from node B to node C, if it is less than previous distance then we update new distance else not

# distances = {'A':0,'B':1,'C':3,'D':4}

#0<4 and then 1<4,2<4,3<4,4<4(exit)
while len(visited)<len(graph): 
    min_node = None
    sum_of_path = 0
    for key,value in distances.items():
        if key not in visited:
            if min_node is None or distances[key] < distances[min_node]:
                min_node = key
                # sum_of_path = value
    for key_min,value_min in graph[min_node].items():
        sum_of_path = distances[min_node] + value_min
        if sum_of_path < distances[key_min]:
            distances[key_min] = sum_of_path
    visited.append(min_node)
print(distances)
        # if distances[key_min] < distances[min_node]:
        #     min_node = key



    
        # if i not in visited:
        #     unvisited_node.append(i)
        #     continue
