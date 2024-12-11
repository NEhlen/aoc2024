file = "11/input.txt"

with open(file, "r") as f:
    stones_start = f.read().strip().split()


def recursive_rules(stone, i, N, cache):
    if (stone, i) in cache:
        return cache[(stone, i)]
    if i == N:
        return 1
    if int(stone) == 0:
        n = recursive_rules("1", i + 1, N, cache)
        cache[(stone, i)] = n
        return n
    elif len(stone) % 2 == 0:
        n = recursive_rules(
            stone[: len(stone) // 2], i + 1, N, cache
        ) + recursive_rules(str(int(stone[len(stone) // 2 :])), i + 1, N, cache)
        cache[(stone, i)] = n
        return n
    else:
        n = recursive_rules(str(int(stone) * 2024), i + 1, N, cache)
        cache[(stone, i)] = n
        return n


# part A
cache = dict()
N_blinks = 25
stones = stones_start.copy()
stones = [recursive_rules(stone, 0, N_blinks, cache) for stone in stones]

print("number of stones:", sum(stones))

# part B
cache = dict()
N_blinks = 75
stones = stones_start.copy()
stones = [recursive_rules(stone, 0, N_blinks, cache) for stone in stones]

print("number of stones:", sum(stones))
