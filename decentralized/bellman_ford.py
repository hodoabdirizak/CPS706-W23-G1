

import networkx as nx


def decentralized(graph: nx.Graph, start_node: int, end_node: int):

    dist_vecs = {n: ({m: float('inf') for m in graph.nodes()})
                 for n in graph.nodes()}

    for n in graph.nodes():
        dist_vecs[n][n] = 0

    for u, v, w in graph.edges(data='weight'):
        dist_vecs[u][v] = w
        dist_vecs[v][u] = w

    notify_neighbors = {n: True for n in graph.nodes()}

    # Loop

    dv_start_end = []

    t = 0
    while any(notify_neighbors.values()):

        # print(f'{notify_neighbors}')
        # print(f't = {t}')
        # for i, x in enumerate(dist_vecs):
        #     print(f'{i} = {list(dist_vecs[x].values())}')
        # print("\n\n")

        dv_start_end.append(
            {"dv_start": dist_vecs[start_node], "dv_end": dist_vecs[end_node]})

        dist_vecs_next = {}
        notify_neighbors_next = {n: False for n in graph.nodes()}

        for curr_network in graph.nodes():

            curr_network_dv = dist_vecs[curr_network].copy()

            for neighbor, attr in graph.adj[curr_network].items():
                weight = attr['weight']

                if not notify_neighbors[neighbor]:
                    continue

                for i, distance in dist_vecs[neighbor].items():
                    temp_distance = weight + distance

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

    # print(dv_start_end)
    # print(path)
    # print(cost)

    return dv_start_end, path, cost


# G = nx.Graph()

# nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8]
# nodes_str = [str(x) for x in nodes]
# G.add_nodes_from(nodes_str)

# # Image of graph: https://media.geeksforgeeks.org/wp-content/uploads/graphhh.png
# edges = [(0, 1, 4),
#          (0, 7, 8),
#          (1, 2, 8),
#          (1, 7, 11),
#          (7, 6, 1),
#          (7, 8, 7),
#          (2, 8, 2),
#          (8, 6, 6),
#          (2, 3, 7),
#          (2, 5, 4),
#          (3, 5, 14),
#          (3, 4, 9),
#          (5, 4, 10),
#          (6, 5, 2)]
# edges_str = [(str(s), str(e), w) for s, e, w in edges]
# G.add_weighted_edges_from(edges_str)


# start = '0'
# end = '8'
# decentralized(G, start, end)