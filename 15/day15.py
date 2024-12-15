import numpy as np
from copy import deepcopy

file = "15/input.txt"

with open(file, "r") as f:
    plan, moves = f.read().strip().split("\n\n")


def plot_plan(robot: complex, boxes: set[complex], walls: set[complex]):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 1)
    # walls
    wx, wy = zip(*[(w.real, w.imag) for w in walls])
    ax.scatter(wx, wy)

    # boxes
    bx, by = zip(*[(b.real, b.imag) for b in boxes])
    ax.scatter(bx, by)

    # robot
    ax.scatter([robot.real], [robot.imag])

    ax.set_ylim(ax.get_ylim()[::-1])


def print_plan(robot: complex, boxes: set[complex], walls: set[complex]) -> np.ndarray:
    floor = np.array([["."] * plan.shape[1]] * plan.shape[0])
    # walls
    wx, wy = zip(*[(int(w.real), int(w.imag)) for w in walls])
    floor[wy, wx] = "#"

    # boxes
    bx, by = zip(*[(int(b.real), int(b.imag)) for b in boxes])
    floor[by, bx] = "O"

    # robot
    floor[int(robot.imag), int(robot.real)] = "@"
    return floor


def score_boxes(boxes: set[complex]) -> int:
    return sum([int(box.imag) * 100 + int(box.real) for box in boxes])


# process moves
moves = moves.replace("\n", "")
dir_map = {"v": 0 + 1j, "<": -1 + 0j, ">": 1 + 0j, "^": 0 - 1j}
moves = [dir_map[char_] for char_ in moves]

# process map
plan = np.array([[char_ for char_ in line] for line in plan.split("\n")])
ry, rx = np.where(plan == "@")
starting_pos_robot = rx[0] + 1j * ry[0]

boxes = list(zip(*np.where(plan == "O")))
boxes = [box[1] + 1j * box[0] for box in boxes]
boxes = set(boxes)

walls = list(zip(*np.where(plan == "#")))
walls = [wall[1] + 1j * wall[0] for wall in walls]
walls = set(walls)

robot_pos = starting_pos_robot.copy()
for move in moves:
    print(move)
    movement_check = True
    boxes_to_move = set()
    i = 1
    while movement_check:
        pos_check = robot_pos + move * i
        if pos_check in boxes:
            boxes = boxes - {pos_check}
            boxes_to_move.add(pos_check)
            i += 1
        elif pos_check in walls:
            movement_check = False
            boxes = boxes.union(boxes_to_move)
        else:
            movement_check = False
            robot_pos += move
            boxes = boxes.union({box + move for box in boxes_to_move})

print_plan(robot_pos, boxes, walls)
print("GPS A:", score_boxes(boxes))
