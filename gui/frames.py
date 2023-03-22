import tkinter as tk  
from tkinter import Canvas
import re
from home_page import *
  
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

num_routers = source_router = dest_router = 0
offline_routers = []

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
            err_msg = print_errors(num_routers_var.get(),source_router_var.get(),dest_router_var.get(),offline_routers_var.get())
            print(err_msg)
            if err_msg == "":
                num_routers = int(num_routers_var.get())
                source_router = int(source_router_var.get())
                dest_router = int(dest_router_var.get())
                offline_routers_raw = offline_routers_var.get()
                offline_routers = [int(router) for router in offline_routers_raw.split(",")]
                self.show_frame(Page1)

            else:
                canvas = tk.Canvas(self, width= 750, height= 150, bg="White")
                canvas.create_text(10,10, anchor='nw', text=err_msg, fill="red", font=('calibre 10 bold'))  
                canvas.grid(row=6,column=0, columnspan = 10, sticky = tk.W+tk.E)  

        sub_btn=tk.Button(self, text = 'Submit', command = validate)

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
        sub_btn.grid(row=5,column=1)
  
class Page1(tk.Frame):  
    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent)  
        label = tk.Label(self, text="Edges", font=('calibre 12 bold'))  
        label.grid(row=5,column=1)
        # label.pack(pady=10,padx=10)  

        button1 = tk.Button(self, text="Go Back to Input", command=lambda: controller.show_frame(Main_window))  
        # button1.pack()  
        button1.grid(row=7,column=1)

        button2 = tk.Button(self, text="Submit", command=lambda: controller.show_frame(Page2))  
        # button2.pack()  
        button2.grid(row=7,column=2)
        print("num_routers = {}, sourcec_router = {}, dest_router = {}, offline_routers = {}".format(num_routers, source_router, dest_router, offline_routers))
  
class Page2(tk.Frame):  
    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent)  
        label = tk.Label(self, text="Graph animation", font=('calibre 12 bold'))  
        # label.pack(pady=10,padx=10)  
        label.grid(row=5,column=1)

        button2 = tk.Button(self, text="Go Back to Edges", command=lambda: controller.show_frame(Page1))  
        # button2.pack()  
        button2.grid(row=5,column=2)

def data(lst):
    '''accepts a list of data'''
    return lst

window = Container()  
window.title('Routing Algorithm Visualization Tool')
window.geometry('800x600')
window.mainloop()  