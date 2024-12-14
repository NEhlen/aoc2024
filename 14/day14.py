import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

file = "14/input.txt"
width, height = 11, 7
width, height = 101, 103
simulation_time_A = 100

with open(file, "r") as f:
    lines = [line.strip() for line in f.readlines()]


# make a map out of the robot positions by counting the
# robots on each tile
def make_map(robots: dict[str, complex]) -> np.ndarray:
    xs = [robot["p"].real for robot in robots]
    ys = [robot["p"].imag for robot in robots]

    room = np.zeros((height, width), dtype=int)
    for x, y in zip(xs, ys):
        room[int(y), int(x)] += 1

    return room


# split the room into quadrants and multiply their sums
def get_score_A(room: np.ndarray) -> int:
    mid_x = room.shape[1] // 2
    mid_y = room.shape[0] // 2
    quad_0 = room[:mid_y, :mid_x]
    quad_1 = room[(mid_y + 1) :, :mid_x]
    quad_2 = room[:mid_y, (mid_x + 1) :]
    quad_3 = room[(mid_y + 1) :, (mid_x + 1) :]
    return quad_0.sum() * quad_1.sum() * quad_2.sum() * quad_3.sum()


# run the simulation for a given amount of steps
# important: give the robots as a deepcopy, otherwise the
# dicts in the list will be modified during the iteration
# and the robots won't be in the correct starting position
# for part B
# the variances are used in part B
def run_simulation(
    robots: list[dict[str, complex]], simulation_time: int
) -> tuple[list[dict[str, complex]], tuple[list[float], list[float]]]:
    variances_x = []
    variances_y = []
    # run simulation
    for _ in range(simulation_time):
        # move robots
        for robot in robots:
            pn: complex = robot["p"] + robot["v"]
            robot["p"] = pn.real % width + 1j * (pn.imag % height)

        # get variance of x and y positions for part B
        xs = np.array([robot["p"].real for robot in robots])
        ys = np.array([robot["p"].imag for robot in robots])
        var_x = xs.var()
        var_y = ys.var()
        variances_x.append(var_x)
        variances_y.append(var_y)

    return robots, (variances_x, variances_y)


# run through file and generate the robots
robots = []
for line in lines:
    p, v = line.split()
    p = p[2:]
    v = v[2:]
    px, py = p.split(",")
    vx, vy = v.split(",")
    robots.append(
        {
            "p": int(px) + 1j * int(py),
            "v": int(vx) + 1j * int(vy),
        }
    )


# part A
robots_A, _ = run_simulation(deepcopy(robots), simulation_time_A)
room_A = make_map(robots_A)
plt.imshow(room_A)

print("Safte Factor A:", get_score_A(room_A))


# part B
# choose a high simulation time arbitrarily
# collect the variances in x and y and find a timestep
# where both varx and vary are minimal
# use that to rerun the simulation with this timestep as the
# simulation time.

# Alternative Solution:
# run simulation once with a large simulation time, save
# every timestep as an image in a folder
# scroll through the images in the file explorer
# the christmas tree will be obvious
simulation_time = 10000
_, (variances_x, variances_y) = run_simulation(deepcopy(robots), simulation_time)

# find where minima of variances coincide
minima_var_x = np.where(variances_x == min(variances_x))[0]
minima_var_y = np.where(variances_y == min(variances_y))[0]
for count, mvy in enumerate(minima_var_y):
    if mvy in minima_var_x:
        break
simulation_time_B = minima_var_y[count] + 1

robots_B, _ = run_simulation(deepcopy(robots), simulation_time_B)
room_B = make_map(robots_B)
plt.imshow(room_B)
print("Shortest Simulation Time B:", simulation_time_B)
