import networkx as nx
import matplotlib.pyplot as plt
import random

import sys

random.seed(232)

def create_random_graph(num_routers, source, dest):
    '''returns a graph object based on a randomized graph '''
    # init graph object
    G = nx.Graph()

    # connect all nodes
    for i in range(1,num_routers):
        G.add_edge(str(i), str(i+1), weight=random.randint(1,11))

    # create random edges between nodes
    for i in range(1,num_routers//2):
        # if an edge between 2 nodes doesnt already exist
        if not G.has_edge(str(i), str(random.randint(i+1,num_routers+1))):
            G.add_edge(str(i), str(random.randint(i+1,num_routers+1)), weight=random.randint(1,11))

    # check if an extra node was added
    if len(G.nodes) > num_routers:
        G.remove_node(str(num_routers+1))

    # list of edges
    edges = [(u, v) for (u, v, d) in G.edges(data=True)]

    # display the network in a circular layout
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

    # saves graph to an image
    plt.savefig("gui/graph.png")
    
    # return the graph object
    return G

# create_random_graph(6, [])

def create_custom_graph(data):
    '''returns a graph object based on a customized graph'''
    # init graph object
    G = nx.Graph()

    # populate graph based on input data
    # structure of data list: [Node_A, Node_B, Cost, Node_A, Node_B, Cost, ...]

    for i in range(0, len(data), 3):
        G.add_edge(data[i], data[i + 1], weight=data[i + 2])

    # list of edges
    edges = [(u, v) for (u, v, d) in G.edges(data=True)]

    # display the network in a circular layout
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

    nm = plt.gca()
    nm.margins(0.08)
    plt.axis("off")
    plt.tight_layout()

    # saves graph to an image
    plt.savefig("gui/graph.png")

    # return the graph object
    return G