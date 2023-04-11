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
            return "Number of routers must be between 3 and 15"
        
        elif source_router == dest_router:
            return "Source and destination router must be different"

        elif source_router > num_routers or source_router < 1:
            return "Source router must be between 1 and {}".format(num_routers)
        
        elif dest_router > num_routers or dest_router < 1:
            return "Destination router must be between 1 and {}".format(num_routers)

        return None