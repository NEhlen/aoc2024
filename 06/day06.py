import numpy as np


file = "06/input.txt"

with open(file, "r") as f:
    lines = [line.strip() for line in f.readlines()]

# find field range
max_x = len(lines[0])
max_y = len(lines)
# find obstacle coordinates
obstacles = [
    [pos + row * 1j for pos, char in enumerate(line) if char == "#"]
    for row, line in enumerate(lines)
]
# flatten
obstacles = [x for xs in obstacles for x in xs]

# guard
start_pos = [
    [pos + row * 1j for pos, char in enumerate(line) if char == "^"]
    for row, line in enumerate(lines)
    if "^" in line
][0][0]
start_dir_ = -1j


# check if x is in boundaries of field
def bound_check(x):
    if x.real < 0 or x.real >= max_x:
        return False
    elif x.imag < 0 or x.imag >= max_y:
        return False
    else:
        return True


# cast a ray
# It should be possible to make this into a recursive function
# by calling raycast with a new start pos and start dir and an added
# obstacle along the way at the position of the new destination
# but I keep running into issues, so just brute-force instead
def raycast(start_pos, start_dir_, added_obstacle=None):
    pos = start_pos
    dir_ = start_dir_
    visited_pos = set()
    states = {(pos, dir_)}
    while bound_check(pos):
        visited_pos.add(pos)
        # check if next step possible
        destination = pos + dir_
        if added_obstacle:
            can_visit = destination not in (obstacles + [added_obstacle])
        else:
            can_visit = destination not in obstacles
        # if there is an obstacle on the next step, turn right
        # note: usually turn right would be done with -1j multiplication
        # but the y-axis is pointing down here, so needs to be done via 1j
        # multiplication
        if (not can_visit) and bound_check(destination):
            dir_ *= 1j
        else:
            pos = destination

        new_state = (pos, dir_)
        # check if same position, same direction was already visited
        # in that case we're in a loop
        if new_state in states:
            return True, visited_pos
        # add state to cache
        states.add(new_state)
    return False, visited_pos


# get path
_, path = raycast(start_pos, start_dir_)
print("distinct visited tiles:", len(path))

count = 0
obstacle_candidates = path - {start_pos}
for obstacle in obstacle_candidates:
    if raycast(start_pos, start_dir_, obstacle)[0]:
        count += 1

print("New object positions:", count)
