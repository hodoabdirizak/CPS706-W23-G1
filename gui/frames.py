import tkinter as tk  
from tkinter import *
from PIL import Image, ImageTk
import re
from home_page import *
from create_graph import *
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os

class Container(tk.Tk):  
    def __init__(self, *args, **kwargs):  
        tk.Tk.__init__(self, *args, **kwargs)  
        container = tk.Frame(self)  
        container.pack(side="top", fill="both", expand = True)  
        container.grid_rowconfigure(0, weight=1)  
        container.grid_columnconfigure(0, weight=1)  
  
        self.frames = {}  
  
        for F in (Main_window, Page1, Page2):  
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

def destroy_img():
    global label_img
    if label_img: 
        label_img.master.destroy()
        label_img.destroy()

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
            print("err msg:",err_msg)
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
        label.grid(row=1,column=1)

        button1 = tk.Button(self, text="Go Back to Input", command=lambda: controller.show_frame(Main_window))  
        button2 = tk.Button(self, text="Submit", command=lambda: controller.show_frame(Page2))  

        button1.grid(row=2,column=1)
        button2.grid(row=2,column=2)

        def randomize():
            '''calls function from edges.py to display a static graph with random edges
            assumes that user does not want to customize edges'''
            global label_img
            destroy_img()
            G = display_static_graph(num_routers, source_router, dest_router, offline_routers)

            # get image created by previous fxn call
            img = ImageTk.PhotoImage(Image.open("rand_graph.png"))
            label_img = tk.Label(image=img)
            label_img.image = img
            label_img.pack()

        def collect_input():
            '''should allow user to customize edges'''

        random_edges = tk.Button(self, text="Randomize Edges", command = randomize)
        custom_edges = tk.Button(self, text="Customize Edges", command = collect_input) 
        random_edges.grid(row=3,column=1)
        custom_edges.grid(row=3,column=2)
      
  
class Page2(tk.Frame):  
    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent)  

        label = tk.Label(self, text="Graph animation", font=('calibre 12 bold'))  
 
        label.grid(row=1,column=1)

        button1 = tk.Button(self, text="Go Back to Edges", command=lambda: controller.show_frame(Page1))  
        cent = tk.Button(self, text="Centralized Algorithm")  
        decent = tk.Button(self, text="Decentralized Algorithm") 

        button1.grid(row=2,column=1)
        cent.grid(row=3,column=1)
        decent.grid(row=3,column=2)
        
def data(lst):
    '''accepts a list of data'''
    return lst

window = Container()  
window.title('Routing Algorithm Visualization Tool')
window.geometry('800x600')
window.mainloop()  