'''Functions for the home page'''

import tkinter as tk
from tkinter import Canvas
import re

# ERROR CHECKING
def print_errors(A,B,C):
    '''Returns error message if user has provided invalid input''' 

    # If any field is empty
    if A == "" or B == "" or C == "":
        return "Complete all fields"
    
    else:
        num_routers = int(A)
        source_router = int(B)
        dest_router = int(C)

        # If number of routers is less than 3 or more than 15
        if not 3 <= num_routers <= 15:
            return "Number of routers must be between 3 and 15"
        
        # If source and destination router are the same
        elif source_router == dest_router:
            return "Source and destination router must be different"

        # If the source router is invalid
        elif source_router > num_routers or source_router < 1:
            return "Source router must be between 1 and {}".format(num_routers)
        
        # If the destination router is invalid 
        elif dest_router > num_routers or dest_router < 1:
            return "Destination router must be between 1 and {}".format(num_routers)

        # Data is valid
        return None