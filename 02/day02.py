import numpy as np

filename = "02/input.txt"

# load data
with open(filename, "r") as f:
    lines = f.readlines()


data = []
for line in lines:
    data.append(np.array([int(num) for num in line.split()]))


def check_report(report: np.ndarray) -> tuple[bool, np.ndarray]:
    diffs = report[1:] - report[:-1]
    monotonic = all(diffs < 0) or all(diffs > 0)
    within_bounds = all(np.abs(diffs) >= 1) and all(np.abs(diffs) <= 3)
    return monotonic and within_bounds, diffs


def check_report_dampened(report: np.ndarray) -> bool:
    for i in range(len(report)):
        result, _ = check_report(np.concatenate([report[:i], report[(i + 1) :]]))
        if result:
            return result
    return False


# part A
print("Safe reports:", np.sum([check_report(report)[0] for report in data]))


# part B
print(
    "Safe reports with dampener:",
    np.sum([check_report_dampened(report) for report in data]),
)
