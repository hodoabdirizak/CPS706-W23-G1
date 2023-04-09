import networkx as nx
import heapq

def dijkstra_table(graph, start, end):
    # Initialize the distance to each node to infinity and the previous node to None
    dist = {node: float('inf') for node in graph.nodes}
    prev = {node: None for node in graph.nodes}
    
    # The distance to the start node is 0
    dist[start] = 0
    
    # Initialize the priority queue with the start node and its distance
    pq = [(0, start)]
    
    # Keep track of the nodes that have been visited
    visited = set()
    
    # Print the table header
    print(f"{'Node':<5}{'Distance':<10}{'Previous':<10}")
    
    # Loop until we have visited all nodes or found the end node
    while pq:
        # Get the node with the smallest distance from the start node
        curr_dist, curr_node = heapq.heappop(pq)
        
        # If we have already visited this node, skip it
        if curr_node in visited:
            continue
        
        # Mark the node as visited
        visited.add(curr_node)
        
        # Update the distances to the node's neighbors
        for neighbor in graph.neighbors(curr_node):
            new_dist = dist[curr_node] + graph[curr_node][neighbor]['weight']
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = curr_node
                heapq.heappush(pq, (new_dist, neighbor))
        
        # Print the current state of the table
        print(f"{curr_node:<5}{dist[curr_node]:<10}{prev[curr_node] if prev[curr_node] is not None else '-':<10}")
        
        # If we have found the end node, we're done
        if curr_node == end:
            break
    
        # If we didn't find the end node, print a message
        if dist[end] == float('inf'):
            print("No path found")
        else:
            # Print the shortest path from the start node to the end node
            path = [end]
            while prev[path[-1]] is not None:
                path.append(prev[path[-1]])
            path.reverse()
            print("Shortest path:", "->".join(path))


# Create a graph with weighted edges
graph = nx.Graph()
graph.add_edge('A', 'B', weight=1)
graph.add_edge('A', 'C', weight=4)
graph.add_edge('B', 'D', weight=3)
graph.add_edge('C', 'D', weight=2)
graph.add_edge('D', 'E', weight=1)

# Call the dijkstra_table function with start node 'A' and end node 'E'
dijkstra_table(graph, 'A', 'E')














