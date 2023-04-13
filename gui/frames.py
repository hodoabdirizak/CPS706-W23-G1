import tkinter as tk  
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import re
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from home_page import *
from create_graph import *

import sys
sys.path.append('./centralized')
sys.path.append('./decentralized')

from dijkstra import *
from bellman_ford import *

from centralized_pygame import *
from decentralized_pygame import *


class Container(tk.Tk): 
    '''Class that contains all of the frames in the Tkinter Window''' 
    def __init__(self, *args, **kwargs):  
        '''Initialization method for the Container class'''
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)  
        container.pack(side="top", fill="both", expand = True)  
        container.grid_rowconfigure(0, weight=1)  
        container.grid_columnconfigure(0, weight=1)  
  
        self.frames = {}  
  
        # Place each frame in the Container
        for F in (Main_window, Page1):  
            frame = F(container, self)
            self.frames[F] = frame  
            frame.grid(row=0, column=0, sticky="nsew")  
  
        self.show_frame(Main_window)  
  
    # Displays a frame 
    def show_frame(self, cont):  
        frame = self.frames[cont]  
        frame.tkraise()  

# Define global variables to be accessed by multiple frames
num_routers = source_router = dest_router = 0
buttonClicked = False
G = None
label_img = None
tkfont = ('DM Sans', 11, 'bold')
tkfont_bold = ('DM Sans', 14, 'bold')
col_dark = '#293241'
col_white = '#e0fbfc'
col_accent = '#98c1d9'
col_grey = '#3d5a80'

class Main_window(tk.Frame):
    '''Class for the Main Window frame, the frame first seen by the user'''
    def __init__(self, parent, controller):  
        tk.Frame.__init__(self,parent)  
        self.config(background=col_dark)

        # Create text for the title and instructions for the Main Window 
        label = tk.Label(self, bd=1, text="Routing Algorithm Visualization Tool", anchor='nw', fg=col_accent, bg=col_dark, font=tkfont_bold)  
        label2 = tk.Label(self, bd=1, text="Before we start, we'll need the following information:", anchor='nw', fg='white', bg=col_dark, font=('DM Sans', 12, 'bold'))  

        # Declare variables to store values input by the user 
        num_routers_var = tk.StringVar()
        source_router_var = tk.StringVar()
        dest_router_var = tk.StringVar()

        # entry widgets
        # Create labels for the text boxes
        empt_string = tk.Label(self, bd=1, text = '', fg=col_white, bg=col_dark, font=tkfont)
        num_routers_label = tk.Label(self, bd=1, text = 'Number of Routers', fg=col_white, bg=col_dark, font=tkfont)
        source_router_label = tk.Label(self, bd=1, text = 'Source Router', fg=col_white, bg=col_dark, font=tkfont)
        dest_router_label = tk.Label(self, bd=1, text = 'Destination Router', fg=col_white, bg=col_dark, font=tkfont)

        # Create entries for each label
        num_routers_entry = tk.Entry(self, bd=1, textvariable = num_routers_var, fg=col_dark, font=('DM Sans', 11, 'bold'))
        source_router_entry = tk.Entry(self, bd=1, textvariable = source_router_var, fg=col_dark, font=('DM Sans', 11, 'bold'))
        dest_router_entry = tk.Entry(self, bd=1, textvariable = dest_router_var, fg=col_dark, font=('DM Sans', 11, 'bold'))
        
        # Create empty text to situate the display grid
        empty_1 = tk.Label(self, bd=1, text="                                                                   ", bg=col_dark) 
        empty_2 = tk.Label(self, bd=1, text="                                                                   ", bg=col_dark) 
        empty_3 = tk.Label(self, bd=1, text="                                                                   ", bg=col_dark) 
        empty_4 = tk.Label(self, bd=1, text="                                                                   ", bg=col_dark) 
        label_end = tk.Label(self, bd=1, text="Hit ESC key to exit program", fg='white', bg=col_dark, font=tkfont_bold) 

        # Create Validate and Submit buttons
        val_btn=tk.Button(self, text = 'Validate', fg=col_dark, bg=col_accent, font=tkfont, command = switch)
        sub_btn=tk.Button(self, text = 'Submit', fg=col_dark, bg=col_accent, font=tkfont, state=tk.DISABLED, command = lambda: [disable,controller.show_frame(Page1)])

        def validate():
            '''Validates that info provided is correct
            if invalid: print error msg to window 
            else: call edges()'''
            global num_routers, source_router, dest_router

            # Update error message
            err_msg = print_errors(num_routers_var.get(),source_router_var.get(),dest_router_var.get())

            # Create the canvas element that displays the error message
            canvas = tk.Canvas(self, width= 750, height= 30, bg=col_dark, highlightthickness=0)
            canvas.create_text(5,5, anchor='nw', text=err_msg, fill="#ee6c4d", font=tkfont)  
            canvas.grid(row=4,column=6) 

            # If there is no error, update the number of routers, source and destination router
            if err_msg == None:
                num_routers = int(num_routers_var.get())
                source_router = int(source_router_var.get())
                dest_router = int(dest_router_var.get())              
                return True

            # There is an error with the input data
            return False
            
        def switch():
            '''Makes the Submit button visible if the data is validated'''
            if validate():
                sub_btn['state'] = tk.NORMAL
            if not validate():
                sub_btn['state'] = tk.DISABLED

        def disable():
            '''Disables the Submit button if the data has not yet been validated'''
            sub_btn['state'] = tk.DISABLED

        # Display each previously created label and entry using grid
        label.grid(row=0,column=2, padx=10, pady=30, columnspan=2)
        label2.grid(row=1,column=2, padx=10, pady=40, columnspan=2)
   
        num_routers_label.grid(row=2,column=2, padx=10, pady=10)
        num_routers_entry.grid(row=2,column=3, padx=10, pady=10)
        source_router_label.grid(row=3,column=2, padx=10, pady=10)
        source_router_entry.grid(row=3,column=3, padx=10, pady=10)
        dest_router_label.grid(row=4,column=2, padx=10, pady=10)
        dest_router_entry.grid(row=4,column=3, padx=10, pady=10)

        val_btn.grid(row=5,column=2,padx=10, pady=10)
        sub_btn.grid(row=5,column=3,padx=10, pady=10)
        empt_string.grid(row=6,column=1, padx=10, pady=10)

        empty_1.grid(row=7,column=0, padx=10, pady=10)
        empty_2.grid(row=7,column=1, padx=10, pady=10)
        empty_3.grid(row=7,column=2, padx=10, pady=10)
        empty_4.grid(row=7,column=3, padx=10, pady=10)

        label_end.grid(row=8,column=2, padx=10, pady=250, columnspan=2)
         
