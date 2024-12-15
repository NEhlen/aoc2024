import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt

np.set_printoptions(linewidth=800)

file = "15/input.txt"

step_through = True

with open(file, "r") as f:
    plan, moves = f.read().strip().split("\n\n")


def print_plan(
    robot: complex, boxes_l: set[complex], boxes_r: set[complex], walls: set[complex]
) -> np.ndarray:
    floor = np.array([["."] * plan.shape[1]] * plan.shape[0])
    # walls
    wx, wy = zip(*[(int(w.real), int(w.imag)) for w in walls])
    floor[wy, wx] = "#"

    # boxes
    bx, by = zip(*[(int(b.real), int(b.imag)) for b in boxes_l])
    floor[by, bx] = "["
    brx, bry = zip(*[(int(b.real), int(b.imag)) for b in boxes_r])
    floor[bry, brx] = "]"

    # robot
    floor[int(robot.imag), int(robot.real)] = "@"
    return floor


def plot_plan(
    robot: complex, boxes_l: set[complex], boxes_r: set[complex], walls: set[complex]
):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 1)
    # walls
    wx, wy = zip(*[(w.real, w.imag) for w in walls])
    ax.scatter(wx, wy)

    # boxes
    bx, by = zip(*[(b.real, b.imag) for b in boxes_l])
    ax.scatter(bx, by)
    brx, bry = zip(*[(b.real, b.imag) for b in boxes_r])
    ax.scatter(brx, bry)

    # robot
    ax.scatter([robot.real], [robot.imag])

    ax.set_ylim(ax.get_ylim()[::-1])


def score_boxes(boxes: set[complex]) -> int:
    return sum([int(box.imag) * 100 + int(box.real) for box in boxes])


# process moves
moves = moves.replace("\n", "")
dir_map = {"v": 0 + 1j, "<": -1 + 0j, ">": 1 + 0j, "^": 0 - 1j}
dir_map_reverse = dict(zip(dir_map.values(), dir_map.keys()))
moves = [dir_map[char_] for char_ in moves]


# modify map
plan = plan.replace("#", "##")
plan = plan.replace("O", "[]")
plan = plan.replace(".", "..")
plan = plan.replace("@", "@.")

plan = np.array([[char_ for char_ in line] for line in plan.split("\n")])
ry, rx = np.where(plan == "@")
starting_pos_robot = rx[0] + 1j * ry[0]

walls = list(zip(*np.where(plan == "#")))
walls = [wall[1] + 1j * wall[0] for wall in walls]
walls = set(walls)

boxes = list(zip(*np.where(plan == "[")))
boxes_l = [box[1] + 1j * box[0] for box in boxes]
boxes_l = set(boxes_l)
boxes_r = [box[1] + 1 + 1j * box[0] for box in boxes]
boxes_r = set(boxes_r)


robot_pos = starting_pos_robot.copy()
for row in print_plan(robot_pos, boxes_l, boxes_r, walls):
    print(" ".join(row))

for move in moves:
    print(dir_map_reverse[move])
    movement_check = True
    boxes_to_move_l = set()
    boxes_to_move_r = set()
    i = 1
    to_check = {robot_pos + move}
    while movement_check:
        i += 1
        cont = False
        for tc in to_check:
            if tc in boxes_l:
                boxes_l = boxes_l - {tc}
                boxes_r = boxes_r - {tc + 1}
                boxes_to_move_l.add(tc)
                boxes_to_move_r.add(tc + 1)
                to_check = to_check.union({tc + move, tc + 1 + move})
                cont = True
            elif tc in boxes_r:
                boxes_l = boxes_l - {tc - 1}
                boxes_r = boxes_r - {tc}
                boxes_to_move_l.add(tc - 1)
                boxes_to_move_r.add(tc)
                to_check = to_check.union({tc - 1 + move, tc + move})
                cont = True
            elif tc in walls:
                movement_check = False
                boxes_l = boxes_l.union(boxes_to_move_l)
                boxes_r = boxes_r.union(boxes_to_move_r)
                cont = True
                break
        if not cont:
            movement_check = False
            robot_pos += move
            boxes_l = boxes_l - boxes_to_move_l
            boxes_l = boxes_l.union({box + move for box in boxes_to_move_l})
            boxes_r = boxes_r - boxes_to_move_r
            boxes_r = boxes_r.union({box + move for box in boxes_to_move_r})
            break

    if step_through:
        input("")
        for row in print_plan(robot_pos, boxes_l, boxes_r, walls):
            print(" ".join(row))

print("GPS score B:", score_boxes(boxes_l))
