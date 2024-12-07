file = "07/input.txt"

with open(file, "r") as f:
    lines = [line.strip() for line in f.readlines()]

data = []
for line in lines:
    result, parameters = line.split(":")
    new_point = (int(result), parameters.strip().split())
    data.append(new_point)

operators_A = ("+", "*")
operators_B = ("+", "*", "")


def operate(num: str, rest: list[str], result: int, operators: list[str]):
    if len(rest) == 1:
        for operator in operators:
            new_num = eval(num + operator + rest[0])
            if new_num == result:
                return True
        else:
            return False
    else:
        for operator in operators:
            new_num = eval(num + operator + rest[0])
            if new_num > result:
                return False
            if operate(str(new_num), rest[1:], result, operators):
                return True
        else:
            return False


total_sum_A = 0
for line in data:
    result, params = line
    if operate(params[0], params[1:], result, operators_A):
        total_sum_A += result

print("Total Calibration Result:", total_sum_A)

total_sum_B = 0
for line in data:
    result, params = line
    if operate(params[0], params[1:], result, operators_B):
        total_sum_B += result

print("Total Calibration Result:", total_sum_B)
