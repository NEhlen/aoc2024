import numpy as np


file = "05/input.txt"

with open(file, "r") as f:
    lines = [line.strip() for line in f.readlines()]


# ordering rules
# make ordering rules symmetric by having a before and after dict
before = {}  # nums in vals must come before key
after = {}  # nums in vals must come after key

for i, line in enumerate(lines):
    if line == "":
        instructions = lines[(i + 1) :]
        break
    b, a = [int(num) for num in line.split("|")]
    if b in after:
        after[b].update([a])
    else:
        after[b] = set([a])

    if a in before:
        before[a].update([b])
    else:
        before[a] = set([b])

# symmetrize keys
for key in after.keys():
    if key not in before.keys():
        before[key] = {}

for key in before.keys():
    if key not in after.keys():
        after[key] = {}

instructions = [[int(i) for i in inst.split(",")] for inst in instructions]

# check instructions
# because we have them symmetric now we can just check from one side
# for instruction in instructions:
solutionA = 0
solutionB = 0
for instruction in instructions:
    # check from left to right if the number is printed to the left of any
    # number in its before dict
    check = [
        set(instruction[(count + 1) :]).intersection(before[page])
        for count, page in enumerate(instruction)
    ]
    check_length = [len(c) == 0 for c in check]
    # the instruction is only correct if all checks are true
    correct = all(check_length)
    if correct:
        solutionA += instruction[len(instruction) // 2]
    else:
        # reorder instruction
        temp_list = instruction.copy()
        for page, c in zip(instruction[:-1][::-1], check[:-1][::-1]):
            if c:
                insert_at = max([temp_list.index(n) for n in c])
                element = temp_list.pop(temp_list.index(page))
                temp_list.insert(insert_at, element)
        solutionB += temp_list[len(temp_list) // 2]

print("Solution A:", solutionA)
print("Solution B:", solutionB)
