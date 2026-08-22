#!/usr/bin/env python3
"""Create a basis XYZ file by marking atoms absent from a fragment with ':' .

Example marked line:
  P          -1.520...  ->  P :        -1.520...
"""

from __future__ import annotations

import argparse
import math
import re
from dataclasses import dataclass
from typing import List, Sequence


ATOM_RE = re.compile(r"^(\s*)([A-Za-z]{1,2})(\s+)(.*\S)\s*$")
ligand = "pme3"

@dataclass
class Atom:
    element: str
    x: float
    y: float
    z: float
    raw_line: str


@dataclass
class XYZ:
    count_line: str
    comment_line: str
    atoms: List[Atom]


def parse_xyz(path: str) -> XYZ:
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    if len(lines) < 2:
        raise ValueError(f"{path} does not look like an XYZ file (missing header lines)")

    try:
        n_atoms = int(lines[0].strip())
    except ValueError as exc:
        raise ValueError(f"Invalid atom count in {path!r}: {lines[0]!r}") from exc

    atom_lines = lines[2 : 2 + n_atoms]
    if len(atom_lines) != n_atoms:
        raise ValueError(
            f"{path} declares {n_atoms} atoms but only {len(atom_lines)} coordinate lines were found"
        )

    atoms: List[Atom] = []
    for line in atom_lines:
        parts = line.split()
        if len(parts) < 4:
            raise ValueError(f"Invalid coordinate line in {path!r}: {line!r}")
        atoms.append(
            Atom(
                element=parts[0],
                x=float(parts[1]),
                y=float(parts[2]),
                z=float(parts[3]),
                raw_line=line,
            )
        )

    return XYZ(count_line=lines[0], comment_line=lines[1], atoms=atoms)


def distance(a: Atom, b: Atom) -> float:
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2)


def match_fragment_to_full(full_atoms: Sequence[Atom], frag_atoms: Sequence[Atom], warn_threshold: float) -> set[int]:
    """Return the indices in full_atoms that match fragment atoms (one-to-one)."""
    used: set[int] = set()

    for i, frag in enumerate(frag_atoms, start=1):
        best_idx = None
        best_dist = None

        for j, full in enumerate(full_atoms):
            if j in used or full.element != frag.element:
                continue
            d = distance(full, frag)
            if best_dist is None or d < best_dist:
                best_dist = d
                best_idx = j

        if best_idx is None or best_dist is None:
            raise RuntimeError(
                f"Could not match fragment atom {i} ({frag.element} {frag.x} {frag.y} {frag.z}) to the full structure"
            )

        if best_dist > warn_threshold:
            print(
                f"WARNING: fragment atom {i} matched with distance {best_dist:.6f} (> {warn_threshold:g})"
            )

        used.add(best_idx)

    return used


def add_colon_marker(atom_line: str) -> str:
    """Insert ' :' after the element token, preserving overall spacing style."""
    m = ATOM_RE.match(atom_line)
    if not m:
        return atom_line

    lead, element, gap, rest = m.groups()
    if len(gap) >= 2:
        new_gap = " :" + gap[2:]
    else:
        new_gap = " :"

    return f"{lead}{element}{new_gap}{rest}"


def write_basis(full: XYZ, present_indices: set[int], output_path: str) -> None:
    out_lines = [full.count_line, full.comment_line]

    for idx, atom in enumerate(full.atoms):
        if idx in present_indices:
            out_lines.append(atom.raw_line)
        else:
            out_lines.append(add_colon_marker(atom.raw_line))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Build a basis XYZ file from a full XYZ and a fragment XYZ. "
            "Atoms absent from fragment are marked with ' :'."
        )
    )
    parser.add_argument("--full", default=f"1b_{ligand}_opt.xyz", help="Full XYZ file")
    parser.add_argument(
        "--fragments",
        nargs="+",
        default=[f"15h_1b_{ligand}_geo.xyz", f"TPhP_1b_{ligand}_geo.xyz"],
        help="One or more fragment XYZ files",
    )
    parser.add_argument(
        "--outputs",
        nargs="+",
        default=[f"15h_1b_{ligand}_geo_basis.xyz", f"TPhP_1b_{ligand}_geo_basis.xyz"],
        help="One output file per fragment",
    )
    parser.add_argument(
        "--warn-threshold",
        type=float,
        default=0.01,
        help="Warn if matched atom distance exceeds this value (Angstrom)",
    )
    parser.add_argument(
        "--pair-complement",
        action=argparse.BooleanOptionalAction,
        default=True,
        help=(
            "When two fragment/output pairs are provided, build the second output as the "
            "exact complement of the first fragment match."
        ),
    )
    args = parser.parse_args()

    full = parse_xyz(args.full)

    if len(args.fragments) != len(args.outputs):
        raise ValueError(
            "--fragments and --outputs must have the same number of entries "
            f"(got {len(args.fragments)} fragments and {len(args.outputs)} outputs)"
        )

    # Optional mode for paired fragments where the second fragment is intended to be
    # the opposite mask but is not guaranteed to be in the same coordinate frame.
    if args.pair_complement:
        if len(args.fragments) != 2:
            raise ValueError("--pair-complement requires exactly 2 fragments")

        frag1 = parse_xyz(args.fragments[0])
        present1 = match_fragment_to_full(full.atoms, frag1.atoms, args.warn_threshold)
        write_basis(full, present1, args.outputs[0])
        print(
            f"Wrote {args.outputs[0]}: total atoms={len(full.atoms)}, "
            f"present in fragment={len(present1)}, marked missing={len(full.atoms) - len(present1)}"
        )

        all_indices = set(range(len(full.atoms)))
        present2 = all_indices - present1
        write_basis(full, present2, args.outputs[1])
        print(
            f"Wrote {args.outputs[1]}: total atoms={len(full.atoms)}, "
            f"present in fragment={len(present2)}, marked missing={len(full.atoms) - len(present2)}"
        )

        # Best-effort consistency check against second fragment atom count.
        frag2 = parse_xyz(args.fragments[1])
        if len(frag2.atoms) != len(present2):
            print(
                "WARNING: second fragment atom count does not match computed complement "
                f"({len(frag2.atoms)} vs {len(present2)})."
            )
        return

    for fragment_path, output_path in zip(args.fragments, args.outputs):
        fragment = parse_xyz(fragment_path)
        present = match_fragment_to_full(full.atoms, fragment.atoms, args.warn_threshold)
        write_basis(full, present, output_path)

        print(
            f"Wrote {output_path}: total atoms={len(full.atoms)}, "
            f"present in fragment={len(present)}, marked missing={len(full.atoms) - len(present)}"
        )


if __name__ == "__main__":
    main()
