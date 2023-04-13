import networkx as nx

# Initialize an array that will contain all of the distance vectors with 
# each iteration of the while loop 
dist_vecs = []

# Initialize an array that will contain all of the distance vectors with 
# each iteration of the while loop 
prev_node = []

def dijkstra(graph, start_node, end_node):
    """
    Finds the shortest path in a weighted graph using Dijkstra's algorithm.

    Args:
        graph (nx.Graph): A NetworkX graph object representing the weighted graph.
        start_node (any hashable type): The starting node for the shortest path.
        end_node (any hashable type): The end node for the shortest path.

    Returns:
        the shortest path as a list of nodes from source to destination.
    """
    global dist_vecs
    global prev_node
    temp = None

    # Initialize a list to keep track of the shortest distance to each node from the start node.
    distances = [float('inf')] * len(graph.nodes())
    distances[list(graph.nodes()).index(start_node)] = 0

    # Initialize a list to keep track of the parent node in the shortest path to each node.
    parent_nodes = [None] * len(graph.nodes())

    # Initialize a list to keep track of visited nodes.
    visited_nodes = [False] * len(graph.nodes())

    # Loop through all the nodes in the graph.
    while not all(visited_nodes):
        temp_dv = distances.copy()
        dist_vecs.append(temp_dv)

        temp_pn = parent_nodes.copy()
        new_pn = []
        # Populate parent nodes
        for i in temp_pn:
            if i is not None:
                new_pn.append(str(i+1))
            else:
                new_pn.append("N/A")
        prev_node.append(new_pn)

        # Find the unvisited node with the smallest distance from the start node.
        current_node_index = None
        current_node_distance = float('inf')
        for i in range(len(graph.nodes())):
            if not visited_nodes[i] and distances[i] < current_node_distance:
                current_node_index = i
                current_node_distance = distances[i]
            
        # Mark the current node as visited.
        visited_nodes[current_node_index] = True
        
        # Update the distances to all the neighboring nodes of the current node.
        for neighbor in graph.neighbors(list(graph.nodes())[current_node_index]):
            neighbor_index = list(graph.nodes()).index(neighbor)
            distance = distances[current_node_index] + int(graph[list(graph.nodes())[current_node_index]][neighbor]['weight'])
            if distance < distances[neighbor_index]:
                distances[neighbor_index] = distance
                parent_nodes[neighbor_index] = current_node_index


    # Backtrack from the end node to the start node to find the shortest path.
    shortest_path = [list(graph.nodes()).index(end_node)]
    current_node_index = shortest_path[0]
    while parent_nodes[current_node_index] is not None:
        shortest_path.insert(0, parent_nodes[current_node_index])
        current_node_index = parent_nodes[current_node_index]

    shortest_path = [list(graph.nodes())[i] for i in shortest_path]

    return shortest_path

def get_dist_vecs():
    '''A helper function that is used to retrieve 
    the distance vector array from frames.py'''
    return dist_vecs

def get_prev_node():
    '''A helper function that is used to retrieve 
    the list containing the parents nodes from frames.py'''
    return prev_node