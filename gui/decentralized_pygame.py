import networkx as nx
import os
import pygame
from update_cost import * 
pygame.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'

# Define constants for the window size and node radius
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
NODE_RADIUS = 15

# Get info about window size
info = pygame.display.Info() 
screen_width,screen_height = info.current_w,info.current_h

# Define colors for the nodes and edges
NODE_COLOR = (255, 255, 255)
EDGE_COLOR = (255, 255, 255)

# Define the font for the node labels
FONT = pygame.font.Font(None, 30)
    
# Define the main function that will run the game
def decent_main(graph, start, end):
    # Create the window
    screen = pygame.display.set_mode((WINDOW_WIDTH+50, WINDOW_HEIGHT+100))
    # Set the positions of the nodes based on their degrees
    positions = nx.circular_layout(graph)
    for node in graph.nodes():
        pos = positions[node]
        graph.nodes[node]["pos"] = (int(pos[0]*WINDOW_WIDTH//2.5 + WINDOW_WIDTH//2.5+50),
                                    int(pos[1]*WINDOW_HEIGHT//2.5 + WINDOW_HEIGHT//2.5+100))
    
    
    # Set the size of each cell
    cell_width, cell_height = 50, 50

    # Draw the table
    for row in range(end):
        for col in range(num_cols):
            rect = pygame.Rect(col * cell_width, row * cell_height, cell_width, cell_height)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)

    # Run the game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if path_index > 0:
                        path_index -= 1
                        current_node = path[path_index]
                
                elif event.key == pygame.K_RIGHT:
                    if path_index < len(path) - 1:
                        path_index += 1
                        current_node = path[path_index]

                elif event.key == pygame.K_ESCAPE:
                    running = False 
                    break
        if not running:
            break            
        
        # Update the screen
        draw_graph(screen, graph, path, current_node)
    
    # Quit pygame
    pygame.display.quit()
    pygame.quit()

# G = nx.Graph()
# G.add_edge('1', '2', weight=5)
# G.add_edge('1', '4', weight=5)
# G.add_edge('2', '3', weight=2)
# G.add_edge('3', '4', weight=4)
# G.add_edge('4', '5', weight=2)
# G.add_edge('5', '6', weight=9)
# G.add_edge('4', '6', weight=2)
# G.add_edge('5', '7', weight=4)
# G.add_edge('4', '7', weight=6)
# G.add_edge('3', '6', weight=7)


# # # Define a path through the graph
# path = ['1', '4', '5','7']

# # # Run the game
# cent_main(G, path)