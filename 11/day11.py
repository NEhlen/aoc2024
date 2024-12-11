file = "11/input.txt"

with open(file, "r") as f:
    stones_start = f.read().strip().split()


def recursive_rules(stone: str, i: int, N: int, cache: dict) -> int:
    """
    recursion for rules
    stone is a str of an int
    i is the current amount of blinks
    N is the total amount of blinks to do
    cache is a dictionary that holds already evaluated states (could also be done
    with @cache modifier of functools) so that they can be skipped in the future
    """
    # if (stone, i) combination was evaluated already, just take that value
    if (stone, i) in cache:
        return cache[(stone, i)]
    # if total blinks reached, return 1
    if i == N:
        return 1
    # if the stone number is 0, recurse deeper with stone value "1"
    if int(stone) == 0:
        n = recursive_rules("1", i + 1, N, cache)
        cache[(stone, i)] = n
        return n
    # if the the number of digits in the stone number is even
    # split the number in the middle and recurse deeper and add
    # both results
    elif len(stone) % 2 == 0:
        n = recursive_rules(
            stone[: len(stone) // 2],
            i + 1,
            N,
            cache,
        ) + recursive_rules(
            str(int(stone[len(stone) // 2 :])),
            i + 1,
            N,
            cache,
        )
        cache[(stone, i)] = n
        return n
    # else recurse deeper with stone num * 2024
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
