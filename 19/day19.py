from functools import cache

file = "19/input.txt"

with open(file, "r") as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

towels = lines[0].split(", ")
patterns = lines[1:]


@cache
def check_pattern(pattern: str):
    if not pattern:
        return 1
    checks = []
    for towel in towels:
        if pattern.startswith(towel):
            checks.append(check_pattern(pattern[len(towel) :]))
    return sum(checks)


count_possible_A = 0
count_possible_B = 0
for pattern in patterns:
    print(pattern)
    options = check_pattern(pattern)
    count_possible_A += options > 0
    count_possible_B += options


print("Possible patterns A:", count_possible_A)
print("Possible patterns B:", count_possible_B)
