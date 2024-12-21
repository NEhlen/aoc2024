import numpy as np
import re
from functools import cache
from itertools import product

file = "21/input.txt"

with open(file, "r") as f:
    lines = [line.strip() for line in f.readlines()]


# connection matrix for the numpad
# buttons      A, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
con_numpad = np.array(
    [
        [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],  # A
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # 0
        [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],  # 1
        [0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0],  # 2
        [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],  # 3
        [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0],  # 4
        [0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],  # 5
        [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],  # 6
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],  # 7
        [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],  # 8
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    ],  # 9
)
base_numpad = {
    "A": 0,
    "0": 1,
    "1": 2,
    "2": 3,
    "3": 4,
    "4": 5,
    "5": 6,
    "6": 7,
    "7": 8,
    "8": 9,
    "9": 10,
}

# get the distance matrix from each numpad button to each other button
dist_numpad = con_numpad.copy()
counter = 2
while np.any(dist_numpad == 0):
    dist_numpad[dist_numpad == 0] += (
        (dist_numpad @ con_numpad)[dist_numpad == 0] != 0
    ) * counter
    counter += 1
np.fill_diagonal(dist_numpad, 0)


numpad_coords = {
    "7": 0 + 0j,
    "8": 1 + 0j,
    "9": 2 + 0j,
    "4": 0 + 1j,
    "5": 1 + 1j,
    "6": 2 + 1j,
    "1": 0 + 2j,
    "2": 1 + 2j,
    "3": 2 + 2j,
    "0": 1 + 3j,
    "A": 2 + 3j,
}

forbidden_numpad = 0 + 3j

# connection matrix for arrow keypad
# buttons A, ^, <, v, >
con_arrow = np.array(
    [
        [0, 1, 0, 0, 1],  # A
        [1, 0, 0, 1, 0],  # ^
        [0, 0, 0, 1, 0],  # <
        [0, 1, 1, 0, 1],  # v
        [1, 0, 0, 1, 0],  # >
    ]
)
base_arrow = {"A": 0, "^": 1, "<": 2, "v": 3, ">": 4}
# get the distance matrix from each arrow button to each other button
dist_arrow = con_arrow.copy()
counter = 2
while np.any(dist_arrow == 0):
    dist_arrow[dist_arrow == 0] += (
        (dist_arrow @ con_arrow)[dist_arrow == 0] != 0
    ) * counter
    counter += 1
np.fill_diagonal(dist_arrow, 0)

# arrow keypad coordinates
arrow_coords = {
    "^": 1 + 0j,
    "A": 2 + 0j,
    "<": 0 + 1j,
    "v": 1 + 1j,
    ">": 2 + 1j,
}

forbidden_arrows = 0 + 0j

movement_cost = {"<^": 2, "<v": 1, "v>": 1, ">^": 2}


def robot(moves: str, depth: int = 0, adder: int = 0):

    if depth == 1:
        return moves
    cur_pos = "A"
    movements = []
    for move in moves:
        diff = arrow_coords[move] - arrow_coords[cur_pos]
        movement = ""

        if arrow_coords[move].real == 0 or arrow_coords[cur_pos].real == 0:
            if diff.imag >= 0:
                movement += "v" * int(diff.imag)

            if diff.real <= 0:
                movement += "<" * int(-diff.real)

            if diff.real > 0:
                movement += ">" * int(diff.real)

            if diff.imag < 0:
                movement += "^" * int(-diff.imag)

        else:
            if diff.real <= 0:
                movement += "<" * int(-diff.real)

            if diff.imag < 0:
                movement += "^" * int(-diff.imag)

            if diff.imag >= 0:
                movement += "v" * int(diff.imag)

            if diff.real > 0:
                movement += ">" * int(diff.real)

        movement += "A"
        movements.append(movement)

        cur_pos = move
    return movements


sum_complexities = 0


def numpad2robot(numpad: str):
    cur_pos = "A"
    movements_numpad = []
    movement_counter = 1
    for c in numpad:
        movement_counter *= 1
        diff = numpad_coords[c] - numpad_coords[cur_pos]
        movement = ""
        if (
            numpad_coords[c].real + 1j * numpad_coords[cur_pos].imag == forbidden_numpad
        ) or (
            numpad_coords[cur_pos].real + 1j * numpad_coords[c].imag == forbidden_numpad
        ):

            if diff.real > 0:
                movement += ">" * int(diff.real)

            if diff.imag >= 0:
                movement += "v" * int(diff.imag)

            if diff.imag < 0:
                movement += "^" * int(-diff.imag)

            if diff.real <= 0:
                movement += "<" * int(-diff.real)

        else:
            if diff.real <= 0:
                movement += "<" * int(-diff.real)

            if diff.imag < 0:
                movement += "^" * int(-diff.imag)

            if diff.imag >= 0:
                movement += "v" * int(diff.imag)

            if diff.real > 0:
                movement += ">" * int(diff.real)

        movement += "A"
        movements_numpad.append(movement)
        cur_pos = c

    return "".join(movements_numpad)


for to_push in lines:
    print(to_push, len("".join(robot("".join(robot(numpad2robot(to_push)))))))
    sum_complexities += len(
        "".join(robot("".join(robot(numpad2robot(to_push)))))
    ) * int(re.sub(r"\D", "", to_push))

print("Sum of complexities A:", sum_complexities)

# %%
# idea:
# make another connection matrix but from robot i to robot j
# base: pairs of buttons (from, to)
# to move button i from a to b the matrix row
# (a,b) should have a 1 for the moves robot j needs to do
# for the arrow keys, there are only 25 pairs of combinations
# so we end up with a 25x25 matrix


def getPath(from_, to_):
    diff = to_ - from_
    movement = ""

    if to_.real == 0 or from_.real == 0:
        if diff.imag >= 0:
            movement += "v" * int(diff.imag)

        if diff.real <= 0:
            movement += "<" * int(-diff.real)

        if diff.real > 0:
            movement += ">" * int(diff.real)

        if diff.imag < 0:
            movement += "^" * int(-diff.imag)

    else:
        if diff.real <= 0:
            movement += "<" * int(-diff.real)

        if diff.imag < 0:
            movement += "^" * int(-diff.imag)

        if diff.imag >= 0:
            movement += "v" * int(diff.imag)

        if diff.real > 0:
            movement += ">" * int(diff.real)

    return movement + "A"


connection_matrix = np.zeros((25, 25), dtype=int)
basis = [x + y for (x, y) in product("A^<v>", "A^<v>")]

for i, pair in enumerate(basis):
    a, b = pair[0], pair[1]
    path = getPath(arrow_coords[a], arrow_coords[b])
    for p1, p2 in zip("A" + path[:-1], path):
        connection_matrix[i, basis.index(p1 + p2)] += 1


# generate the deep connection matrix of robots at depth N
# by repeated matrix multiplication
def deepConnection(depth):
    return np.linalg.matrix_power(connection_matrix, depth)


total = 0
for to_push in lines:
    depth = 25

    deep_connection_matrix = deepConnection(
        depth
    )  # connection from final robot to depth N
    # sum of all move counts for each pair of (from, to) buttons on final input how
    # many moves of robot at depth depth is needed
    deep_connection_counts = deep_connection_matrix.sum(axis=1)

    count = 0
    to_push_rb = "A" + numpad2robot(to_push)
    for i in range(0, len(to_push_rb) - 1):
        a, b = to_push_rb[i], to_push_rb[i + 1]
        count += deep_connection_counts[basis.index(a + b)]

    total += count * int(re.sub(r"\D", "", to_push))
    print(to_push, count)

print("total B", total)
