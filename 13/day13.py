import numpy as np


file = "13/input.txt"

with open(file, "r") as f:
    input_ = f.read()

blocks = []
for block in input_.split("\n\n"):
    a, b, p = block.strip().split("\n")

    a = a.split(":")[1]
    a = a.split(",")
    a = np.array([int(t.split("+")[1]) for t in a])

    b = b.split(":")[1]
    b = b.split(",")
    b = np.array([int(t.split("+")[1]) for t in b])

    p = p.split(":")[1]
    p = p.split(",")
    p = np.array([int(t.split("=")[1]) for t in p])

    blocks.append({"a": a, "b": b, "prize": p})

cost = np.array([3, 1])


def invert_2by2(arr: np.ndarray) -> np.ndarray:
    inv = np.array([[arr[1, 1], -arr[0, 1]], [-arr[1, 0], arr[0, 0]]])
    inv /= arr[0, 0] * arr[1, 1] - arr[1, 0] * arr[0, 1]
    return inv


tokens_spent_A = 0
tokens_spent_B = 0
diff_list = []
for block in blocks:
    A = np.vstack([block["a"], block["b"]], dtype=float).T

    Ainv = invert_2by2(A)
    moves_A = Ainv @ (block["prize"])
    moves_B = Ainv @ (block["prize"] + 10000000000000)

    if (
        abs(moves_A[0] - int(moves_A[0])) < 0.01
        or abs(moves_A[0] - int(moves_A[0]) - 1) < 0.01
    ) and (
        abs(moves_A[1] - int(moves_A[1])) < 0.01
        or abs(moves_A[1] - int(moves_A[1]) - 1) < 0.01
    ):
        tokens_A = moves_A @ cost
        tokens_spent_A += tokens_A

    if (
        abs(moves_B[0] - int(moves_B[0])) < 0.01
        or abs(moves_B[0] - int(moves_B[0]) - 1) < 0.01
    ) and (
        abs(moves_B[1] - int(moves_B[1])) < 0.01
        or abs(moves_B[1] - int(moves_B[1]) - 1) < 0.01
    ):
        tokens_B = moves_B @ cost
        tokens_spent_B += tokens_B

print("Tokens spent A:", int(tokens_spent_A))
print("Tokens spent B:", int(tokens_spent_B))
