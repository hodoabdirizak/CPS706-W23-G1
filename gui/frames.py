import tkinter as tk  
from tkinter import *
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
    def __init__(self, *args, **kwargs):  
        tk.Tk.__init__(self, *args, **kwargs)  
        container = tk.Frame(self)  
        container.pack(side="top", fill="both", expand = True)  
        container.grid_rowconfigure(0, weight=1)  
        container.grid_columnconfigure(0, weight=1)  
  
        self.frames = {}  
  
        for F in (Main_window, Page1):  
            frame = F(container, self)
            self.frames[F] = frame  
            frame.grid(row=0, column=0, sticky="nsew")  
  
        self.show_frame(Main_window)  
  
    def show_frame(self, cont):  
        frame = self.frames[cont]  
        frame.tkraise()  

# global vars
num_routers = source_router = dest_router = 0
offline_routers = []
buttonClicked = False
G = None
label_img = None

class Main_window(tk.Frame):
    def __init__(self, parent, controller):  
        tk.Frame.__init__(self,parent)  

        label = tk.Label(self, text="Enter input", font=('calibre 12 bold'))  

        # declare vars to store values input by user 
        num_routers_var = tk.StringVar()
        source_router_var = tk.StringVar()
        dest_router_var = tk.StringVar()
        offline_routers_var = tk.StringVar()

        # entry widgets
        # labels for vars
        num_routers_label = tk.Label(self, text = 'Number of Routers', font=('calibre', 10, 'bold'))
        source_router_label = tk.Label(self, text = 'Source Router', font=('calibre', 10, 'bold'))
        dest_router_label = tk.Label(self, text = 'Destination Router', font=('calibre', 10, 'bold'))
        offline_routers_label = tk.Label(self, text = 'List of Offline Routers (optional)', font=('calibre', 10, 'bold'))

        # entries for vars
        num_routers_entry = tk.Entry(self, textvariable = num_routers_var, font=('calibre',10,'normal'))
        source_router_entry = tk.Entry(self, textvariable = source_router_var, font=('calibre',10,'normal'))
        dest_router_entry = tk.Entry(self, textvariable = dest_router_var, font=('calibre',10,'normal'))
        offline_routers_entry = tk.Entry(self, textvariable = offline_routers_var, font=('calibre',10,'normal')) 
        
        def validate():
            '''validates that info provided is correct
            if invalid: print error msg to window 
            else: call edges()'''
            global num_routers, source_router, dest_router, offline_routers
            err_msg = print_errors(num_routers_var.get(),source_router_var.get(),dest_router_var.get(),offline_routers_var.get())
            canvas = tk.Canvas(self, width= 750, height= 150)
            canvas.create_text(10,10, anchor='nw', text=err_msg, fill="red", font=('calibre 10 bold'))  
            canvas.grid(row=6,column=0, columnspan = 10, sticky = tk.W+tk.E)  
            if err_msg == None:
                num_routers = int(num_routers_var.get())
                source_router = int(source_router_var.get())
                dest_router = int(dest_router_var.get())
                offline_routers_raw = offline_routers_var.get()
                if offline_routers_raw == "":
                    offline_routers = []
                else:
                    offline_routers = [int(router) for router in offline_routers_raw.split(",")]                
                return True

            return False
            
        def switch():
            if validate():
                sub_btn['state'] = tk.NORMAL
            if not validate():
                sub_btn['state'] = tk.DISABLED

        def disable():
            sub_btn['state'] = tk.DISABLED

        # placing the label and entry using grid
        label.grid(row=0,column=0)
        num_routers_label.grid(row=1,column=0)
        num_routers_entry.grid(row=1,column=1)
        source_router_label.grid(row=2,column=0)
        source_router_entry.grid(row=2,column=1)
        dest_router_label.grid(row=3,column=0)
        dest_router_entry.grid(row=3,column=1)
        offline_routers_label.grid(row=4,column=0)
        offline_routers_entry.grid(row=4,column=1)

        val_btn=tk.Button(self, text = 'Validate', command = switch)
        sub_btn=tk.Button(self, text = 'Submit', state=tk.DISABLED, command = lambda: [disable,controller.show_frame(Page1)])

        val_btn.grid(row=5,column=0)
        sub_btn.grid(row=5,column=1)

class Page1(tk.Frame):  
    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent)  
        label = tk.Label(self, text="Generate Network", font=('calibre 12 bold'))  
        label.grid(row=0,column=1)

        def create_graph():
            '''calls function from edges.py to display a graph with random edges
            assumes that user does not want to customize edges'''
            label = tk.Label(self, text="Network of {} routers, where source = {} and destination = {}".format(num_routers,source_router,dest_router), font=('calibre 12'))  
            label.grid(row=1,column=1)

            # destroy any existing graph
            plt.clf()

            global G
            G = create_random_graph(num_routers, offline_routers)


            # get image created by previous fxn call
            img = ImageTk.PhotoImage(Image.open("rand_graph.png"))
            label_img = tk.Label(self,image=img)
            label_img.image = img
            label_img.grid(row=3,column=1)

            # create a table with based on randomized nodes and weights, store in data var
            #  Node A  |   Node B   |  Cost
            #     1    |      2     |    5

            # should start at grid row=3 and column 2

            # follow this tutorial to make the table editable: 
            # see 'Python Tkinter Table Refresh': https://pythonguides.com/python-tkinter-table-tutorial/
            # after each record refresh, update data var

            # follow this tutorial to allow new input fields: 
            # see 'Python Tkinter Table Input': https://pythonguides.com/python-tkinter-table-tutorial/

            # after the user is done editing the table, they have to press 'update graph'  
            # triggers fxn call to update_graph(), need to pass in data to fxn
            custom_edges = tk.Button(self, text="Update graph", command = lambda: update_graph(data)) 
            custom_edges.grid(row=2,column=2)

        def update_graph(data):
            '''calls create_custom_graph() from create.py to create a new graph object'''
            # G = create_custom_graph(data)
            # get image created by previous fxn call
            # img = ImageTk.PhotoImage(Image.open("cust_graph.png"))
            # label_img = tk.Label(self,image=img)
            # label_img.image = img
            # label_img.grid(row=3,column=1)

        create_graph()
        random_edges = tk.Button(self, text="Create graph", command = create_graph)
        random_edges.grid(row=2,column=0)

        go_back = tk.Button(self, text="Go Back to Input", command=lambda: [controller.show_frame(Main_window)])  
        
        
        def get_path_cent():
            '''call the fxn from dijkstra.py to get the shortest path. 
            executes the pygame for centralized algorithm'''
            path = dijkstra(G, str(source_router), str(dest_router))
            
            # start pygame
            cent_main(G, path)
            pygame.quit()

        def get_path_decent():
            '''call the fxn from XYZ.py to get the shortest path. 
            executes the pygame for decentralizated algorithm'''
            dv_start_end, path, cost = decentralized(G, str(source_router), str(dest_router))
            # start pygame
            decent_main(str(num_routers), str(source_router), str(dest_router), dv_start_end, path, cost)
            pygame.quit()

        # these buttons should be hidden until the graph object has been generated
        cent = tk.Button(self, text="Run Centralized Algorithm", command=get_path_cent)  
        decent = tk.Button(self, text="Run Decentralized Algorithm", command=get_path_decent) 

        go_back.grid(row=5,column=0)
        cent.grid(row=5,column=2)
        decent.grid(row=5,column=3)
             
def data(lst):
    '''accepts a list of data'''
    return lstW 

window = Container()  
window.title('Routing Algorithm Visualization Tool')
window.geometry('1200x600')
window.mainloop()  