import networkx as nx
import matplotlib.pyplot as plt
import random

import sys

random.seed(232)

def create_random_graph(num_routers, offline_routers, source, dest):
    '''returns a graph object based on a randomized graph '''
    # init graph object
    G = nx.Graph()

    # connect all nodes
    for i in range(1,num_routers):
        G.add_edge(str(i), str(i+1), weight=random.randint(1,11))

    for i in range(1,num_routers//2):
        # if an edge between 2 nodes doesnt already exist
        if not G.has_edge(str(i), str(random.randint(i+1,num_routers+1))):
            G.add_edge(str(i), str(random.randint(i+1,num_routers+1)), weight=random.randint(1,11))

    # add offline nodes
    for node in offline_routers:
        G.add_node(node)

    # check if an extra node was added
    if len(G.nodes) > num_routers:
        G.remove_node(str(num_routers+1))

    # if source and destination node are connected 
    if G.has_edge(str(source), str(dest)):
    # remove edge to make the path more complex
        G.remove_edge(str(source),str(dest))

    # list of edges
    edges = [(u, v) for (u, v, d) in G.edges(data=True)]

    pos = nx.circular_layout(G)  

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=500)

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=4, alpha=0.5)

    # node labels
    nx.draw_networkx_labels(G, pos, font_size=16, font_family="sans-serif")
    
    # edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=14, font_family="sans-serif")

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()

    print(G.nodes())
    # saves graph to an image
    plt.savefig("rand_graph.png")
    # print(dijkstra(G, '1', '5'))
    return G

# create_random_graph(6, [])

def create_custom_graph(data):
    '''returns a graph object based on a customized graph'''
    # init graph object
    G = nx.Graph()

    # populate graph based on input data
    
    # saves graph to an image
    plt.savefig("cust_graph.png")
    return G