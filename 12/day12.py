import numpy as np
from scipy.ndimage import label, find_objects
from scipy.signal import convolve2d

file = "12/input.txt"

with open(file, "r") as f:
    lines = [line.strip() for line in f.readlines()]

garden = np.array([[c for c in line] for line in lines])

# map letters to numbers to be able to do maths like convolutions
rename_dict = dict(zip(np.unique(garden), range(1, len(np.unique(garden)) + 1)))
rename = lambda e: rename_dict[e]
rename = np.vectorize(rename)
garden = rename(garden)


def count_fences(arr: np.ndarray) -> np.ndarray:
    connected = np.zeros(arr.shape, dtype=int)
    if connected.shape[1] > 1:
        is_connected = (convolve2d(arr, np.array([[1, -1]]), mode="valid") == 0).astype(
            int
        )
        connected[:, 1:] += is_connected
        connected[:, :-1] += is_connected
    if connected.shape[0] > 1:
        is_connected = (
            convolve2d(arr, np.array([[1], [-1]]), mode="valid") == 0
        ).astype(int)
        connected[1:] += is_connected
        connected[:-1] += is_connected

    fences = 4 - connected
    return fences


def get_sides(g):
    padded = np.zeros((g.shape[0] + 2, g.shape[1] + 2), dtype=int)
    padded[1:-1, 1:-1] = g
    g = padded
    cvu = np.zeros(g.shape, dtype=int)  #  up edges
    cvd = np.zeros(g.shape, dtype=int)  # down edges
    chl = np.zeros(g.shape, dtype=int)  # left edges
    chr = np.zeros(g.shape, dtype=int)  # right edges
    dvu = np.zeros(g.shape, dtype=int)
    dvd = np.zeros(g.shape, dtype=int)
    dhl = np.zeros(g.shape, dtype=int)
    dhr = np.zeros(g.shape, dtype=int)
    t0 = convolve2d(g, np.array([[1], [-1]]), mode="valid")
    t1 = convolve2d(g, np.array([[1, -1]]), mode="valid")
    cvu[1:] += t0 == 1
    cvd[:-1] += t0 == -1
    chl[:, 1:] += t1 == 1
    chr[:, :-1] += t1 == -1
    dvu[:, 1:] += convolve2d(cvu, np.array([[1, -1]]), mode="valid")
    dvd[:, 1:] += convolve2d(cvd, np.array([[1, -1]]), mode="valid")
    dhl[1:] += convolve2d(chl, np.array([[1], [-1]]), mode="valid")
    dhr[1:] += convolve2d(chr, np.array([[1], [-1]]), mode="valid")

    mask = g == 1
    return (
        (dvd[mask] > 0).sum()
        + (dvu[mask] > 0).sum()
        + (dhl[mask] > 0).sum()
        + (dhr[mask] > 0).sum()
    )


connected_regions = {}
total_price_A = 0
total_price_B = 0
for val in range(1, garden.max() + 1):
    # only find features exactly matching val, need to make boolean mask
    mask = garden == val
    labeled, num_features = label(mask)

    regions_for_val = []
    # run through labeled regions
    for i in range(1, num_features + 1):
        region_mask = labeled == i

        area = region_mask.sum()
        fences = count_fences(region_mask)
        num_fences = fences[region_mask].sum()
        num_sides = get_sides(region_mask)
        total_price_A += area * num_fences
        total_price_B += area * num_sides

print("Total Price A:", total_price_A)
print("Total Price B:", total_price_B)
