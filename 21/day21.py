import numpy as np
import re
from functools import cache

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

for to_push in lines:

    cur_pos = "A"
    movements_numpad = []
    movement_counter = 1
    for c in to_push:
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

    print(to_push, len("".join(robot("".join(robot("".join(movements_numpad)))))))
    sum_complexities += len(
        "".join(robot("".join(robot("".join(movements_numpad)))))
    ) * int(re.sub(r"\D", "", to_push))

print("Sum of complexities A:", sum_complexities)


# should work if it didn't crash the kernel
# need to revisit later
@cache
def robot_B(moves: str, depth: int = 0):

    if depth == 25:
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

        movement += "A|"
        # movements.append(robot_B(movement, depth + 1))

        movements.append("".join([robot_B(m, depth + 1) for m in movement.split("|")]))

        cur_pos = move
    # if movements:
    #     print(movements, depth)
    return "".join(movements)


len("".join([robot_B(m) for m in movements_numpad]))
