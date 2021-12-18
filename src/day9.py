from dataclasses import dataclass, replace
from typing import Generator, TextIO
from heapq import nlargest
from math import prod
import click
import sys

WALL_HEIGHT = 9


@click.group()
def main(): pass


@dataclass
class Dimensions:
    h: int
    w: int


@dataclass(frozen=True)
class Point:
    r: int
    c: int


class Heightmap:
    _vals: list[list[int]]
    dims: Dimensions

    def __init__(self, vals: list[list[int]]) -> None:
        self._vals = vals
        self.dims = Dimensions(h=len(vals), w=len(vals[0]))

    def __getitem__(self, point: Point) -> int:
        return self._vals[point.r][point.c]


def get_heightmap(inp: TextIO) -> Heightmap:
    return Heightmap(list(list(int(v) for v in line.rstrip()) for line in inp))


def adjacent_points(
    dims: Dimensions,
    point: Point
) -> Generator[Point, None, None]:
    if point.r > 0:
        yield replace(point, r=point.r-1)
    if point.c > 0:
        yield replace(point, c=point.c-1)
    if point.r < dims.h-1:
        yield replace(point, r=point.r+1)
    if point.c < dims.w-1:
        yield replace(point, c=point.c+1)


def is_low_point(heightmap: Heightmap, point: Point) -> bool:
    return all(heightmap[point] < heightmap[adj_point]
               for adj_point in adjacent_points(heightmap.dims, point))


def get_low_points(heightmap: Heightmap) -> Generator[Point, None, None]:
    for r in range(heightmap.dims.h):
        for c in range(heightmap.dims.w):
            point = Point(r, c)
            if is_low_point(heightmap, point):
                yield point


def risk_level(heightmap: Heightmap, point: Point) -> int:
    return heightmap[point] + 1


@main.command()
def part1():
    heightmap = get_heightmap(sys.stdin)
    print(sum(risk_level(heightmap, point)
          for point in get_low_points(heightmap)))


def get_basin_size(heightmap: Heightmap, low_point: Point) -> int:
    visited: set[Point] = {low_point}
    to_visit: list[Point] = [low_point]
    size = 0

    while len(to_visit) > 0:
        point = to_visit.pop()
        size += 1

        for point in adjacent_points(heightmap.dims, point):
            if heightmap[point] < WALL_HEIGHT and point not in visited:
                visited.add(point)
                to_visit.append(point)

    return size


def get_basin_sizes(heightmap: Heightmap) -> Generator[int, None, None]:
    for point in get_low_points(heightmap):
        yield get_basin_size(heightmap, point)


@main.command()
def part2():
    print(prod(nlargest(3, get_basin_sizes(get_heightmap(sys.stdin)))))


if __name__ == '__main__':
    main()
