import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

DIM = 70  # 6

start = 0 + 0j
end = DIM + (DIM) * 1j

STEPS = 1024  # 12

file = "18/input.txt"

with open(file, "r") as f:
    lines = [line.strip() for line in f.readlines()]

bts_all = [int(line.split(",")[0]) + 1j * int(line.split(",")[1]) for line in lines]

bts = bts_all[:STEPS]


# simple heuristic, just take manhatten distance to end
def heuristic(node: complex):
    return int((end.real - node.real) + (end.imag - node.imag))


# standard A star algo
def run_astar(bts):
    dirs = {1 + 0j, -1 + 0j, 1j, -1j}  # directions to neighbors

    potentials = {start}  #  set holds points to check

    # dictionary {i: j} will hold the cheapest previous node j to get to node i
    path_dict = {}

    cheapest_cost = {
        (i + 1j * j): 1000000000 for i in range(DIM + 1) for j in range(DIM + 1)
    }  #  dictionary {i: c} will hold the cheapest cost c to get to node i
    cheapest_cost[start] = 0

    # dictionary {i: c} will hold the heuristically predicted cost c to get to node i
    # used for efficient path search
    potential_cost = {
        (i + 1j * j): 1000000000 for i in range(DIM + 1) for j in range(DIM + 1)
    }
    potential_cost[start] = heuristic(start)

    # as long as there are potential nodes to check, run the algo
    while potentials:
        # get the potential cost from heuristics for all nodes in potentials
        temp_scores = {node: potential_cost[node] for node in potentials}
        # use potential cost to choose the node with the potentially lowest
        # cost to get to end as the next one to check
        cur_pos = min(temp_scores, key=temp_scores.get)
        # if the new node is the goal, end the algo
        if cur_pos == end:
            return path_dict, cheapest_cost

        # pop current node from potentials
        potentials = potentials - {cur_pos}
        # check the neighbors
        for dir_ in dirs:
            # neighbor coords
            new_pos = cur_pos + dir_
            # if the neighbor pos is on the grid and there's not byte on the position
            # keep going
            if (
                0 <= new_pos.real < (DIM + 1) and 0 <= new_pos.imag < (DIM + 1)
            ) and new_pos not in bts:
                # the new score to get to the new position is
                # the cheapest score of the current position + 1
                new_score = cheapest_cost[cur_pos] + 1
                # if the new score is better than the current lowest score to reach
                # the new node, put the current node as the parent in the path dict
                # add the new score as the cheapest score for the new postion
                # to the cost dict
                # recalculate potential cost to reach and for the new position
                # based on its new cheapest score and the heuristic to reach
                # the end
                if new_score < cheapest_cost[new_pos]:
                    path_dict[new_pos] = cur_pos
                    cheapest_cost[new_pos] = new_score
                    potential_cost[new_pos] = new_score + heuristic(new_pos)
                    potentials.add(new_pos)
    else:
        print("Failed")
        return None, None


# build the path from the path dict and the goal to reach
def build_path(path_dict: dict[complex, complex], cur_pos: complex):
    total_path = [cur_pos]
    while cur_pos in path_dict.keys():
        cur_pos = path_dict[cur_pos]
        total_path.append(cur_pos)
    return total_path[::-1]


# run the algorithm
path_dict, cheapest_cost = run_astar(bts)
# build shortest path from the path dictionary
path = build_path(path_dict, end)


# visualization helper functions
def plot_bts(bts: list[complex]):
    plan = np.zeros((DIM + 1, DIM + 1))
    for bt in bts:
        plan[int(bt.imag), int(bt.real)] = 1
    return plan


def plot_cost(cost_dict: dict[complex, int]):
    plan = np.zeros((DIM + 1, DIM + 1))
    for key, val in cost_dict.items():
        plan[int(key.imag), int(key.real)] = val
    plan[plan > 1000000] = np.nan
    return plan


def print_plan(bts: list[complex], path: list[complex]):
    plan = np.array([["."] * (DIM + 1)] * (DIM + 1))
    for bt in bts:
        plan[int(bt.imag), int(bt.real)] = "#"

    for p in path:
        plan[int(p.imag), int(p.real)] = "O"
    return plan


# visualization for terminal
plan = print_plan(bts, path)
for p in plan:
    print("".join(p))


# visualization matplotlib
fig, axarr = plt.subplots(2, 1, dpi=300, figsize=(20, 10), sharex=True, sharey=True)
axarr[0].scatter([p.real for p in path], [p.imag for p in path], s=5)
axarr[0].scatter([p.real for p in bts], [p.imag for p in bts], s=5)
axarr[0].set_aspect("equal")
axarr[0].set_title("Winning Path")
axarr[0].invert_yaxis()
axarr[1].imshow(plot_cost(cheapest_cost))
axarr[1].set_xlabel("X Coords [a.u.]")
axarr[1].set_ylabel("Y Coords [a.u.]")
axarr[1].set_title("Cost")
plt.tight_layout()
fig.savefig("18/partA.png")

# Answer
print("Minimum Steps A:", len(path) - 1)


# %%
# PART B
# just brute force, but only check when a new bit falls on the current best path
for len_bts in range(1024, len(bts_all)):
    if bts_all[len_bts] not in path:
        print(bts_all[len_bts])
        continue
    path_dict, cheapest_cost = run_astar(bts_all[: len_bts + 1])
    if not path_dict:
        print(len_bts)
        print(bts_all[len_bts])
        break
    path = build_path(path_dict, end)

print(
    "First Byte to cut off all paths:",
    str(int(bts_all[len_bts].real)) + "," + str(int(bts_all[len_bts].imag)),
)

# %%
