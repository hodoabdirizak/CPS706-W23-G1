

import networkx as nx


def decentralized(graph: nx.Graph, start_node: int, end_node: int):

    # Create dictionary to assign each network its own distance vector
    # By default cost will be set to infinity
    dist_vecs = {n: ({m: float('inf') for m in graph.nodes()})
                 for n in graph.nodes()}

    # Assign cost to network itself as 0
    for n in graph.nodes():
        dist_vecs[n][n] = 0

    # Assign cost to neighbors, the weight between them
    for u, v, w in graph.edges(data='weight'):
        dist_vecs[u][v] = w
        dist_vecs[v][u] = w

    # Create a dictionary to indicate whether a network was updated and needs to notify its neighbors
    notify_neighbors = {n: True for n in graph.nodes()}

    # A list to return the distance vectors of the starting and ending network as the algorithm progresses
    dv_start_end = []

    t = 0
    while any(notify_neighbors.values()):

        # Save distance vector of starting/ending network at time=t
        dv_start_end.append(
            {"dv_start": dist_vecs[start_node], "dv_end": dist_vecs[end_node]})

        # Temporary dictionaries for dist_vecs and notify_neighbors to be used in next iteration
        dist_vecs_next = {}
        notify_neighbors_next = {n: False for n in graph.nodes()}

        # Send distance vectors to neighbors and update vectors if lower cost possible
        for curr_network in graph.nodes():

            curr_network_dv = dist_vecs[curr_network].copy()

            for neighbor, attr in graph.adj[curr_network].items():
                weight = attr['weight']

                if not notify_neighbors[neighbor]:
                    continue

                for i, distance in dist_vecs[neighbor].items():
                    if (isinstance(distance, float)):
                        temp_distance = int(weight) + distance
                    else:
                        temp_distance = int(weight) + int(distance)
                    if (isinstance(curr_network_dv[i], str)):
                        if temp_distance < int(curr_network_dv[i]):
                            curr_network_dv[i] = temp_distance
                            notify_neighbors_next[curr_network] = True
                    else:
                        if temp_distance < curr_network_dv[i]:
                            curr_network_dv[i] = temp_distance
                            notify_neighbors_next[curr_network] = True

            dist_vecs_next[curr_network] = curr_network_dv

        dist_vecs = dist_vecs_next
        notify_neighbors = notify_neighbors_next

        t += 1

    # At this point all Distance-Vectors for each network have been computed
    # We start with the starting network and use the DVs of its nieghbors to choose
    # the lowest cost path, and continue to do this until the end network is found
    path = []
    curr_node = start_node
    while curr_node != end_node:
        path.append(curr_node)

        low_node = None
        low_cost = float('inf')
        for neighbor, attr in graph.adj[curr_node].items():
            weight = attr['weight']

            cost = weight + dist_vecs[neighbor][end_node]

            if cost < low_cost:
                low_node = neighbor
                low_cost = cost
        curr_node = low_node

    path.append(end_node)

    cost = dist_vecs[start_node][end_node]

    return dv_start_end, path, cost