from functools import cache

input_file = "19/input.txt"

with open(input_file, "r") as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

# The first line contains the towels, split by comma and space
towels = lines[0].split(", ")
# The remaining lines are the patterns to check
patterns = lines[1:]


# Define a cached function to check if a pattern can be formed using the towels
@cache
def check_pattern(pattern: str):
    # If the pattern is empty, it means it can be formed
    if not pattern:
        return 1
    checks = []
    # Check each towel to see if the pattern starts with it
    for towel in towels:
        if pattern.startswith(towel):
            # Recursively check the remaining part of the pattern
            checks.append(check_pattern(pattern[len(towel) :]))
    # Return the sum of all possible ways to form the pattern
    return sum(checks)


# Initialize counters for possible patterns
count_possible_A = 0
count_possible_B = 0

# Iterate over each pattern
for pattern in patterns:
    print(pattern)
    # Get the number of ways to form the pattern
    options = check_pattern(pattern)
    # Increment the counter if there is at least one way to form the pattern
    count_possible_A += options > 0
    # Increment the counter by the number of ways to form the pattern
    count_possible_B += options

print("Possible patterns A:", count_possible_A)
print("Possible patterns B:", count_possible_B)
