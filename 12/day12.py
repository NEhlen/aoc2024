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


connected_regions = {}
total_price = 0
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
        total_price += area * num_fences

print("Total Price A:", total_price)