class Page1(tk.Frame):  
    '''Class for the Page1 frame, the page that comes after Main Window'''
    def __init__(self, parent, controller):  
        '''Initialize the class'''
        tk.Frame.__init__(self, parent)  
        self.config(background=col_dark)
        label = tk.Label(self, text="Generate Network", pady = 10, fg=col_white, bg=col_dark, font=tkfont_bold)  
        label.grid(row=0,column=1)

        def create_graph():
            '''Calls function from edges.py to create a randomized networkx graph and display the graph on Page1'''

            # Create text to display the number of routers, the source and destination nodes
            label = tk.Label(self, text="Network of {} routers, where source = {} and destination = {}".format(num_routers,source_router,dest_router), fg=col_white, bg=col_dark, font=('DM Sans', 13, 'bold'))  
            label.grid(row=1,column=1)

            # Destroy any existing graph shown in Page 1 
            plt.clf()

            # Set the G variable equal to the result of the create_rand_graph function from create_graph.py
            global G
            G = create_random_graph(num_routers, source_router, dest_router)

            # Get image created by previous fxn call
            img = ImageTk.PhotoImage(Image.open("gui/graph.png"))
            label_img = tk.Label(self,image=img)
            label_img.image = img
            label_img.grid(row=3,column=1,rowspan=3, padx = 25)

            # Create a table with based on randomized nodes and weights, store in data var
            label_table = tk.Label(self, text="", font=tkfont, bg=col_dark, highlightbackground=col_dark, highlightthickness=0, borderwidth=0)  
            label_table.grid(row=3,column=2, columnspan=2)
            
            # Uses Treeview to make a table to display current graph info (Node A, Node B, Cost)
            set = ttk.Treeview(label_table)
            set.pack(side=RIGHT, padx=15, pady=20)

            # Set columns of table 
            set['columns'] = ('node_a', 'node_b', 'cost')
            set.column("#0", width=0, stretch=NO)
            set.column("node_a", anchor=CENTER, width=80)
            set.column("node_b", anchor=CENTER, width=80)
            set.column("cost", anchor=CENTER, width=80)

            # Set heading of table 
            set.heading("#0", text="", anchor=CENTER)
            set.heading("node_a", text="Node A", anchor=CENTER)
            set.heading("node_b", text="Node B", anchor=CENTER)
            set.heading("cost", text="Cost", anchor=CENTER)

            # Initalize data array to hold the source nodes, destination nodes, and weights of graph G
            global data
            data = []

            # If graph G is not empty, user has selected to create randomized graph
            if G:
                # Populate data array with node info of graph G
                for u, v, d in G.edges(data=True):
                    data.append(u)
                    data.append(v)
                    data.append(d['weight'])

            global count
            count = 0
            
            # records array to use when to populate table
            records = []
            for i in range(0, len(data), 3):
                # populate records array with info from data array
                records.append((data[i], data[i+1], data[i+2]))
                
            # user graph customization

            # create input textboxes for nodes user wants to enter
            for record in records:
                set.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2]))
                count += 1

            table_input = tk.Label(self, text="", font=tkfont, bg=col_dark, highlightbackground=col_dark, highlightthickness=0, borderwidth=0)  
            table_input.grid(row=4,column=2,columnspan=2)

            Input_frame = Frame(table_input, bg=col_dark, highlightbackground=col_dark, highlightthickness=0, borderwidth=0)
            Input_frame.pack()

            # set label of input textboxes
            node_a = Label(Input_frame, text="Node A", bg=col_dark, fg=col_white)
            node_a.grid(row=4, column=2)

            node_b = Label(Input_frame, text="Node B", bg=col_dark, fg=col_white)
            node_b.grid(row=4, column=3)

            cost = Label(Input_frame, text="Cost", bg=col_dark, fg=col_white)
            cost.grid(row=4, column=4)
            
            # create input textboxes
            node_a_entry = Entry(Input_frame)
            node_a_entry.grid(row=5, column=2)

            node_b_entry = Entry(Input_frame)
            node_b_entry.grid(row=5, column=3)

            cost_entry = Entry(Input_frame)
            cost_entry.grid(row=5, column=4)

            def input_record():
                '''Is called when user wants to add a row to the customization table, modifying current graph later'''
                global count

                # place user entries in table
                set.insert(parent='', index='end', iid=count, text='', values=(node_a_entry.get(), node_b_entry.get(), cost_entry.get()))
                count += 1
                
                # add user entries to data array to modify graph later
                data.extend((node_a_entry.get(), node_b_entry.get(), cost_entry.get()))
                
                # clear user entry textboxes
                node_a_entry.delete(0, END)
                node_b_entry.delete(0, END)
                cost_entry.delete(0, END)

            # Select Record
            def select_record():
                '''Is called when user wants to edit the existing row of table, displaying highlighted row data 
                in entry boxes for editing'''

                # clear entry boxes
                node_a_entry.delete(0, END)
                node_b_entry.delete(0, END)
                cost_entry.delete(0, END)

                # grab record
                selected = set.focus()
                values = set.item(selected, 'values')
                global to_delete
                to_delete = [values[0], values[1], values[2]]
                # grab record values
                values = set.item(selected, 'values')

                # output to entry boxes
                node_a_entry.insert(0, values[0])
                node_b_entry.insert(0, values[1])
                cost_entry.insert(0, values[2])

            # save Record
            def update_record():
                '''Is called when user wants to refresh table to include edited existing row of table'''
                # need to insert new data and remove indexes that have been overwritten
                selected = set.focus()

                # delete old data
                for i in range(len(data) - len(to_delete) + 1):
                    if data[i:i + len(to_delete)] == to_delete:
                        del data[i:i + len(to_delete)]

                # save new data
                set.item(selected, text="",
                             values=(node_a_entry.get(), node_b_entry.get(), cost_entry.get()))
                data.extend((node_a_entry.get(), node_b_entry.get(), cost_entry.get()))
                # clear entry boxes
                node_a_entry.delete(0, END)
                node_b_entry.delete(0, END)
                cost_entry.delete(0, END)

            # frame for button trio
            Input_frame_buttons = Frame(table_input, bg=col_dark, highlightbackground=col_dark, highlightthickness=0, borderwidth=0)
            Input_frame_buttons.pack()
            
            # select button - calls select_record function
            select_button = Button(Input_frame_buttons, text="Select Record", fg=col_white, bg=col_grey, font=tkfont, command=select_record)
            select_button.grid(row=5,column=2, padx = 15, pady = 20)
            
            # update button - calls update_record function
            refresh_button = Button(Input_frame_buttons, text="Update Record", fg=col_white, bg=col_grey, font=tkfont, command=update_record)
            refresh_button.grid(row=5,column=3, padx = 15, pady = 20)

            # input button - calls input_record function
            input_button = Button(Input_frame_buttons, text="Add Record", fg=col_white, bg=col_grey, font=tkfont, command=input_record)
            input_button.grid(row=5,column=4, padx = 15, pady = 20)

            # calls update_graph() function, with list of current graph info to create graph image
            custom_edges = Button(Input_frame_buttons, text="Update graph", fg=col_dark, bg=col_accent, font=tkfont, command = lambda: update_graph(data)) 
            custom_edges.grid(row=6,column=3)

        def update_graph(data):
            '''Calls function from edges.py to create a custom networkx graph and display the graph on Page1'''

            # destroy any existing graph
            plt.clf()

            global G
            G = create_custom_graph(data)

            # get image created by previous fxn call
            img = ImageTk.PhotoImage(Image.open("gui/graph.png"))
            label_img = tk.Label(self,image=img)
            label_img.image = img
            label_img.grid(row=3,column=1,rowspan=3, padx = 25)

        # Initially displays no graph
        create_graph()

        # Upon clicking create graph button, triggers the create_graph function
        random_edges = tk.Button(self, text="Create graph", fg=col_white, bg=col_grey, font=tkfont, command = create_graph)
        random_edges.grid(row=1,column=0, padx = 5, pady = 10)

        # Upon clicking the Go Back to Input button, returns to the first page 
        go_back = tk.Button(self, text="Go Back to Input", fg=col_white, bg=col_grey, font=tkfont, command=lambda: [controller.show_frame(Main_window)])  
        go_back.grid(row=2,column=0, padx = 5, pady = 10)

        def get_path_cent():
            '''Calls functions from dijkstra.py to get the shortest path, 
            the list of parents nodes, and the list of distance vectors,  
            executes the pygame for the centralized algorithm'''
            # Create the shortest path from dijsktra.py 
            path = dijkstra(G, str(source_router), str(dest_router))
        
            # get table columns from the dijkstra's algorithm
            dist_vecs = get_dist_vecs()
            prev_node = get_prev_node()
            
            # start the pygame for the centralized algorithm
            cent_main(G, path, dist_vecs, prev_node)

            # quit the pygame
            pygame.quit()

        def get_path_decent():
            '''call the fxn from bellman_ford.py to get the shortest path. 
            executes the pygame for decentralizated algorithm'''
            # Creates the shortest path and gathers vector info from bellman_ford.py 
            dv_start_end, path, cost = decentralized(G, str(source_router), str(dest_router))

            # start the pygame for the decentralized algorithm
            decent_main(str(num_routers), str(source_router), str(dest_router), dv_start_end, path, cost, G)

            # quit the pygame
            pygame.quit()

        # Create buttons for the centralized and decentralized algorithms  
        cent = tk.Button(self, text="Run Centralized Algorithm", fg=col_dark, bg=col_accent, font=tkfont, command=get_path_cent)  
        decent = tk.Button(self, text="Run Decentralized Algorithm", fg=col_dark, bg=col_accent, font=tkfont, command=get_path_decent) 

        # Display the buttons on the grid
        cent.grid(row=2,column=2)
        decent.grid(row=2,column=3)

        # Display text for quitting the game
        label_end = tk.Label(self, bd=1, text="Hit ESC key to exit program", fg='white', bg=col_dark, font=tkfont_bold) 
        empty_1 = tk.Label(self, bd=1, text="                                                                   ", bg=col_dark) 
        empty_1.grid(row=8,column=1)
        label_end.grid(row=9,column=1)

             
def close(event):
    '''closes the program'''
    window.withdraw()
    sys.exit()

# Initialize the class
window = Container()  

# Create the title and set window size
window.title('Routing Algorithm Visualization Tool')
window.geometry('1200x600')

# Set background to dark colour
window.configure(background=col_dark)

# Make window full screen
window.attributes('-fullscreen', True)

# When ESC is pressed, close the program
window.bind('<Escape>', close)

# Run the program
window.mainloop()  
