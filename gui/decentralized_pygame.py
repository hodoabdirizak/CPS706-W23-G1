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

# Set the frame rate
clock = pygame.time.Clock()
fps = 60

# ====================================================================================

# Define the main function that will run the game
def decent_main(num_routers,start, end, dv_start_end, path, cost):
    
   
    # Define the dimensions of the window
    WINDOW_WIDTH = 700
    WINDOW_HEIGHT = 700

    # Define the number of rows in the table
    N = int(num_routers)

    # Initialize Pygame
    pygame.init()

    # Create the window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Set the font for the title
    title_font = pygame.font.SysFont(None, 35)
    # Set the font for the text in the table
    font = pygame.font.Font(None, 30)

    # Render the title text and create a rect object for it
    # title_text = title_font.render(f"Time: {len(dv_start_end)}", True, (255, 255, 255))
    # title_rect = title_text.get_rect(center=(WINDOW_WIDTH/2, 30))

    # Draw the title on the window surface
    # screen.blit(title_text, title_rect)

    # Define the size of each cell
    cell_width, cell_height = WINDOW_WIDTH // 4, 50
    
    
# Run the game loop
    time = 0
    running = True
    pressed = 1
    while running:
        # event = pygame.event.wait()
        for event in pygame.event.get():
            # Clear the screen
            screen.fill((0, 0, 0))
            
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and time > 0:
                    time = time - 1
                elif event.key == pygame.K_RIGHT and time >= 0 and not(time == len(dv_start_end)-1):
                    time = time + 1
                elif event.key == pygame.K_ESCAPE:
                    running = False 
                    break
                else:
                    # do nothing
                    time

        screen.fill((0, 0, 0))
                    
        text = "Time: " + str(time) #+ "\n" +
        title_text = title_font.render(text, True, (255, 255, 255))
        text2 = str(path) 
        title_text2 = title_font.render(text2, True, (255, 255, 255))
        text3 = "Cost: " + str(cost)
        title_text3 = title_font.render(text3, True, (255, 255, 255))


        title_rect = title_text.get_rect(center=(WINDOW_WIDTH/2, 25))
        title_rect2 = title_text.get_rect(center=(WINDOW_WIDTH/2, 50))
        title_rect3 = title_text.get_rect(center=(WINDOW_WIDTH/2, 75))
        # Draw the title on the window surface
        screen.blit(title_text, title_rect)
        screen.blit(title_text2, title_rect2)
        screen.blit(title_text3, title_rect3)
        # Handle events
        


        # Loop over each row in the table
        for row in range(N+1):  # Add 1 to include the header row
            # Loop over each column in the row
            for col in range(4):
                # Calculate the position of the cell based on the row and column
                x = col * cell_width
                y = (row * cell_height) + 100
                
                # Create a Rect object for the cell
                cell_rect = pygame.Rect(x, y, cell_width, cell_height)
                
                # Draw the cell with a white background and a black border
                pygame.draw.rect(screen, (255, 255, 255), cell_rect)
                pygame.draw.rect(screen, (0, 0, 0), cell_rect, 1)
                
                # Add text to the cell
                if row == 0:  # This is the header row
                    if col == 0:
                        text = f"DV in Source"
                    elif col == 2:
                        text = f"DV in Destination"
                    else:
                        text = "Distance"
                    # Render the header text in bold
                    text_surface = font.render(text, True, (0, 0, 0), (255, 255, 255))
                    # Center the header text in the cell
                    text_rect = text_surface.get_rect(center=cell_rect.center)
                    # Draw the header text to the screen
                    screen.blit(text_surface, text_rect)
                else:  # These are the data rows
                    if col == 0:
                        text = f"{start} --> {row}"
                    elif col == 1:
                        timeat = dv_start_end[time]
                        starting = timeat['dv_start']
                        text = f"{starting[f'{row}']}"
                    elif col == 2:
                        text = f"{end} --> {row}"
                    else:
                        timeat = dv_start_end[time]
                        ending = timeat['dv_end']
                        text = f"{ending[f'{row}']}"
                    # Render the data text
                    text_surface = font.render(text, True, (0, 0, 0))
                    # Center the data text in the cell
                    text_rect = text_surface.get_rect(center=cell_rect.center)
                    # Draw the data text to the screen
                    screen.blit(text_surface, text_rect)
            

        # Create a clock object
        clock = pygame.time.Clock()
        # Limit the frame rate to 60 FPS
        clock.tick(60)

        # Update the display
        pygame.display.update()


    # Wait for the user to close the window
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

  