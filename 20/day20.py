import numpy as np
import pandas as pd

file = "20/input.txt"

with open(file, "r") as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

plan = np.array([[char for char in line] for line in lines])

start = np.where(plan == "S")
start = start[1][0] + 1j * start[0][0]

end = np.where(plan == "E")
end = end[1][0] + 1j * end[0][0]


dirs = {1 + 0j, -1 + 0j, 1j, -1j}  # directions to neighbors


path = np.where(plan == ".")
path = path[1] + 1j * path[0]
path = set(path)

walls = np.where(plan == "#")
walls = walls[1] + 1j * walls[0]
walls = set(walls)

# run along path
# to get the number of steps to each point on the path from the start
cur_pos = start
path_dict = {}
path_dict[start] = 0
for i in range(1, len(path) + 1):
    for dir_ in dirs:
        if cur_pos + dir_ in path and cur_pos + dir_ not in path_dict.keys():
            path_dict[cur_pos + dir_] = i
            cur_pos += dir_
            break
path_dict[end] = i + 1

# cheat dict
cheat_dict = {}
# for each point in path check in all directions if there is a wall and
# if there is a tile that's part of the path behind that wall
# if yes, take the difference between the two points in the path to get
# the steps between them along the path and subtract 2 because of the
# movement through the wall
# this is the distance saved by cheating
for p, val in path_dict.items():
    for dir_ in dirs:
        if (p + dir_ in walls) and (p + 2 * dir_ in path_dict.keys()):
            diff = path_dict[p + 2 * dir_] - val
            # only take positive values that would improve the position along the path
            if diff > 0:
                cheat_dict[(p, p + 2 * dir_)] = diff - 2

t = pd.DataFrame(cheat_dict, index=["diff"]).T
print(
    "Cheats saving more than 100 picoseconds A",
    t[t["diff"] >= 100].value_counts("diff").sort_index().sum(),
)

# part B
distance = 20
# cheat dict
cheat_dict = {}
# O(n^2) but n is reasonably small
# check all pairs of points on path, if the manhatten distance is less than distance
# and the difference in steps is more than 1, add to cheat dict
# the difference between the two points in the path minus the manhatten distance
# because that's the amount of steps saved by cheating
for p, val in path_dict.items():
    for p2, val2 in path_dict.items():
        manhattan = abs((p - p2).real) + abs((p - p2).imag)
        if (manhattan <= distance) and ((val2 - val) > 1):
            cheat_dict[(p, p2)] = val2 - val - manhattan

t = pd.DataFrame(cheat_dict, index=["diff"]).T
print(
    "Cheats saving more than 100 picoseconds B",
    t[t["diff"] >= 100].value_counts("diff").sort_index().sum(),
)
