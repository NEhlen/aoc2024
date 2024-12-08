import numpy as np

file = "08/input.txt"
visualize = False

with open(file, "r") as f:
    lines = [line.strip() for line in f.readlines()]

data = np.array([[char for char in line] for line in lines])

# get antenna types
antenna_types = np.unique(data)
antenna_types = antenna_types[antenna_types != "."]

# part A
all_nodes = []
for atype in antenna_types:
    acy, acx = np.where(data == atype)
    antennas = np.vstack([acy, acx]).T

    # reshape to make pairwise diffs
    # adiffs[i,j] holds the difference between vector in row
    # i and vector in row j in antennas
    adiffs = antennas[:, None, :] - antennas[None, :, :]

    # get the nodes positions by adding the diffs to the original
    # antenna positions
    nodes_3d = antennas[:, None, :] + adiffs

    # flatten the nodes down to a 2d array
    nodes = nodes_3d.reshape(-1, nodes_3d.shape[-1])

    # mask the "on-diagonals" of nodes_3d because they are artifacts
    # of the vector optimization (we're adding and subtracting the
    # antenna position to itself so just end up with the original
    # antenanna position)
    mask = ~np.eye(nodes_3d.shape[0], dtype=bool).reshape(-1)
    nodes = nodes[mask]
    all_nodes.append(nodes)

all_nodes = np.vstack(all_nodes)

# filter out nodes outside of the "playing field"
all_nodes = all_nodes[
    (all_nodes[:, 0] >= 0)
    & (all_nodes[:, 0] < data.shape[0])
    & (all_nodes[:, 1] >= 0)
    & (all_nodes[:, 1] < data.shape[1])
]

print("Unique Antinodes A:", len(np.unique(all_nodes, axis=0)))

# visualize
if visualize:
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.invert_yaxis()

    for atype in antenna_types:
        acy, acx = np.where(data == atype)
        ax.scatter(acx, acy)
        for x, y in zip(acx, acy):
            ax.text(x, y, atype)
    ax.scatter(all_nodes[:, 1], all_nodes[:, 0], s=20, marker="s")


# part B
all_nodes = []
for atype in antenna_types:
    acy, acx = np.where(data == atype)
    antennas = np.vstack([acy, acx]).T

    # reshape to make pairwise diffs
    # adiffs[i,j] holds the difference between vector in row
    # i and vector in row j in antennas
    adiffs = antennas[:, None, :] - antennas[None, :, :]

    # get the nodes positions by adding n times the diffs to the
    # original antenna positions
    # repeat 50 times, in a 50x50 grid this means we ensure we've
    # reached any potential note
    for n in range(50):
        nodes_3d = antennas[:, None, :] + n * adiffs
        # flatten the nodes down to a 2d array
        nodes = nodes_3d.reshape(-1, nodes_3d.shape[-1])
        all_nodes.append(nodes)

all_nodes = np.vstack(all_nodes)

# filter out nodes outside of the "playing field"
all_nodes = all_nodes[
    (all_nodes[:, 0] >= 0)
    & (all_nodes[:, 0] < data.shape[0])
    & (all_nodes[:, 1] >= 0)
    & (all_nodes[:, 1] < data.shape[1])
]
print("Unique Antinodes B:", len(np.unique(all_nodes, axis=0)))


# visualize
if visualize:
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.invert_yaxis()

    for atype in antenna_types:
        acy, acx = np.where(data == atype)
        ax.scatter(acx, acy)
        for x, y in zip(acx, acy):
            ax.text(x, y, atype)
    ax.scatter(all_nodes[:, 1], all_nodes[:, 0], s=20, marker="s")
