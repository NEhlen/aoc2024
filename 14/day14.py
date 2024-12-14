import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
import scipy.special

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


# calculate the entropy of the configuration
# for that, split the room into smaller grids as macrostates
# with number of tiles (N1, N2, N3, N4, ...)
# the macrostate configuration is then given by their occupation number
# (n1, n2, n3, n4, ...)
# The number of microstates for a single grid
# is given by wi = (Ni + ni - 1 over ni) (binomial coefficient)
# the total number of microstates for the full macrostate is then given
# by
# W = w1 * w2 * w3 * w4 * ...
# and the entropy by
# S ~ ln(W) = ln(w1) + ln(w2) + ln(w3) + ln(w4) + ...
# the state with lowest entropy will be the state with the lowest amount
# of microstates that give the macrostate (n1, n2, n3, n4, ...)
# this will happend for a very ordered state where few
# robots will be scattered randomly thus finding the ordered state
# of a picture of a christmas tree
def calculate_entropy(robots: list[dict[str, complex]]):
    room = make_map(robots)
    n_slc = 10
    x_slices = list(range(0, room.shape[1], n_slc))
    if x_slices[-1] != room.shape[1]:
        x_slices += [room.shape[1]]
    y_slices = list(range(0, room.shape[0], n_slc))
    if y_slices[-1] != room.shape[0]:
        y_slices += [room.shape[0]]
    lnw = 0
    for i, nx in enumerate(x_slices[:-1]):
        for j, ny in enumerate(y_slices[:-1]):
            grid = room[ny : y_slices[j + 1], nx : x_slices[i + 1]]

            N = grid.shape[0] * grid.shape[1]
            n = grid.sum()
            lnw += np.log(scipy.special.binom(N + n - 1, n))
    return lnw


# run the simulation for a given amount of steps
# important: give the robots as a deepcopy, otherwise the
# dicts in the list will be modified during the iteration
# and the robots won't be in the correct starting position
# for part B
# for part B, the entropy of each configuration is calculated
# by splitting the room into smaller grids to define a macrostate
# see above
def run_simulation(
    robots: list[dict[str, complex]], simulation_time: int
) -> tuple[list[dict[str, complex]], list[float]]:
    entropy = np.zeros(simulation_time)
    # run simulation
    for i in range(simulation_time):
        # move robots
        for robot in robots:
            pn: complex = robot["p"] + robot["v"]
            robot["p"] = pn.real % width + 1j * (pn.imag % height)

        # get variance of x and y positions for part B
        entropy[i] = calculate_entropy(robots)

    return robots, entropy


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
fig0, ax0 = plt.subplots(1, 1, dpi=200)
ax0.set_xlabel("tiles x")
ax0.set_ylabel("tiles y")
ax0.imshow(room_A)
plt.tight_layout()
fig0.savefig("14/partA_configuration.png")
print("Safty Factor A:", get_score_A(room_A))


# part B
# choose a high simulation time arbitrarily
# collect the entropies at each timestamp
# find the minimum entropy
# use that to rerun the simulation with this timestep as the
# simulation time.

# Alternative Solution:
# run simulation once with a large simulation time, save
# every timestep as an image in a folder
# scroll through the images in the file explorer
# the christmas tree will be obvious
simulation_time = 10000
_, entropy = run_simulation(deepcopy(robots), simulation_time)

# find entropy minimum
simulation_time_B = np.where(entropy == min(entropy))[0][0] + 1

# plot entropy over time
fig1, ax1 = plt.subplots(1, 1, dpi=200)
ax1.scatter(range(len(entropy)), entropy, s=5)
ax1.plot(range(len(entropy)), entropy, color="tab:gray", zorder=-1)
ax1.scatter(simulation_time_B, min(entropy), zorder=-2, s=200)
ax1.text(
    simulation_time_B - 500,
    min(entropy),
    f"Minimum Entropy ts:\n${simulation_time_B}$" + r"$\,\rm{s}$",
    ha="right",
    bbox=dict(boxstyle="round", ec="tab:orange", fc="none", pad=0.6),
)
ax1.set_xlabel("Simulation Time [s]")
ax1.set_ylabel("Entropy [nits]")
plt.tight_layout()
fig1.savefig("14/partB_entropy.png")

# rerun simulation with the correct final timestamp
robots_B, _ = run_simulation(deepcopy(robots), simulation_time_B)
print("Shortest Simulation Time B:", simulation_time_B)

# plot tree
room_B = make_map(robots_B)
fig2, ax2 = plt.subplots(1, 1, dpi=200)
ax2.set_xlabel("tiles x")
ax2.set_ylabel("tiles y")
ax2.imshow(room_B)
plt.tight_layout()
fig2.savefig("14/partB_configuration.png")
plt.show()
