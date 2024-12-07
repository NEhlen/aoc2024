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
    second_num = rest[0]
    new_nums = [eval(num + operator + second_num) for operator in operators]
    if len(rest) == 1:
        return any([new_num == result for new_num in new_nums])
    else:
        return any(
            [operate(str(new_num), rest[1:], result, operators) for new_num in new_nums]
        )


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
