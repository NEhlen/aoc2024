import numpy as np
import re

file = "03/input.txt"

with open(file, "r") as f:
    memory = f.read()

instructions = re.findall("mul\\([0-9]{1,3},[0-9]{1,3}\\)", memory)


def parse_instruction(instruction: str):
    numbers = instruction[4:-1]
    numA, numB = numbers.split(",")
    numA, numB = int(numA), int(numB)
    return numA * numB


print("total A:", sum([parse_instruction(inst) for inst in instructions]))


instructions_B = re.findall(
    "(don't\\(\\)|do\\(\\)|mul\\([0-9]{1,3},[0-9]{1,3}\\))", memory
)


def parse_instruction_B(instruction: str):
    if "do" not in instruction:
        numbers = instruction[4:-1]
        numA, numB = numbers.split(",")
        numA, numB = int(numA), int(numB)
        return numA * numB
    else:
        if instruction == "don't()":
            return False
        else:
            return True


def total_B(instructions):
    total_sum = 0
    add_ = True
    for instruction in instructions:
        if type(instruction) is int:
            if add_:
                total_sum += instruction
        else:
            add_ = instruction
    return total_sum


parsed_instructions_B = [parse_instruction_B(inst) for inst in instructions_B]


print("total B:", total_B(parsed_instructions_B))
