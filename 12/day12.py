import numpy as np
from scipy.ndimage import label
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


# count fences for A
def count_fences(arr: np.ndarray) -> int:
    # check number of connected sides
    connected = np.zeros(arr.shape, dtype=int)
    if connected.shape[1] > 1:
        # check whether a tile is connected to the right by convolving with [1,-1]
        # a tile that is connected to the same type to the right will have a 0
        # after the convolution
        is_connected = (convolve2d(arr, np.array([[1, -1]]), mode="valid") == 0).astype(
            int
        )
        # the convolution is valid only in the part where both array fully overlap
        # so use array slicing to add the is_connected to the correct part of the
        # array
        connected[:, :-1] += is_connected
        # if a tile is connected to the right, the tile right of it is connected
        # to the left, so change array slice accordingly and at it to the count
        # of the other tile
        connected[:, 1:] += is_connected
    # same as above for the other dimension
    if connected.shape[0] > 1:
        is_connected = (
            convolve2d(arr, np.array([[1], [-1]]), mode="valid") == 0
        ).astype(int)
        connected[1:] += is_connected
        connected[:-1] += is_connected

    # the amount of fences around a tile is 4 minus the amount of connected sides
    # of the tile
    fences = 4 - connected
    # only add the parts of the actual tiles we're currently interested in
    mask = arr == 1
    return fences[mask].sum()


# count sides for B
def count_sides(g: np.ndarray) -> int:
    # pad the slice with zeros so edges along the top, bottom, right and left
    # of g can be detected with the same logic
    padded = np.zeros((g.shape[0] + 2, g.shape[1] + 2), dtype=int)
    padded[1:-1, 1:-1] = g
    g = padded
    cvu = np.zeros(g.shape, dtype=int)  #  up edges
    cvd = np.zeros(g.shape, dtype=int)  # down edges
    chl = np.zeros(g.shape, dtype=int)  # left edges
    chr = np.zeros(g.shape, dtype=int)  # right edges
    dvu = np.zeros(g.shape, dtype=int)  #  up edges
    dvd = np.zeros(g.shape, dtype=int)  # down edges
    dhl = np.zeros(g.shape, dtype=int)  # left edges
    dhr = np.zeros(g.shape, dtype=int)  # right edges
    # similar as in count_fences convolve along horizontal and
    # vertical directions to find the horizontal and vertical edges
    # here they are split between left, right, up, down edges
    # to allow for correct
    tv = convolve2d(g, np.array([[1], [-1]]), mode="valid")
    th = convolve2d(g, np.array([[1, -1]]), mode="valid")
    cvu[1:] += tv == 1
    cvd[:-1] += tv == -1
    chl[:, 1:] += th == 1
    chr[:, :-1] += th == -1
    # to this point the edges were counted, but we need to find sides
    # so now convolve the edge-arrays c.. along the other direction
    # to find the points where edges actually change
    dvu[:, 1:] += convolve2d(cvu, np.array([[1, -1]]), mode="valid")
    dvd[:, 1:] += convolve2d(cvd, np.array([[1, -1]]), mode="valid")
    dhl[1:] += convolve2d(chl, np.array([[1], [-1]]), mode="valid")
    dhr[1:] += convolve2d(chr, np.array([[1], [-1]]), mode="valid")

    # the numpy optimization means we've done this for all tiles, but
    # we only need to count the ones of the actual shape, so mask to
    # the relevant region, only take the values where the convolutions
    # end up with a positive value and sum up
    mask = g == 1
    return (
        (dvd[mask] > 0).sum()
        + (dvu[mask] > 0).sum()
        + (dhl[mask] > 0).sum()
        + (dhr[mask] > 0).sum()
    )


total_price_A = 0
total_price_B = 0
for val in range(1, garden.max() + 1):
    # only find features exactly matching val, need to make boolean mask
    mask = garden == val
    # use scipy label to avoid writing a floodfill algorithm for area detection
    labeled, num_features = label(mask)

    # run through labeled regions
    for i in range(1, num_features + 1):
        # get the current region of interest
        region_mask = labeled == i
        # calculate the area just by summing up everything
        area = region_mask.sum()
        # count fences and sides
        num_fences = count_fences(region_mask)
        num_sides = count_sides(region_mask)
        # add to total price
        total_price_A += area * num_fences
        total_price_B += area * num_sides

print("Total Price A:", total_price_A)
print("Total Price B:", total_price_B)
