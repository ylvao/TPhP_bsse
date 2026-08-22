from math import sqrt

def read_xyz(path):
    lines = open(path).read().splitlines()
    n = int(lines[0].strip())
    atoms = []
    for i, l in enumerate(lines[2:2+n], start=1):
        if not l.strip():
            continue
        p = l.split()
        atoms.append((p[0], float(p[1]), float(p[2]), float(p[3]), i, l))
    return atoms

name = "1b_pme3"
# frag_name = "TPhP"
frag_name = "15h"
frag = read_xyz(f"{frag_name}_{name}_geo.xyz")
full = read_xyz(f"{name}_opt.xyz")
dest = f"{frag_name}_{name}_geo.xyz"
used = set()
matches = []

for fi, (fe, fx, fy, fz, _, fl) in enumerate(frag, start=1):
    best = None
    for j, (ee, x, y, z, _, ll) in enumerate(full, start=1):
        if j in used or ee != fe:
            continue
        d = ((fx - x) ** 2 + (fy - y) ** 2 + (fz - z) ** 2) ** 0.5
        if best is None or d < best[0]:
            best = (d, j, (ee, x, y, z, ll))
    if best is None:
        print("no match", fi, fl)
        break
    d, j, data = best
    if d > 0.01:
        print("warning big d", fi, "->", j, d, fl, "::", data[4])
    used.add(j)
    matches.append((fi, j, d, fl, data[4]))

with open(dest, "w") as f:
    f.write(f"{str(len(matches))}\n\n")
    for m in matches:
        fi, j, d, fl, ll = m
        # print(f"{fi:2d} -> {j:2d} d={d:.6f} | {fl} || {ll}")
        f.write(f"{ll}\n")