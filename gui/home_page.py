'''Functions for the home page'''

import tkinter as tk
from tkinter import Canvas
import re

# ERROR CHECKING
def print_errors(A,B,C):
    # returns error msg 
    if A == "" or B == "" or C == "":
        return "Complete all fields"
    
    else:
        num_routers = int(A)
        source_router = int(B)
        dest_router = int(C)

        if not 3 <= num_routers <= 15:
            return "Change num_routers to a value between 3 and 15"
        
        elif source_router == dest_router:
            return "source_router and dest_router must be different"

        elif source_router > num_routers or source_router < 1 or dest_router > num_routers or dest_router < 1:
            return "Change source_router and dest_router to a value between 1 and {}".format(num_routers)

        return None