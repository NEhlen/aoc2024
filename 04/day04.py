import numpy as np


file = "04/input.txt"

with open(file, "r") as f:
    lines = f.readlines()

data = np.array([[l for l in line.strip()] for line in lines])


def count_occurences(
    data: np.ndarray, filter_: np.ndarray, sum_axis: int | tuple[int]
) -> int:
    # create sliding window of array of size (1,4)
    v = np.lib.stride_tricks.sliding_window_view(data, filter_.shape)
    # count how many letters are equal
    count = np.squeeze(
        np.char.compare_chararrays(v, filter_, "==", True).sum(axis=sum_axis)
    )
    # find the ones where all are equal
    num_xmas = (count == (filter_ != "O").sum()).sum()
    return num_xmas


# horizontal
# filters
h_f = np.array([["X", "M", "A", "S"]])
h_b = np.array([["S", "A", "M", "X"]])

nhf = count_occurences(data, h_f, 3)
nhb = count_occurences(data, h_b, 3)

# vertical
# filters
v_f = np.array([["X"], ["M"], ["A"], ["S"]])
v_b = np.array([["S"], ["A"], ["M"], ["X"]])

nvf = count_occurences(data, v_f, 2)
nvb = count_occurences(data, v_b, 2)


# vertical
# diagonal
d_ff = np.array(
    [
        ["X", "O", "O", "O"],
        ["O", "M", "O", "O"],
        ["O", "O", "A", "O"],
        ["O", "O", "O", "S"],
    ]
)
d_bf = np.array(
    [
        ["O", "O", "O", "X"],
        ["O", "O", "M", "O"],
        ["O", "A", "O", "O"],
        ["S", "O", "O", "O"],
    ]
)
d_fb = np.array(
    [
        ["O", "O", "O", "S"],
        ["O", "O", "A", "O"],
        ["O", "M", "O", "O"],
        ["X", "O", "O", "O"],
    ]
)
d_bb = np.array(
    [
        ["S", "O", "O", "O"],
        ["O", "A", "O", "O"],
        ["O", "O", "M", "O"],
        ["O", "O", "O", "X"],
    ]
)

ndff = count_occurences(data, d_ff, (2, 3))
ndfb = count_occurences(data, d_fb, (2, 3))
ndbf = count_occurences(data, d_bf, (2, 3))
ndbb = count_occurences(data, d_bb, (2, 3))

print("total occurences:", nhb + nhf + nvb + nvf + ndff + ndfb + ndbf + ndbb)


# part b

mas_ff = np.array(
    [
        ["M", "O", "S"],
        ["O", "A", "O"],
        ["M", "O", "S"],
    ]
)
mas_fb = np.array(
    [
        ["S", "O", "S"],
        ["O", "A", "O"],
        ["M", "O", "M"],
    ]
)
mas_bf = np.array(
    [
        ["M", "O", "M"],
        ["O", "A", "O"],
        ["S", "O", "S"],
    ]
)
mas_bb = np.array(
    [
        ["S", "O", "M"],
        ["O", "A", "O"],
        ["S", "O", "M"],
    ]
)

nmff = count_occurences(data, mas_ff, (2, 3))
nmfb = count_occurences(data, mas_fb, (2, 3))
nmbf = count_occurences(data, mas_bf, (2, 3))
nmbb = count_occurences(data, mas_bb, (2, 3))

print("total mas:", nmff + nmfb + nmbf + nmbb)
