from functools import cache

file = "19/input.txt"

with open(file, "r") as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

towels = lines[0].split(", ")
patterns = lines[1:]


@cache
def check_pattern(pattern: str):
    if not pattern:
        return True
    checks = []
    for towel in towels:
        if pattern.startswith(towel):
            checks.append(check_pattern(pattern[len(towel) :]))
    return any(checks)


count_possible = 0
for pattern in patterns:
    print(pattern)
    count_possible += check_pattern(pattern)


print("Possible patterns:", count_possible)
