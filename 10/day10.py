import numpy as np

file = "niels/10/input.txt"

with open(file, "r") as f:
    lines = [line.strip() for line in f.readlines()]

topomap = np.array([[int(char_) for char_ in line] for line in lines])

starting_positions = np.array(list(zip(*np.where(topomap == 0))))

dirs = np.array([[0, 1], [1, 0], [0, -1], [-1, 0]])


def move(pos, previous_val: int = -1, reached=set()):
    if 0 <= pos[0] < topomap.shape[0] and 0 <= pos[1] < topomap.shape[1]:
        val = topomap[*pos]
        if val != (previous_val + 1):
            return 0, reached
        if val == 9:
            return 1, reached.union({(int(pos[0]), int(pos[1]))})
        total = 0

        for dir_ in dirs:
            n, r = move(pos + dir_, val)
            total += n
            reached = reached.union(r)
        return total, reached
    return 0, reached


optionsA = 0
optionsB = 0
for start in starting_positions:
    count, reached_goals = move(start, -1)
    optionsA += len(reached_goals)
    optionsB += count

print("Number of options A:", optionsA)
print("Number of options B:", optionsB)
