from collections import defaultdict
from functools import cache
from typing import Generator, TextIO, TypeAlias
import click
import sys


@click.group()
def main(): pass


Map: TypeAlias = dict[str, set[str]]


def get_map(inp: TextIO) -> Map:
    res: Map = defaultdict(set)
    for line in inp:
        start, end = line.rstrip().split('-')
        res[start].add(end)
        res[end].add(start)
    return res


def is_small_cave(name: str) -> bool:
    return name[0].islower()


def count_paths(map: Map, allow_revisit: bool):
    @cache
    def count_paths_recursive(
        name: str,
        small_visited: frozenset[str],
        revisited: bool
    ) -> int:
        if name == 'end':
            return 1
        elif name == 'start' and revisited:
            return 0

        if is_small_cave(name):
            small_visited |= set((name,))

        total = sum(count_paths_recursive(succ, small_visited, revisited)
                    for succ in map[name] if succ not in small_visited)

        if allow_revisit and not revisited:
            total += sum(count_paths_recursive(succ, small_visited, True)
                         for succ in map[name] & small_visited)

        return total

    return count_paths_recursive('start', frozenset(), False)


@main.command()
def part1():
    print(count_paths(get_map(sys.stdin), allow_revisit=False))


@main.command()
def part2():
    print(count_paths(get_map(sys.stdin), allow_revisit=True))


if __name__ == '__main__':
    main()
