from heapq import heappush, heappop
from typing import Generator, Optional, TextIO, TypeAlias
import click
import sys

Grid: TypeAlias = list[list[int]]


@click.group()
def main(): pass


def get_grid(inp: TextIO) -> Grid:
    res: Grid = []
    for line in inp:
        row: list[int] = []
        for c in line.rstrip():
            row.append(int(c))
        res.append(row)
    return res


def adjacent(
    r: int,
    c: int,
    height: int,
    width: int
) -> Generator[tuple[int, int], None, None]:
    if r > 0:
        yield (r-1, c)
    if c > 0:
        yield (r, c-1)
    if r < height-1:
        yield (r+1, c)
    if c < width-1:
        yield (r, c+1)


def get_min_risk(grid: Grid) -> int:
    height = len(grid)
    width = len(grid[0])

    node_q: list[tuple[int, int, int]] = []
    visited: set[tuple[int, int]] = set()
    min_cost: dict[tuple[int, int], Optional[int]] = {}

    heappush(node_q, (0, 0, 0))
    visited.add((0, 0))
    while True:
        cost, r, c = heappop(node_q)
        visited.add((r, c))
        if r == height-1 and c == width-1:
            return cost

        for (r, c) in adjacent(r, c, height, width):
            if (r, c) in visited:
                continue

            new_cost = cost + grid[r][c]
            if ((prev_cost := min_cost.get((r, c))) is None
                    or new_cost < prev_cost):
                heappush(node_q, (new_cost, r, c))
                min_cost[(r, c)] = new_cost


@ main.command()
def part1():
    grid = get_grid(sys.stdin)

    print(get_min_risk(grid))


def incr_wrap_1_idx(v: int) -> int:
    res = v + 1
    return res if res < 10 else res - 9


def get_extended_grid(inp: TextIO) -> Grid:
    grid = get_grid(inp)
    orig_width = len(grid[0])

    for row in grid:
        for c in range(orig_width, 5*orig_width):
            row.append(incr_wrap_1_idx(row[c-orig_width]))

    orig_height = len(grid)
    for r in range(orig_height, 5*orig_height):
        grid.append([incr_wrap_1_idx(v) for v in grid[r-orig_height]])

    return grid


@ main.command()
def part2():
    grid = get_extended_grid(sys.stdin)
    print(get_min_risk(grid))


if __name__ == '__main__':
    main()
