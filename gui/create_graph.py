import networkx as nx
import matplotlib.pyplot as plt
import random

import sys
sys.path.append('./centralized')
from dijkstra import * 

random.seed(232)

def create_random_graph(num_routers, offline_routers):
    '''returns a graph object based on a randomized graph '''
    # init graph object
    G = nx.Graph()

    # connect all nodes
    for i in range(1,num_routers):
        G.add_edge(str(i), str(i+1), weight=random.randint(1,11))

    # add random nodes
    for i in range(1,num_routers-2):
        # if an edge between 2 nodes doesnt already exist
        # if not G.has_edge(str(i), str(random.randint(i+1,num_routers+1))):
            # add an edge between the 
        G.add_edge(str(i), str(random.randint(i+1,num_routers+1)), weight=random.randint(1,10))

    # add offline nodes
    for node in offline_routers:
        G.add_node(node)

    # list of edges
    edges = [(u, v) for (u, v, d) in G.edges(data=True)]

    pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=700)

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=6, alpha=0.5)

    # node labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    
    # edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=15, font_family="sans-serif")

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()

    # saves graph to an image
    plt.savefig("rand_graph.png")
    # print(dijkstra(G, '1', '5'))
    return G

def create_custom_graph(data):
    '''returns a graph object based on a customized graph'''
    # init graph object
    G = nx.Graph()

    # populate graph based on input data
    
    # saves graph to an image
    plt.savefig("cust_graph.png")
    return G