from dataclasses import dataclass, replace
from typing import Sequence, TextIO, TypeAlias
import click
import sys


@click.group()
def main(): pass


@dataclass(frozen=True)
class Point:
    x: int
    y: int


Paper: TypeAlias = set[Point]


@dataclass
class Fold:
    axis: str
    value: int


def get_input(inp: TextIO) -> tuple[Paper, Sequence[Fold]]:
    paper = Paper()
    for line in inp:
        line = line.rstrip()
        if not line:
            break

        x, y = line.split(',')
        paper.add(Point(int(x), int(y)))

    fold_seq: Sequence[Fold] = []
    for line in inp:
        fold_spec = line.split()[-1]
        axis, val = fold_spec.split('=')
        fold_seq.append(Fold(axis, int(val)))

    return (paper, fold_seq)


def apply_fold(paper: Paper, fold: Fold) -> Paper:
    unaffected = {p for p in paper if getattr(p, fold.axis) < fold.value}
    affected = {p for p in paper if getattr(p, fold.axis) > fold.value}
    folded = {replace(p, **{fold.axis: 2 * fold.value - getattr(p, fold.axis)})
              for p in affected}

    return unaffected | folded


@main.command()
def part1():
    paper, fold_seq = get_input(sys.stdin)

    paper = apply_fold(paper, fold_seq[0])
    print(len(paper))


def pretty_print(paper: Paper):
    max_x = max(p.x for p in paper)
    max_y = max(p.y for p in paper)

    res = ""
    for y in range(max_y+1):
        for x in range(max_x+1):
            res += "#" if Point(x, y) in paper else "."
        res += "\n"
    print(res)


@main.command()
def part2():
    paper, fold_seq = get_input(sys.stdin)
    for fold in fold_seq:
        paper = apply_fold(paper, fold)

    pretty_print(paper)


if __name__ == '__main__':
    main()
