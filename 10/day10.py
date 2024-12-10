import numpy as np

file = "10/test2.txt"

with open(file, "r") as f:
    lines = [line.strip() for line in f.readlines()]

# load the topographical map as numpy array
topomap = np.array([[int(char_) for char_ in line] for line in lines])

# get an (N,2)-array of starting points where the value is 0
starting_positions = np.array(list(zip(*np.where(topomap == 0))))

# which directions to check
dirs = np.array([[0, 1], [1, 0], [0, -1], [-1, 0]])


# recursively move through paths
# keep count of possible paths and sets of unique reached endpoints
def move(pos, previous_val: int = -1, reached=set()):
    # check if the position is on the map, if not return 0
    if 0 <= pos[0] < topomap.shape[0] and 0 <= pos[1] < topomap.shape[1]:
        val = topomap[*pos]
        # if value - previous value != 1 it's not a valid step
        # and thus adds 0 pathways and no endpoint to the path
        if val != (previous_val + 1):
            return 0, reached
        # if the value is 9 we've reached the end and return 1 for
        # a possible path and add the position to the set of
        # reached points
        if val == 9:
            return 1, reached.union({(int(pos[0]), int(pos[1]))})
        # run through all 4 directions and recurse into move,
        # add the total counted pathways and add the reached
        # endpoints to the set of reached endpoints
        total = 0
        for dir_ in dirs:
            n, r = move(pos + dir_, val, reached)
            total += n
            reached = reached.union(r)
        # return counts of all pathways and set of reached endpoints
        return total, reached
    # not on map, so return 0 and don't modify the set of reached endpoints
    return 0, reached


# run recursion
optionsA = 0
optionsB = 0
for start in starting_positions:
    count, reached_goals = move(start, -1)
    optionsA += len(reached_goals)
    optionsB += count

print("Number of options A:", optionsA)
print("Number of options B:", optionsB)
