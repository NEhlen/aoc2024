import numpy as np
from itertools import combinations

file = "23/input.txt"

with open(file, "r") as f:
    lines = [line.strip() for line in f.readlines()]

connection_dict = dict()

for line in lines:
    from_, to_ = line.split("-")
    if from_ in connection_dict:
        connection_dict[from_].add(to_)
    else:
        connection_dict[from_] = {to_}
    if to_ in connection_dict:
        connection_dict[to_].add(from_)
    else:
        connection_dict[to_] = {from_}

base = list(connection_dict.keys())
connection_matrix = np.zeros((len(base), len(base)), dtype=int)

for key, val in connection_dict.items():
    for v in val:
        connection_matrix[base.index(key), base.index(v)] = 1

# three way loops

three_way = connection_matrix @ connection_matrix @ connection_matrix
connections = np.diag(three_way).sum() // 6


# subset of connection dict with nodes starting with "t"
t_nodes = [key for key in connection_dict.keys() if key.startswith("t")]

triangles = set()
for tn in t_nodes:
    i = base.index(tn)
    neighbors = connection_dict[tn]
    neighbors_i = sorted([base.index(n) for n in neighbors])
    pairs = combinations(neighbors_i, 2)
    for j, k in pairs:
        if connection_matrix[j, k] == 1:
            print(f"Found triangle {tn} - {base[j]} - {base[k]}")
            triangles.add(tuple(sorted((i, j, k))))


print("Number of Triangles with at least 1 node starting with 't':", len(triangles))


# part B
import numpy as np
from itertools import combinations


# Check if a set of nodes forms a clique.
def is_clique(nodes, adj_matrix):

    for u, v in combinations(nodes, 2):
        if adj_matrix[u, v] == 0:
            return False
    return True


# Find all maximal cliques in the graph.
def find_cliques(adj_matrix):

    n = len(adj_matrix)
    all_nodes = set(range(n))
    cliques = []

    # Bron-Kerbosch algorithm
    def bron_kerbosch(r, p, x):
        if not p and not x:
            cliques.append(r)
        while p:
            v = p.pop()
            bron_kerbosch(
                r.union({v}), p.intersection(adj_list[v]), x.intersection(adj_list[v])
            )
            x.add(v)

    # Build adjacency list
    adj_list = {i: set(np.where(adj_matrix[i])[0]) for i in range(n)}
    bron_kerbosch(set(), all_nodes, set())

    return cliques


# Step 1: Find cliques
cliques = find_cliques(connection_matrix)


print("Cliques:", cliques)

maximum_clique = max(cliques, key=len)
print("Maximum clique:", ",".join(sorted([base[i] for i in maximum_clique])))
