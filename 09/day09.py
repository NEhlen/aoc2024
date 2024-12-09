import numpy as np

file = "09/input.txt"

with open(file, "r") as f:
    diskmap = f.read().strip()


def diskmap_to_blocks(diskmap: str) -> list[int]:
    blocks = []
    for pos, (file, freespace) in enumerate(zip(diskmap[0::2], diskmap[1::2])):
        blocks.append([pos] * int(file))
        blocks.append(["."] * int(freespace))
    if (len(diskmap) % 2) != 0:
        blocks.append([pos + 1] * int(diskmap[-1]))
    return blocks


expanded = diskmap_to_blocks(diskmap)
expanded_A = [e for ex in expanded for e in ex]

reorder = True
while reorder:
    to_reorder = expanded_A[-1]
    if "." not in expanded_A:
        break
    expanded_A = expanded_A[:-1]
    if to_reorder != ".":

        insert_index = expanded_A.index(".")
        expanded_A = (
            expanded_A[:insert_index] + [to_reorder] + expanded_A[(insert_index + 1) :]
        )


def get_checksum(blocks: str) -> int:
    return sum([num * pos for pos, num in enumerate(blocks) if num != "."])


print("Checksum A:", get_checksum(expanded_A))

disk_copy = expanded.copy()
disk_id = max([n for n in expanded_A if type(n) == int])
for did in list(range(1, disk_id + 1))[::-1]:
    idx = next(
        (
            index
            for index, sublist in enumerate(disk_copy)
            if sublist and sublist[0] == did
        ),
        None,
    )
    to_reorder = disk_copy[idx]
    for insert_idx, block in enumerate(disk_copy):
        if "." in block and insert_idx < idx:
            diff = len(block) - len(to_reorder)
            if diff >= 0:
                disk_copy[insert_idx] = to_reorder

                disk_copy.pop(idx)
                disk_copy.insert(idx, ["."] * len(to_reorder))
                if diff > 0:
                    disk_copy.insert(
                        insert_idx + 1, ["."] * (len(block) - len(to_reorder))
                    )
                break

expanded_B = [e for ex in disk_copy for e in ex]

print("Checksum B:", get_checksum(expanded_B))
