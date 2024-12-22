import numpy as np
from collections import Counter

file = "22/input.txt"

with open(file, "r") as f:
    lines = [line.strip() for line in f.readlines()]


class Monkey:
    def __init__(self, secret, stop_at=2000):
        self.secret = secret
        self.day_count = 0
        self.stop_at = stop_at

    def __iter__(self):
        return self

    def __next__(self):
        if self.day_count >= self.stop_at:
            raise StopIteration

        temp = self.secret * 64
        self.secret = self.secret ^ temp
        self.secret = self.secret % 16777216

        temp = self.secret // 32
        self.secret = self.secret ^ temp
        self.secret = self.secret % 16777216

        temp = self.secret * 2048
        self.secret = self.secret ^ temp
        self.secret = self.secret % 16777216
        self.day_count += 1
        return self.secret


monkeys = [Monkey(int(i), 2000) for i in lines]

monkey_matrix = np.zeros((2001, len(monkeys)), dtype=int)
monkey_matrix[0, :] = [int(i) for i in lines]
for i in range(1, 2001):
    for countm, monkey in enumerate(monkeys):
        t = next(monkey)
        monkey_matrix[i, countm] = t

print("Total sum A:", monkey_matrix[-1, :].sum())


# part B

# look for best results in monkey matrix

# get price from monkey matrix
mm_price = np.vectorize(lambda num: int(str(num)[-1]))(monkey_matrix)

# get price diffs
diffs = np.diff(mm_price, axis=0)

# write bananas to get for each 4 number sequence
diffs_bananas = dict()
monkey_dict = []
for m in range(mm_price.shape[1]):
    diffs_bananas_monkey = {}
    for i in range(len(diffs) - 3):
        t = tuple(map(int, diffs[i : i + 4, m]))
        if t not in diffs_bananas_monkey:
            diffs_bananas_monkey[t] = mm_price[i + 4, m]
    monkey_dict.append(diffs_bananas_monkey)
    diffs_bananas = dict(Counter(diffs_bananas) + Counter(diffs_bananas_monkey))

# get best sequence
print(
    "total Bananas:",
    max(diffs_bananas.values()),
    "With sequence:",
    max(diffs_bananas, key=diffs_bananas.get),
)
