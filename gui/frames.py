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

        # entry widgets
        # labels for vars
        num_routers_label = tk.Label(self, text = 'Number of Routers', font=('calibre', 10, 'bold'))
        source_router_label = tk.Label(self, text = 'Source Router', font=('calibre', 10, 'bold'))
        dest_router_label = tk.Label(self, text = 'Destination Router', font=('calibre', 10, 'bold'))

        # entries for vars
        num_routers_entry = tk.Entry(self, textvariable = num_routers_var, font=('calibre',10,'normal'))
        source_router_entry = tk.Entry(self, textvariable = source_router_var, font=('calibre',10,'normal'))
        dest_router_entry = tk.Entry(self, textvariable = dest_router_var, font=('calibre',10,'normal'))
        
        def validate():
            '''validates that info provided is correct
            if invalid: print error msg to window 
            else: call edges()'''
            global num_routers, source_router, dest_router
            err_msg = print_errors(num_routers_var.get(),source_router_var.get(),dest_router_var.get())
            canvas = tk.Canvas(self, width= 750, height= 150)
            canvas.create_text(10,10, anchor='nw', text=err_msg, fill="red", font=('calibre 10 bold'))  
            # canvas.grid(row=6,column=5, columnspan = 10, sticky = tk.W+tk.E)  
            canvas.grid(row=6,column=5, columnspan = 10, sticky = tk.W+tk.E)  
            if err_msg == None:
                num_routers = int(num_routers_var.get())
                source_router = int(source_router_var.get())
                dest_router = int(dest_router_var.get())              
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
        label.grid(row=0,column=4, columnspan=6)
        num_routers_label.grid(row=1,column=4, columnspan=3)
        num_routers_entry.grid(row=1,column=5, columnspan=3)
        source_router_label.grid(row=2,column=4, columnspan=3)
        source_router_entry.grid(row=2,column=5, columnspan=3)
        dest_router_label.grid(row=3,column=4, columnspan=3)
        dest_router_entry.grid(row=3,column=5, columnspan=3)

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
            G = create_random_graph(num_routers, source_router, dest_router)

            # get image created by previous fxn call
            img = ImageTk.PhotoImage(Image.open("rand_graph.png"))
            label_img = tk.Label(self,image=img)
            label_img.image = img
            label_img.grid(row=3,column=1,rowspan=3, padx = 15)

            # create a table with based on randomized nodes and weights, store in data var
            label_table = tk.Label(self, text="", font=('calibre 12'))  
            label_table.grid(row=3,column=2, columnspan=2)

            set = ttk.Treeview(label_table)
            set.pack(side=RIGHT, padx=15, pady=20)

            set['columns'] = ('node_a', 'node_b', 'cost')
            set.column("#0", width=0, stretch=NO)
            set.column("node_a", anchor=CENTER, width=80)
            set.column("node_b", anchor=CENTER, width=80)
            set.column("cost", anchor=CENTER, width=80)

            set.heading("#0", text="", anchor=CENTER)
            set.heading("node_a", text="Node A", anchor=CENTER)
            set.heading("node_b", text="Node B", anchor=CENTER)
            set.heading("cost", text="Cost", anchor=CENTER)

            # data
            global data
            data = []

            if G:
               data = [(u, v, d['weight']) for u, v, d in G.edges(data=True)];
            
            global count
            count = 0

            for record in data:
                set.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2]))
                count += 1

            table_input = tk.Label(self, text="", font=('calibre 12'))  
            table_input.grid(row=4,column=2,columnspan=2)

            Input_frame = Frame(table_input)
            Input_frame.pack()

            node_a = Label(Input_frame, text="Node A")
            node_a.grid(row=4, column=2)

            node_b = Label(Input_frame, text="Node B")
            node_b.grid(row=4, column=3)

            cost = Label(Input_frame, text="Cost")
            cost.grid(row=4, column=4)

            node_a_entry = Entry(Input_frame)
            node_a_entry.grid(row=5, column=2)

            node_b_entry = Entry(Input_frame)
            node_b_entry.grid(row=5, column=3)

            cost_entry = Entry(Input_frame)
            cost_entry.grid(row=5, column=4)

            def input_record():
                global count

                set.insert(parent='', index='end', iid=count, text='',
                           values=(node_a_entry.get(), node_b_entry.get(), cost_entry.get()))
                count += 1
                data.extend((node_a_entry.get(), node_b_entry.get(), cost_entry.get()))
                node_a_entry.delete(0, END)
                node_b_entry.delete(0, END)
                cost_entry.delete(0, END)

            # Select Record
            def select_record():
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
                # temp_label.config(text=selected)

                # output to entry boxes
                node_a_entry.insert(0, values[0])
                node_b_entry.insert(0, values[1])
                cost_entry.insert(0, values[2])

            # save Record
            def update_record():
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

            # button
            Input_frame_buttons = Frame(table_input)
            Input_frame_buttons.pack()

            # buttons = Label(Input_frame_buttons, text="", font=('calibre 12'))  
            # buttons.grid(row=6,column=3)
            
            input_button = Button(Input_frame_buttons, text="Add Record", command=input_record)
            input_button.grid(row=5,column=2, padx = 15, pady = 20)
            
            refresh_button = Button(Input_frame_buttons, text="Update Record", command=update_record)
            refresh_button.grid(row=5,column=3, padx = 15, pady = 20)

            select_button = Button(Input_frame_buttons, text="Select Record", command=select_record)
            select_button.grid(row=5,column=4, padx = 15, pady = 20)

            custom_edges = Button(Input_frame_buttons, text="Update graph", command = lambda: update_graph(data)) 
            custom_edges.grid(row=6,column=3)

        def update_graph(data):
            '''calls create_custom_graph() from create.py to create a new graph object'''

            # destroy any existing graph
            plt.clf()

            global G
            G = create_custom_graph(data)

            # get image created by previous fxn call
            img = ImageTk.PhotoImage(Image.open("cust_graph.png"))
            label_img = tk.Label(self,image=img)
            label_img.image = img
            label_img.grid(row=3,column=1,rowspan=3, padx = 15)
            # after the user is done editing the table, they have to press 'update graph'  
            # triggers fxn call to update_graph(), need to pass in data to fxn
            custom_edges = tk.Button(self, text="Update graph", command = lambda: update_graph(data)) 
            custom_edges.grid(row=2,column=2, padx = 5, pady = 5)

        create_graph()
        random_edges = tk.Button(self, text="Create graph", command = create_graph)
        random_edges.grid(row=1,column=0, padx = 5, pady = 5)

        go_back = tk.Button(self, text="Go Back to Input", command=lambda: [controller.show_frame(Main_window)])  
        go_back.grid(row=2,column=0)

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

        
        # (row=2,column=2)
        cent.grid(row=2,column=2)
        decent.grid(row=2,column=3)
             
def data(lst):
    '''accepts a list of data'''
    return lst

window = Container()  
window.title('Routing Algorithm Visualization Tool')
window.geometry('1200x600')
window.mainloop()  
