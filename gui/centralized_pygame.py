import networkx as nx
import os
import pygame

os.environ['SDL_VIDEO_CENTERED'] = '1'

# Define constants for the window size and node radius
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 550
NODE_RADIUS = 15

# Define colors for the nodes and edges
NODE_COLOR = (255, 255, 255)
EDGE_COLOR = (255, 255, 255)

FONT = None

def get_path_costs(graph,path):
    path_costs = [0]
    next_cost = 0
    for node in path[:-1]:
        edge_data = graph.get_edge_data(path[path.index(node)],path[path.index(node)+1])
        next_cost += edge_data.get('weight')
        path_costs.append(next_cost)
    return path_costs


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

    # Get the costs in the path to update the count
    costs = get_path_costs(graph,path)

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
        label = FONT.render(str(node), True, (0,0,0))
        label_pos = (pos[0] - NODE_RADIUS/2, pos[1] - NODE_RADIUS/2)
        screen.blit(label, label_pos)
        
        # Write source and dest nodes in top right corner
        source_label = FONT.render("Source: {}".format(int(path[0])), True, EDGE_COLOR)
        dest_label = FONT.render("Destination: {}".format(int(path[-1])), True, EDGE_COLOR)
        source_pos = (WINDOW_WIDTH - source_label.get_width() + NODE_RADIUS, NODE_RADIUS)
        dest_pos = (WINDOW_WIDTH - dest_label.get_width()+ NODE_RADIUS, NODE_RADIUS*3)
        screen.blit(source_label, source_pos)
        screen.blit(dest_label, dest_pos)

        # Write exit instructions in top left
        exit_label = FONT.render("Hit ESC to exit or change graph".format(int(path[0])), False, EDGE_COLOR)
        exit_pos = (NODE_RADIUS, NODE_RADIUS)
        screen.blit(exit_label, exit_pos)
        
        # Draw the current node label
        if node == current_node:
            label = FONT.render(" Current Node", True, (255, 0, 0))
            label_pos = (pos[0] + NODE_RADIUS, pos[1])
            screen.blit(label, label_pos)
            
            # Draw the cost label
            i = path.index(node) 
            cost = costs[i]
            cost_label = FONT.render("Current Cost: {}".format(cost), True, (255, 0, 0))
            cost_pos = (WINDOW_WIDTH - cost_label.get_width() + NODE_RADIUS, NODE_RADIUS*5)
            screen.blit(cost_label, cost_pos)
            
    # Update the screen
    pygame.display.update()

def draw_game_over_screen(screen, path):
    # Add text
    title = FONT.render('Animation complete: The shortest path is {}'.format(" -> ".join(path)), True, (0, 255, 255))

    screen.blit(title, (NODE_RADIUS, WINDOW_HEIGHT + NODE_RADIUS*3))
    pygame.display.update()

def start_page(screen):
    # Clear the screen
    screen.fill((0, 0, 0))



# Define the main function that will run the game
def cent_main(graph, path):
    pygame.init()

    # Define the font for the node labels
    global FONT
    FONT = pygame.font.Font(None, 30)

    # Create the window
    screen = pygame.display.set_mode((WINDOW_WIDTH+50, WINDOW_HEIGHT+100))

    # Set the positions of the nodes based on their degrees
    positions = nx.circular_layout(graph)
    for node in graph.nodes():
        pos = positions[node]
        graph.nodes[node]["pos"] = (int(pos[0]*WINDOW_WIDTH//2.5 + WINDOW_WIDTH//2.5+50),
                                    int(pos[1]*WINDOW_HEIGHT//2.5 + WINDOW_HEIGHT//2.5+100))
    
    # Set the initial state
    current_node = path[0]
    path_index = 0
    
    # Display start page
    

    # Draw the initial graph
    draw_graph(screen, graph, path, current_node)
    
    # Run the game loop
    running = True
    animation_done = False
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if path_index > 0:
                        path_index -= 1
                        current_node = path[path_index]
                
                elif event.key == pygame.K_RIGHT:
                    # if this is the last node in the path:
                    if path_index == len(path) - 1:
                        animation_done = True

                    elif path_index < len(path) - 1:
                        path_index += 1
                        current_node = path[path_index]

                elif event.key == pygame.K_ESCAPE:
                    running = False 
                    break

        if animation_done:
            draw_game_over_screen(screen, path)

        if not running:
            break            
        
        # Update the screen
        if not animation_done:
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
# G.add_edge('4', '6', weight=2)
# G.add_edge('5', '7', weight=4)
# G.add_edge('4', '7', weight=6)
# G.add_edge('3', '6', weight=7)


# # # Define a path through the graph
# path = ['1', '4', '5','7']

# # # Run the game
# cent_main(G, path)