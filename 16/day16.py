# %%
import numpy as np
from collections import deque

file = "16/input.txt"

with open(file, "r") as f:
    lines = [line.strip() for line in f.readlines()]

# %%
plan = np.array([[char_ for char_ in line] for line in lines])
# %%
starting_point = list(zip(*np.where(plan == "S")))[0]
starting_point = starting_point[1] + 1j * starting_point[0]
starting_dir = 1 + 0j
# %%
ending_point = list(zip(*np.where(plan == "E")))[0]
ending_point = ending_point[1] + 1j * ending_point[0]
# %%
walls = list(zip(*np.where(plan == "#")))
walls = [wall[1] + 1j * wall[0] for wall in walls]
walls = set(walls)

# %%
check_dirs = {1 + 0j, -1 + 0j, 1j, -1j}
rotate_cw = 1j
rotate_ccw = -1j

# %%
score_move = 1
score_rotate = 1000


# %%
def compute_cost(facing: complex, dir_: complex):
    # angle_num = np.round(
    #     2
    #     * np.arccos(np.dot([facing.real, facing.imag], [dir_.real, dir_.imag]))
    #     / np.pi
    # ).astype(int)
    angle_num = 0
    cosphi = np.dot([facing.real, facing.imag], [dir_.real, dir_.imag])
    if cosphi == 0:
        angle_num = 1
    elif cosphi < 0:
        angle_num = 2
    return angle_num * score_rotate + score_move


visited = {starting_point}
scores = {starting_point: 0}
to_visit = deque(
    {
        (starting_point + dir_, compute_cost(starting_dir, dir_), dir_)
        for dir_ in check_dirs
    }
)
min_cost = 1000000000000
cur_pos = starting_point
end_reached = False
while to_visit:
    next_tile, next_score, next_dir = to_visit.popleft()
    # if it is a wall, remove from possibilities
    if next_tile in walls:
        continue
    # if we reached the ending point, check if the score
    # is lower than the current minimum score
    if next_tile == ending_point:
        if next_score < min_cost:
            min_cost = next_score

    # if the tile is already in the visited list
    filtered_visited = list(filter(lambda e: e == next_tile, visited))
    if filtered_visited:
        # if the score getting to this visited tile is lower,
        # update the score
        if scores[filtered_visited[0]] > next_score:
            scores[filtered_visited[0]] = next_score
            visited.add(next_tile)
            to_visit.extend(
                {
                    (next_tile + dir_, next_score + compute_cost(next_dir, dir_), dir_)
                    for dir_ in check_dirs
                }
            )
        else:
            continue
    visited.add(next_tile)
    scores[next_tile] = next_score
    for dir_ in check_dirs:
        nt = next_tile + dir_
        ns = next_score + compute_cost(next_dir, dir_)
        if nt not in walls:
            if nt not in visited:
                to_visit.append((nt, ns, dir_))
            elif ns < scores[nt]:
                to_visit.append((nt, ns, dir_))

print(min_cost)


# %%
print("Shortest Path:", scores[ending_point])
# %%
ending_path_seats = set()
ending_score = 10000000000000
cache = {}


# Part B
def move(pos: complex, facing: complex, path: list[complex], score: int):
    global ending_score
    global ending_path_seats
    if pos == ending_point:
        if score < ending_score:
            ending_path_seats = set(path)
            ending_score = score
        elif score == ending_score:
            ending_path_seats = ending_path_seats.union(set(path))
    for dir_ in check_dirs:
        nt = pos + dir_
        ns = score + compute_cost(facing, dir_)
        if nt not in walls:
            if nt not in path:
                if (nt, dir_) in cache:
                    if ns <= cache[(nt, dir_)]:
                        move(nt, dir_, path + [nt], ns)
                        cache[(nt, dir_)] = ns
                else:
                    move(nt, dir_, path + [nt], ns)
                    cache[(nt, dir_)] = ns


# %%
move(starting_point, 1 + 0j, [starting_point], 0)

# %%
seating_plan = plan.copy()
for seat in ending_path_seats:
    seating_plan[int(seat.imag), int(seat.real)] = "O"
for row in seating_plan:
    print(" ".join(row))
# %%
print("Seats along best paths:", len(ending_path_seats))

# %%
