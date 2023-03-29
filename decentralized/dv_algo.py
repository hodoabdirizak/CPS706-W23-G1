dist_vecs = [
    [float('inf'), 5, float('inf'), float('inf'), float('inf')],
    [5, float('inf'), float('inf'), 7, 2],
    [float('inf'), float('inf'), float('inf'), 1, float('inf')],
    [float('inf'), 7, 1, float('inf'), 12],
    [float('inf'), 2, float('inf'), 12, float('inf')],
]


# get num networks
num_networks = len(dist_vecs)

# set self to 0
for i in range(num_networks):
    dist_vecs[i][i] = 0

# neighbors mat
network_neighbors = [[] for i in range(num_networks)]
for curr_network, vec in enumerate(dist_vecs):
    for neighbor, weight in enumerate(vec):
        if weight != float('inf') and curr_network != neighbor:
            network_neighbors[curr_network].append((neighbor, weight))


for i, x in enumerate(network_neighbors):
    print(i)
    print(x)
print("\n\n")

# initalize needs update array
notify_neighbors = [True] * num_networks

# Loop
t = 0

print(f't = {t}')
for x in dist_vecs:
    print(x)
print("\n\n")

while any(notify_neighbors):
    t += 1

    dist_vecs_next = []
    notify_neighbors_next = [False] * num_networks

    for curr_network in range(num_networks):
        curr_network_dv = dist_vecs[curr_network][:]

        for neighbor, weight in network_neighbors[curr_network]:

            for i, distance in enumerate(dist_vecs[neighbor]):
                temp_distance = weight + distance

                if temp_distance < curr_network_dv[i]:
                    curr_network_dv[i] = temp_distance
                    notify_neighbors_next[curr_network] = True

        dist_vecs_next.append(curr_network_dv)

    dist_vecs = dist_vecs_next
    notify_neighbors = notify_neighbors_next

    print(f't = {t}')
    for x in dist_vecs:
        print(x)
    print("\n\n")
