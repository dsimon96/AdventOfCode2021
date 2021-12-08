from collections import deque
from typing import Deque, Generator, Iterable, TextIO
import click
import sys


@click.group()
def main(): pass


TIMER_VAL_NEW = 8
TIMER_VAL_RESET = 6


class LanternfishSimulation:
    lanternfish_counts: Deque[int]

    def __init__(self, initial_timers: Iterable[int]) -> None:
        self.lanternfish_counts = deque([0] * (TIMER_VAL_NEW + 1))

        for timer in initial_timers:
            self.lanternfish_counts[timer] += 1

    def step(self) -> None:
        num_expiring_timers = self.lanternfish_counts.popleft()

        self.lanternfish_counts[TIMER_VAL_RESET] += num_expiring_timers
        self.lanternfish_counts.append(num_expiring_timers)

    def get_count(self) -> int:
        return sum(self.lanternfish_counts)


def get_initial_timers(inputs: TextIO) -> Generator[int, None, None]:
    for val in inputs.readline().rstrip().split(','):
        yield int(val)


def do_sim(inputs: TextIO, num_steps: int) -> int:
    sim = LanternfishSimulation(get_initial_timers(inputs))
    for _ in range(num_steps):
        sim.step()

    return sim.get_count()


@main.command()
def part1():
    print(do_sim(sys.stdin, 80))


@main.command()
def part2():
    print(do_sim(sys.stdin, 256))


@main.command()
@click.argument('N', type=int)
def sim(n: int):
    print(do_sim(sys.stdin, n))


if __name__ == '__main__':
    main()
