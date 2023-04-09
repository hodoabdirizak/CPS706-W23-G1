import networkx as nx
import os
import pygame
pygame.init()
from explanations import *


os.environ['SDL_VIDEO_CENTERED'] = '1'

# Define constants for the window size and node radius
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 550
NODE_RADIUS = 15

# Define colors for the nodes and edges
NODE_COLOR = (255, 255, 255)
EDGE_COLOR = (255, 255, 255)

FONT = None

# Set the frame rate
clock = pygame.time.Clock()
fps = 60

def get_path_costs(graph,path):
    path_costs = [0]
    next_cost = 0
    for node in path[:-1]:
        edge_data = graph.get_edge_data(path[path.index(node)],path[path.index(node)+1])
        next_cost += int(edge_data.get('weight'))
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


# Define the main function that will run the game
def cent_main(graph, path, dist_vecs):
    pygame.init()

    # Define the font for the node labels
    global FONT
    FONT = pygame.font.Font(None, 30)

    # Create the window
    screen = pygame.display.set_mode((WINDOW_WIDTH+50, WINDOW_HEIGHT+100))
  
    # Display start page
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont('DM Sans', 30)
    text_font = pygame.font.SysFont('DM Sans', 25)

    title = font.render("Explanation of Dijikstra's Algorithm", True, (255, 255, 255))
    start = text_font.render("Press any key to continue to the animation", True, (0, 255, 255))

    screen.blit(title, (WINDOW_WIDTH/2 - title.get_width()/2, WINDOW_HEIGHT/2 - title.get_height()/2))
    screen.blit(start, (WINDOW_WIDTH/2 - start.get_width()/2, WINDOW_HEIGHT/2 + start.get_height()/2))
    pygame.display.update()

    running = True
    start_dijkstras = False
    start_animation = False

    # Start screen: Check if key is pressed 
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            
            # stop if any key is pressed
            elif event.type == pygame.KEYDOWN:
                start_dijkstras = True
                running = False

    if start_dijkstras:
        screen.fill((0, 0, 0))

        # Define the size of each cell
        cell_width, cell_height = WINDOW_WIDTH // 4.8 - 20, 25

        # Run the game loop
        time = 0
        running = True
        pressed2 = False
       
        while running:      
            for event in pygame.event.get():
                # Clear the screen
                screen.fill((0, 0, 0))
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and time > 0:
                        time = time - 1
                    elif event.key == pygame.K_RIGHT and time >= 0 and time < len(dist_vecs)-1:
                        time = time + 1
                    
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                        break
                    else:
                        pressed2 = True
                        running = False
                        break
                        
            screen.fill((0, 0, 0))

            # Display the graph
            imp = pygame.image.load("gui/graph.png").convert()
            IMAGE_SMALL = pygame.transform.rotozoom(imp, 0, 0.6)
            screen.blit(IMAGE_SMALL, (10, 50))

            text = "Step: " + str(time+1)  # + "\n" +
            title_text = font.render(text, True, (255, 255, 255))

            title_rect = title_text.get_rect(center=(WINDOW_WIDTH / 2 + 400, 25))
            
            # Draw the title on the window surface
            screen.blit(title_text, title_rect)
            
            table_font = pygame.font.SysFont('DM Sans', 23)

            # Handle events
            # Loop over each row in the table
            for row in range(graph.number_of_nodes() + 1):  # Add 1 to include the header row
                # Loop over each column in the row
                for col in range(3):
                    # Calculate the position of the cell based on the row and column                   
                    x = col * cell_width + 400
                    y = (row * cell_height) + 100  

                    # Create a Rect object for the cell
                    cell_rect = pygame.Rect(x, y, cell_width, cell_height)

                    # Draw the cell with a white background and a black border
                    pygame.draw.rect(screen, (255, 255, 255), cell_rect)
                    pygame.draw.rect(screen, (0, 0, 0), cell_rect, 1)

                    # Add text to the cell
                    if row == 0:  # This is the header row
                        if col == 0:
                            text = f"Node"
                        elif col == 1:
                            text = f"Distance from {path[0]}"
                        else:
                            text = f"Previous node"
                        # Render the header text in bold
                        text_surface = table_font.render(text, True, (0, 0, 0), (255, 255, 255))
                        text_rect = text_surface.get_rect(center=cell_rect.center)
                        screen.blit(text_surface, text_rect)

                    else:  # These are the data rows
                        if col == 0:
                            text = f"{row}"
                        elif col == 1 and time < len(dist_vecs):
                            timeat = dist_vecs[time]
                            starting = timeat[row-1]
                            text = str(starting)
                        else:
                            text = None
                        text_surface = table_font.render(text, True, (0, 0, 0))
                        text_rect = text_surface.get_rect(center=cell_rect.center)
                        screen.blit(text_surface, text_rect)

            # Create a clock object
            clock = pygame.time.Clock()
            # Limit the frame rate to 60 FPS
            clock.tick(60)

            # Update the display
            pygame.display.update()


    # If table is complete, start the animation
    if pressed2:
        title = FONT.render('Using the resulting table, backtrack from the destination to the start node.', True, (255, 255, 255))
        title2 = FONT.render('The shortest path is {}'.format(" -> ".join(path)), True, (255, 255, 255))
        title3 = FONT.render('Press any key to continue', True, (0, 255, 255))
        screen.blit(title, (NODE_RADIUS, WINDOW_HEIGHT - NODE_RADIUS*4))
        screen.blit(title2, (NODE_RADIUS, WINDOW_HEIGHT - NODE_RADIUS*3 + 25))
        screen.blit(title3, (NODE_RADIUS, WINDOW_HEIGHT - NODE_RADIUS*2 + 50))
        pygame.display.update()

        running = True
        # Table screen: Check if key is pressed 
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                
                # stop if any key is pressed
                elif event.type == pygame.KEYDOWN:
                    start_animation = True
                    running = False

    if start_animation:
        # Set the positions of the nodes based on their degrees
        positions = nx.circular_layout(graph)
        for node in graph.nodes():
            pos = positions[node]
            graph.nodes[node]["pos"] = (int(pos[0]*WINDOW_WIDTH//2.5 + WINDOW_WIDTH//2.5+50),
                                        int(pos[1]*WINDOW_HEIGHT//2.5 + WINDOW_HEIGHT//2.5+100))
        
        # Set the initial state
        current_node = path[0]
        path_index = 0

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


# Define a path through the graph
# path = ['1', '4', '5']

# dist= [[0, 'inf', 'inf', 'inf', 'inf', 'inf'], 
#             [0, 5, 5, 'inf', 'inf', 'inf'], 
#             [0, 5, 5, 7, 'inf', 'inf'], 
#             [0, 5, 5, 7, 7, 'inf'], 
#             [0, 5, 5, 7, 7, 'inf'], 
#             [0, 5, 5, 7, 7, 16]]

# # Run the game
# cent_main(G, path, dist)

