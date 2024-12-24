import numpy as np

file = "24/input.txt"
with open(file, "r") as f:
    lines = f.read()
    starting_bits, gates = lines.split("\n\n")
    starting_bits = [line.strip() for line in starting_bits.strip().split("\n")]
    starting_bits = dict(
        [(line.split(": ")[0], int(line.split(": ")[1])) for line in starting_bits]
    )

    gates = [line.strip() for line in gates.strip().split("\n")]
    gates = [line.split(" -> ") for line in gates]
    gates = dict([(line[1], line[0]) for line in gates])


def get_value(bit):
    if bit in starting_bits:
        return starting_bits[bit]
    else:
        gate = gates[bit]
        if "AND" in gate:
            a, b = gate.split(" AND ")
            val_a = get_value(a)
            val_b = get_value(b)
            return val_a & val_b
        elif "XOR" in gate:
            a, b = gate.split(" XOR ")
            val_a = get_value(a)
            val_b = get_value(b)
            return val_a ^ val_b
        elif "OR" in gate:
            a, b = gate.split(" OR ")
            val_a = get_value(a)
            val_b = get_value(b)
            return val_a | val_b
        else:
            return get_value(gate)


z_gates = sorted([gate for gate in gates.keys() if gate.startswith("z")])[::-1]
output_values = [get_value(z) for z in z_gates]
output_bits = [str(val) for val in output_values]
print("Decimal Output A:", int("".join(output_bits), 2))


# part B
input_x = sorted([gate for gate in starting_bits.keys() if gate.startswith("x")])[::-1]
input_x = "".join([str(starting_bits[gate]) for gate in input_x])
input_y = sorted([gate for gate in starting_bits.keys() if gate.startswith("y")])[::-1]
input_y = "".join([str(starting_bits[gate]) for gate in input_y])

output_z = sorted([gate for gate in gates.keys() if gate.startswith("z")])[::-1]
output_z_real = bin(int("".join([str(get_value(z)) for z in z_gates]), 2))

input_x_dec = int(input_x, 2)
input_y_dec = int(input_y, 2)

output_z_correct = bin(input_x_dec + input_y_dec)

for i, (c1, c2) in enumerate(zip(output_z_correct[::-1], (output_z_real)[::-1])):
    if c1 != c2:
        print("incorrect bit:", i)

# z12 jsb AND njf -> z12 it needs to be an XOR
# swap z12 with djg
# z19 x19 AND y19 -> z19 needs XOR, swap with kbs
# z24 swap hjm with mcq
# z37 swap spj dsd
# inspect visually the input after finding wrong bits and then swap
temp = gates["djg"]
gates["djg"] = gates["z12"]
gates["z12"] = temp

temp = gates["sbg"]
gates["sbg"] = gates["z19"]
gates["z19"] = temp

temp = gates["hjm"]
gates["hjm"] = gates["mcq"]
gates["mcq"] = temp

temp = gates["z37"]
gates["z37"] = gates["dsd"]
gates["dsd"] = temp

output = sorted(["djg", "z12", "sbg", "z19", "hjm", "mcq", "z37", "dsd"])
print("Answer B", ",".join(output))
