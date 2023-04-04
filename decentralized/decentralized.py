

import networkx as nx


def decentralized(graph: nx.Graph, start_node: int, end_node: int):

    num_networks = graph.number_of_nodes()

    dist_vecs = [[float('inf')] * num_networks for _ in range(num_networks)]

    for i in range(num_networks):
        dist_vecs[i][i] = 0

    for u, v, w in graph.edges(data='weight'):
        dist_vecs[u][v] = w
        dist_vecs[v][u] = w

    notify_neighbors = [True] * num_networks

    # Loop
    t = 0

    # print(f'{notify_neighbors}')
    print(f't = {t}')
    for i, x in enumerate(dist_vecs):
        print(f'{i} = {x}')
    print("\n\n")

    while any(notify_neighbors):
        t += 1

        dist_vecs_next = []
        notify_neighbors_next = [False] * num_networks

        for curr_network in range(num_networks):

            curr_network_dv = dist_vecs[curr_network][:]

            for neighbor, attr in graph.adj[curr_network].items():
                weight = attr['weight']

                if not notify_neighbors[neighbor]:
                    continue

                for i, distance in enumerate(dist_vecs[neighbor]):
                    temp_distance = weight + distance

                    if temp_distance < curr_network_dv[i]:
                        curr_network_dv[i] = temp_distance
                        notify_neighbors_next[curr_network] = True

            dist_vecs_next.append(curr_network_dv)

        dist_vecs = dist_vecs_next
        notify_neighbors = notify_neighbors_next

        # print(f'{notify_neighbors}')
        print(f't = {t}')
        for i, x in enumerate(dist_vecs):
            print(f'{i} = {x}')
        print("\n\n")

    
    
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

    print(path)
    print("cost", dist_vecs[start_node][end_node])


G = nx.Graph()

nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8]
G.add_nodes_from(nodes)


# Image of graph: https://media.geeksforgeeks.org/wp-content/uploads/graphhh.png
edges = [(0, 1, 4),
         (0, 7, 8),
         (1, 2, 8),
         (1, 7, 11),
         (7, 6, 1),
         (7, 8, 7),
         (2, 8, 2),
         (8, 6, 6),
         (2, 3, 7),
         (2, 5, 4),
         (3, 5, 14),
         (3, 4, 9),
         (5, 4, 10),
         (6, 5, 2)]


G.add_weighted_edges_from(edges)


start = 3
end = 7
decentralized(G, start, end)
