from collections import defaultdict
from itertools import pairwise
from typing import TextIO, TypeAlias
import click
import sys

Rules: TypeAlias = dict[str, str]


@click.group()
def main(): pass


class PolymerString:
    def __init__(self, s: str):
        self.elem_counts: dict[str, int] = defaultdict(int)
        self.pair_counts: dict[str, int] = defaultdict(int)

        for c in s:
            self.elem_counts[c] += 1

        for a, b in pairwise(s):
            self.pair_counts[a+b] += 1


def get_input(inp: TextIO) -> tuple[PolymerString, Rules]:
    s = PolymerString(inp.readline().rstrip())
    inp.readline()

    rules: Rules = Rules()
    for line in inp:
        in_pair, out = line.rstrip().split(' -> ')
        rules[in_pair] = out

    return (s, rules)


def step(s: PolymerString, rules: Rules):
    new_pair_counts: dict[str, int] = s.pair_counts.copy()
    for pair, count in s.pair_counts.items():
        if (out := rules.get(pair)) is None:
            continue

        new_pair_counts[pair] -= count
        new_pair_counts[pair[0] + out] += count
        new_pair_counts[out + pair[1]] += count
        s.elem_counts[out] += count

    s.pair_counts = new_pair_counts


def do_sim(steps: int):
    s, rules = get_input(sys.stdin)
    for _ in range(steps):
        step(s, rules)
    print(max(s.elem_counts.values()) - min(s.elem_counts.values()))


@main.command()
@click.option('--steps', type=int, required=True)
def sim(steps: int):
    do_sim(steps)


@main.command()
def part1():
    do_sim(10)


@main.command()
def part2():
    do_sim(40)


if __name__ == '__main__':
    main()
