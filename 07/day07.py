file = "07/input.txt"

with open(file, "r") as f:
    lines = [line.strip() for line in f.readlines()]

data = []
for line in lines:
    result, parameters = line.split(":")
    new_point = (int(result), parameters.strip().split())
    data.append(new_point)


# recursively run through all possible operator-combinations
# break if num is already bigger than result before whole list exhausted
# break if one operator combination is True already


def operate_A(num: int, i: int, params: list[str], result: int):
    # if the integer to check has reached the end of the list, compare the result
    if i >= len(params):
        return num == result
    # if the number is already bigger than the result before reaching
    # the end of the list return False
    elif num > result:
        return False
    # else check multiplication or addition, return True if one of them is True
    else:
        if operate_A(num + int(params[i]), i + 1, params, result):
            return True
        elif operate_A(num * int(params[i]), i + 1, params, result):
            return True
        else:
            return False


def operate_B(num, i, params, result):
    # if the integer to check has reached the end of the list, compare the result
    if i >= len(params):
        return num == result
    # if the number is already bigger than the result before reaching
    # the end of the list return False
    elif num > result:
        return False
    # else check multiplication, addition or combination,
    # return True if one of them is True
    else:
        if operate_B(num + int(params[i]), i + 1, params, result):
            return True
        elif operate_B(num * int(params[i]), i + 1, params, result):
            return True
        elif operate_B(int(str(num) + params[i]), i + 1, params, result):
            return True
        else:
            return False


total_sum_A = 0
for line in data:
    result, params = line
    if operate_A(int(params[0]), 1, params, result):
        total_sum_A += result

print("Total Calibration Result:", total_sum_A)

total_sum_B = 0
for line in data:
    result, params = line
    if operate_B(int(params[0]), 1, params, result):
        total_sum_B += result

print("Total Calibration Result:", total_sum_B)
