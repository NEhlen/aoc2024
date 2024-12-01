import numpy as np


# load list
file = "01/test.txt"

with open(file, "r") as f:
    lines = f.readlines()

load_data = [line.split() for line in lines]
listA, listB = zip(*load_data)
listA = np.array([int(n) for n in listA])
listB = np.array([int(n) for n in listB])

listA.sort()
listB.sort()


# part A
diffs = np.abs(listA - listB)

print("Summed Differences:", diffs.sum())

similarity = 0
# part B
for element in listA:
    n_element_in_B = (listB == element).sum()
    similarity += element * n_element_in_B
