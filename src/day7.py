from typing import Generator, TextIO
import click
import statistics
import sys


@click.group()
def main(): pass


def get_inputs(inputs: TextIO) -> Generator[int, None, None]:
    for s in inputs.read().rstrip().split(','):
        yield(int(s))


@main.command()
def part1():
    vals = list(get_inputs(sys.stdin))
    median = statistics.median_low(vals)
    print(sum(abs(val - median) for val in vals))


def fuel_cost(x: int, y: int) -> int:
    dist = abs(x - y)
    return dist * (dist + 1) // 2


@main.command()
def part2():
    vals = list(get_inputs(sys.stdin))
    lb = min(vals)
    ub = max(vals)

    print(min(sum(fuel_cost(val, dest) for val in vals)
          for dest in range(lb, ub+1)))


if __name__ == '__main__':
    main()
