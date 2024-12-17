from collections import deque

file = "17/input.txt"

with open(file, "r") as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

initial_state = {}
for line in lines:
    key, val = line.split(":")
    if key.startswith("Reg"):
        initial_state[key] = int(val)
    else:
        initial_state[key] = val.strip()


def combo_op(operand: int):
    if operand == 4:
        return regA
    elif operand == 5:
        return regB
    elif operand == 6:
        return regC
    elif operand == 7:
        raise ValueError("Combo Operand with value of 7 is forbidden")
    else:
        return operand


# division
def adv(operand: int):
    global regA
    res = regA // 2 ** combo_op(operand)
    regA = int(res)
    return res


# bitwise xor
def bxl(operand: int):
    global regB
    res = regB ^ operand
    regB = res
    return res


def bst(operand: int):
    global regB
    res = combo_op(operand) % 8
    regB = res
    return res


# jump not zero
def jnz(operand: int):
    global instruction_pointer
    if regA == 0:
        return False
    else:
        instruction_pointer = operand
        return True


# bitwise xor regb regc
def bxc(operand: int):
    global regB, regC
    res = regB ^ regC
    regB = res


# output
def out(operand: int):
    global console_out
    res = combo_op(operand) % 8
    console_out.append(str(res))
    return res


# division to regB
def bdv(operand: int):
    global regA, regB
    res = regA // 2 ** combo_op(operand)
    regB = int(res)
    return res


# division to regB
def cdv(operand: int):
    global regA, regC
    res = regA // 2 ** combo_op(operand)
    regC = int(res)
    return res


instructions = {0: adv, 1: bxl, 2: bst, 3: jnz, 4: bxc, 5: out, 6: bdv, 7: cdv}


def run(registers: tuple[int], program: str) -> tuple[str, tuple[int]]:
    global regA, regB, regC, instruction_pointer, console_out
    regA = registers[0]
    regB = registers[1]
    regC = registers[2]

    instruction_pointer = 0

    console_out = []

    program = program
    program = [int(num) for num in program.split(",")]
    running = True

    while running:
        if instruction_pointer >= len(program):
            running = False
            break
        instruction = program[instruction_pointer]
        operand = program[instruction_pointer + 1]
        ret = instructions[instruction](operand)
        if instruction != 3:
            instruction_pointer += 2
        elif not ret:
            instruction_pointer += 2

    return console_out, (regA, regB, regC)


result, registers = run(
    (
        initial_state["Register A"],
        initial_state["Register B"],
        initial_state["Register C"],
    ),
    initial_state["Program"],
)

print("Result A:", ",".join(result))


# Part B
# the only time the value in regA is changed is when
# adv is called. This happens only once with the 0,3 combo in the program
# there is also only one jump condition right at the end of the program
# that jumps it back to the beginning, keeping the program looping
# until regA is 0. This means regA is divided by 8 once each loop
# so going from the right to left, once we've found one regA that reproduces
# the last i values of the program, we can multiply regA times 8 and only check the
# next 8 numbers to look for the next value of regA to reproduce the last i+1 numbers
# of the program
# because there might be dead ends, we need to add all the potentials to a set
def check(regA, required):
    regA *= 8
    next_iteration = []
    for n in range(8):
        output, _ = run(
            (regA + n, initial_state["Register B"], initial_state["Register C"]),
            initial_state["Program"],
        )
        if output == list(required):
            next_iteration.append(regA + n)
    return next_iteration


reg_a_potentials = {0}
required_match = deque([])
# compare to program from right to left
prog = initial_state["Program"].strip().split(",")[::-1]
for val in prog:
    required_match.appendleft(val)
    reg_a_potentials = {
        a for reg_a in reg_a_potentials for a in check(reg_a, required_match)
    }

print("Min RegA:", min(reg_a_potentials))
