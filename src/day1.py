import itertools
import sys
from collections import deque
from typing import Deque, Generator, Iterable
import click


@click.group()
def main():
    pass


def get_input() -> Generator[int, None, None]:
    for line in sys.stdin:
        yield int(line)


def count_increases(inputs: Iterable[int]) -> int:
    return sum(1 for prev, cur in itertools.pairwise(inputs) if cur > prev)


@main.command()
def part1():
    print(count_increases(get_input()))


def get_three_sums(inputs: Iterable[int]) -> Generator[int, None, None]:
    window: Deque[int] = deque()
    for number in inputs:
        window.append(number)
        if len(window) < 3:
            continue
        elif len(window) > 3:
            window.popleft()
        yield sum(window)


@main.command()
def part2():
    print(count_increases(get_three_sums(get_input())))


if __name__ == "__main__":
    main()
