import tkinter as tk
from tkinter import Canvas
import re

# init the window, title, and dimensions
window = tk.Tk()
window.title('Routing Algorithm Visualization Tool')
window.geometry('800x600')

# declare vars to store values input by user 
num_routers_var = tk.StringVar()
source_router_var = tk.StringVar()
dest_router_var = tk.StringVar()
offline_routers_var = tk.StringVar()

# entry widgets

# labels for vars
num_routers_label = tk.Label(window, text = 'Number of Routers', font=('calibre', 10, 'bold'))
source_router_label = tk.Label(window, text = 'Source Router', font=('calibre', 10, 'bold'))
dest_router_label = tk.Label(window, text = 'Destination Router', font=('calibre', 10, 'bold'))
offline_routers_label = tk.Label(window, text = 'List of Offline Routers (optional)', font=('calibre', 10, 'bold'))

# entries for vars
num_routers_entry = tk.Entry(window, textvariable = num_routers_var, font=('calibre',10,'normal'))
source_router_entry = tk.Entry(window, textvariable = source_router_var, font=('calibre',10,'normal'))
dest_router_entry = tk.Entry(window, textvariable = dest_router_var, font=('calibre',10,'normal'))
offline_routers_entry = tk.Entry(window, textvariable = offline_routers_var, font=('calibre',10,'normal'))

# ERROR CHECKING - not done
def print_errors():
    # create canvas for displaying error msgs
    canvas = tk.Canvas(window, width= 750, height= 150, bg="White")

    if num_routers_var.get() == "" or source_router_var.get() == "" or dest_router_var.get() == "":
        canvas.create_text(10,10, anchor='nw', text="Complete all fields", fill="red", font=('calibre 10 bold'))
        canvas.grid(row=5,column=0, columnspan = 10, sticky = tk.W+tk.E)
        return True
    
    else:
        num_routers = int(num_routers_var.get())
        source_router = int(source_router_var.get())
        dest_router = int(dest_router_var.get())
        offline_routers_raw = offline_routers_var.get()

        if not 3 <= num_routers <= 15:
            canvas.create_text(10,10, anchor='nw', text="Change num_routers to a value between 3 and 15", fill="red", font=('calibre 10 bold'))
            canvas.grid(row=5,column=0, columnspan = 10, sticky = tk.W+tk.E)
            return True
        
        elif source_router == dest_router:
            canvas.create_text(10,10, anchor='nw', text="source_router and dest_router must be different".format(num_routers), fill="red", font=('calibre 10 bold'))
            canvas.grid(row=5,column=0, columnspan = 10, sticky = tk.W+tk.E)
            return True

        elif source_router > num_routers or source_router < 1 or dest_router > num_routers or dest_router < 1:
            canvas.create_text(10,10, anchor='nw', text="Change source_router and dest_router to a value between 1 and {}".format(num_routers), fill="red", font=('calibre 10 bold'))
            canvas.grid(row=5,column=0, columnspan = 10, sticky = tk.W+tk.E)
            return True

        elif not (re.search("^[-,0-9]+$",offline_routers_raw) or offline_routers_raw == ""):
            canvas.create_text(10,10, anchor='nw', text="offline_routers must follow format: 1,2,3", fill="red", font=('calibre 10 bold')) 
            canvas.grid(row=5,column=0, columnspan = 10, sticky = tk.W+tk.E)
            return True

        if offline_routers_raw == "":
            offline_routers = None

        elif re.search("^[-,0-9]+$",offline_routers_raw):
            offline_routers = [int(router) for router in offline_routers_raw.split(",")]

        elif source_router in offline_routers:
            canvas.create_text(10,10, anchor='nw', text="Change source router or remove source router from list", fill="red", font=('calibre 10 bold'))  
            canvas.grid(row=5,column=0, columnspan = 10, sticky = tk.W+tk.E)  
            return True

        elif dest_router in offline_routers:
            canvas.create_text(10,10, anchor='nw', text="Change dest router or remove dest router from list", fill="red", font=('calibre 10 bold'))
            canvas.grid(row=5,column=0, columnspan = 10, sticky = tk.W+tk.E)
            return True
        else:
            return False    
    

def validate():
    '''validates that info provided is correct
    if invalid: print error msg to window 
    else: call edges()'''

    if not print_errors():
        edges()       

sub_btn=tk.Button(window,text = 'Submit', command = validate)

def edges():
    '''should display an undirected graph with num_routers_var
    allow user to change cost of each edge'''
    # create canvas for displaying error msgs
    canvas = tk.Canvas(window, width= 300, height= 150, bg="White")
    canvas.create_text(10,10, anchor='nw', text="print undirected graph here", fill="red", font=('calibre 10 bold'))  
    canvas.grid(row=5,column=0, columnspan = 5, sticky = tk.W+tk.E)
    
    # allow user to input cost for each edge OR randomize costs

    # upon submitting, should run submit()
    

def submit():
    '''pass input from entry widgets into vars for use in algorithms
    create the undirected graph'''  


# placing the label and entry using grid
num_routers_label.grid(row=0,column=0)
num_routers_entry.grid(row=0,column=1)
source_router_label.grid(row=1,column=0)
source_router_entry.grid(row=1,column=1)
dest_router_label.grid(row=2,column=0)
dest_router_entry.grid(row=2,column=1)
offline_routers_label.grid(row=3,column=0)
offline_routers_entry.grid(row=3,column=1)
sub_btn.grid(row=4,column=1)

window.mainloop()