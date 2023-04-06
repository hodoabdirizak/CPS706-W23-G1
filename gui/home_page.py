'''Functions for the home page'''

import tkinter as tk
from tkinter import Canvas
import re

# ERROR CHECKING
def print_errors(A,B,C,D):
    # returns error msg 
    if A == "" or B == "" or C == "":
        return "Complete all fields"
    
    else:
        num_routers = int(A)
        source_router = int(B)
        dest_router = int(C)
        offline_routers_raw = D

        if not 3 <= num_routers <= 15:
            return "Change num_routers to a value between 3 and 15"
        
        elif source_router == dest_router:
            return "source_router and dest_router must be different"

        elif source_router > num_routers or source_router < 1 or dest_router > num_routers or dest_router < 1:
            return "Change source_router and dest_router to a value between 1 and {}".format(num_routers)

        elif not (re.search("^[-,0-9]+$",offline_routers_raw) or offline_routers_raw == ""):
            return "offline_routers must follow format: 1,2,3"

        if offline_routers_raw == "":
            offline_routers = None
            return None

        else:
            # if re.search("^[-,0-9]+$",offline_routers_raw):
            offline_routers = [int(router) for router in offline_routers_raw.split(",")]

            if source_router in offline_routers:
                return "Change source router or remove source router from list"

            if dest_router in offline_routers:
                return "Change dest router or remove dest router from list"
        
            else:
                return None