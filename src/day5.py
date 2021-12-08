from typing import Generator, Iterable, TextIO
import click
import sys
from collections import defaultdict
from dataclasses import dataclass


@click.group()
def main(): pass


@dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int


def bidirectional_range_inclusive(
    start: int, end: int
) -> Generator[int, None, None]:
    step = 1 if end > start else -1
    for i in range(start, end+step, step):
        yield i


@dataclass
class Line:
    start: Point
    end: Point

    def is_horizontal(self) -> bool:
        return self.start.y == self.end.y

    def is_vertical(self) -> bool:
        return self.start.x == self.end.x

    def points(self) -> Generator[Point, None, None]:
        if self.is_horizontal():
            for x in bidirectional_range_inclusive(self.start.x, self.end.x):
                yield Point(x, self.start.y)
        elif self.is_vertical():
            for y in bidirectional_range_inclusive(self.start.y, self.end.y):
                yield Point(self.start.x, y)
        else:
            for x, y in zip(
                    bidirectional_range_inclusive(self.start.x, self.end.x),
                    bidirectional_range_inclusive(self.start.y, self.end.y)):
                yield Point(x, y)


def parse_point(s: str) -> Point:
    x_str, y_str = s.split(',')
    return Point(x=int(x_str), y=int(y_str))


def get_lines(input: TextIO):
    for line_str in input:
        tokens = line_str.split()
        yield Line(start=parse_point(tokens[0]), end=parse_point(tokens[2]))


def is_horizontal_or_vertical(line: Line):
    return line.start.x == line.end.x or line.start.y == line.end.y


def count_overlap_points(
    lines: Iterable[Line], *, exclude_diagonal: bool
) -> int:
    number_of_lines: dict[Point, int] = defaultdict(int)
    for line in lines:
        if exclude_diagonal and not is_horizontal_or_vertical(line):
            continue

        for point in line.points():
            number_of_lines[point] += 1

    return sum(1 for _, n in number_of_lines.items() if n > 1)


@main.command()
def part1():
    print(count_overlap_points(get_lines(sys.stdin), exclude_diagonal=True))


@main.command()
def part2():
    print(count_overlap_points(get_lines(sys.stdin), exclude_diagonal=False))


if __name__ == '__main__':
    main()
