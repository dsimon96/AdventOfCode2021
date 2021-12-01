import itertools
import sys
from collections import deque
from typing import Deque, Generator
import click


@click.group()
def main():
    pass


def get_input() -> Generator[int, None, None]:
    for line in sys.stdin.readlines():
        yield int(line)


def count_increases(inputs: Generator[int, None, None]) -> int:
    return sum(1 for prev, cur in itertools.pairwise(inputs) if cur > prev)


@main.command()
def part1():
    print(count_increases(get_input()))


def get_three_sums() -> Generator[int, None, None]:
    window: Deque[int] = deque()
    for number in get_input():
        window.append(number)
        if len(window) < 3:
            continue
        elif len(window) > 3:
            window.popleft()
        yield sum(window)


@main.command()
def part2():
    print(count_increases(get_three_sums()))


if __name__ == "__main__":
    main()
