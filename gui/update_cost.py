total_cost = 0

def set_cost(new):
    global total_cost
    total_cost += new
    return total_cost

def get_cost():
    return total_cost