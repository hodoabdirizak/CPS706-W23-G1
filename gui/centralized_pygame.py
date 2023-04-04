import pygame
pygame.init()
import networkx as nx

# Define constants for the window size and node radius
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
NODE_RADIUS = 15

# Define colors for the nodes and edges
NODE_COLOR = (255, 255, 255)
EDGE_COLOR = (255, 255, 255)

# Define the font for the node labels
FONT = pygame.font.Font(None, 30)

def draw_graph(screen, graph, path, current_node):
    # Clear the screen
    screen.fill((0, 0, 0))
    
    # Draw the edges
    for u, v in graph.edges():
        u_pos = graph.nodes[u]["pos"]
        v_pos = graph.nodes[v]["pos"]
        weight = str(graph[u][v]['weight'])
        label = FONT.render(weight, True, EDGE_COLOR)
        label_pos = ((u_pos[0] + v_pos[0])/2, (u_pos[1] + v_pos[1])/2)
        screen.blit(label, label_pos)
        pygame.draw.line(screen, EDGE_COLOR, u_pos, v_pos)

    # Draw the nodes
    for node in graph.nodes():
        pos = graph.nodes[node]["pos"]
        color = NODE_COLOR
        if node in path:
            if node == current_node:
                color = (255, 0, 0)
            else:
                color = (0, 255, 0)
        pygame.draw.circle(screen, color, pos, NODE_RADIUS)
        
        # Draw the label
        label = FONT.render(str(node), True, (255, 255, 255))
        label_pos = (pos[0] - NODE_RADIUS/2, pos[1] - NODE_RADIUS/2)
        screen.blit(label, label_pos)
        
        # Draw the current node label
        if node == current_node:
            label = FONT.render(" Current Router", True, (255, 0, 0))
            label_pos = (pos[0] + NODE_RADIUS, pos[1])
            screen.blit(label, label_pos)
            
            cost = 0
            # Draw the cost label
            # if node is the first node:
            if node != path[0]:
                edge_data = graph.get_edge_data(path[path.index(node)-1],node)
                cost = edge_data['weight']

            cost_label = FONT.render("Current Cost: {}".format(cost), True, EDGE_COLOR)
            cost_pos = (WINDOW_WIDTH - cost_label.get_width() - NODE_RADIUS, NODE_RADIUS)
            screen.blit(cost_label, cost_pos)
            
    # Update the screen
    pygame.display.update()


# Define the main function that will run the game
def cent_main(graph, path):
    # Initialize pygame
    pygame.init()
    
    # Create the window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    # Set the positions of the nodes based on their degrees
    positions = nx.spring_layout(graph, k=1)
    for node in graph.nodes():
        pos = positions[node]
        graph.nodes[node]["pos"] = (int(pos[0]*WINDOW_WIDTH/2 + WINDOW_WIDTH/2),
                                    int(pos[1]*WINDOW_HEIGHT/2 + WINDOW_HEIGHT/2))
    
    # Set the initial state
    current_node = path[0]
    path_index = 0
    
    # Draw the initial graph
    draw_graph(screen, graph, path, current_node)
    
    # Run the game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    if path_index > 0:
                        path_index -= 1
                        current_node = path[path_index]
                elif event.key == pygame.K_RIGHT:
                    if path_index < len(path) - 1:
                        path_index += 1
                        current_node = path[path_index]
                
        
        # Update the screen
        draw_graph(screen, graph, path, current_node)
    
    # Quit pygame
    pygame.quit()

# G = nx.Graph()
# G.add_edge('1', '2', weight=5)
# G.add_edge('1', '4', weight=5)
# G.add_edge('2', '3', weight=2)
# G.add_edge('3', '4', weight=4)
# G.add_edge('4', '5', weight=2)
# G.add_edge('5', '6', weight=9)

# Define a path through the graph
# path = ['1', '4', '5']

# Run the game
# cent_main(G, path)