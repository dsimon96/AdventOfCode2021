from typing import Generator, TextIO, TypeAlias
import click
import sys


@click.group()
def main(): pass


Point: TypeAlias = tuple[int, int]

FLASH_THRESHOLD = 10

ADJ_DELTAS: list[Point] = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1)
]


def adjacent_points(r: int, c: int, size: int) -> Generator[Point, None, None]:
    for dr, dc in ADJ_DELTAS:
        adj_r = r + dr
        adj_c = c + dc

        if 0 <= adj_r and adj_r < size and 0 <= adj_c and adj_c < size:
            yield (adj_r, adj_c)


class OctopusGrid:
    _levels: list[list[int]]
    size: int
    step_count: int = 0

    def __init__(self, levels: list[list[int]]) -> None:
        self._levels = levels
        self.size = len(levels)

    def __str__(self) -> str:
        return '\n'.join(''.join(str(v) for v in row) for row in self._levels)

    def _incr_point(
        self,
        r: int,
        c: int,
        flash_q: list[Point],
        flash_set: set[Point]
    ):
        self._levels[r][c] += 1
        if (self._levels[r][c] >= FLASH_THRESHOLD and (r, c) not in flash_set):
            flash_set.add((r, c))
            flash_q.append((r, c))

    def _incr_all(self, flash_q: list[Point], flash_set: set[Point]):
        for r in range(self.size):
            for c in range(self.size):
                self._incr_point(r, c, flash_q, flash_set)

    def _do_flash(
        self,
        r: int,
        c: int,
        flash_q: list[Point],
        flash_set: set[Point]
    ):
        for adj_r, adj_c in adjacent_points(r, c, self.size):
            self._incr_point(adj_r, adj_c, flash_q, flash_set)

    def step(self) -> int:
        flash_q: list[Point] = []
        flash_set: set[Point] = set()
        self._incr_all(flash_q, flash_set)

        while len(flash_q) > 0:
            r, c = flash_q.pop()
            self._do_flash(r, c, flash_q, flash_set)

        for (r, c) in flash_set:
            self._levels[r][c] = 0

        self.step_count += 1
        return len(flash_set)


def get_grid(inp: TextIO) -> OctopusGrid:
    return OctopusGrid(list(list(int(v) for v in line.rstrip())
                            for line in inp))


@main.command()
@click.option('--steps', default=100, type=int)
@click.option('-v', is_flag=True)
def part1(steps: int, v: bool):
    grid = get_grid(sys.stdin)
    if v:
        print(grid)
        print()

    total_flashes = 0
    for _ in range(steps):
        total_flashes += grid.step()

        if v:
            print(grid)
            print()

    print(total_flashes)


@main.command()
@click.option('-v', is_flag=True)
def part2(v: bool):
    grid = get_grid(sys.stdin)
    if v:
        print(grid)
        print()

    octopus_count = grid.size ** 2
    while octopus_count != grid.step():
        if v:
            print(grid)
            print()

    print(grid.step_count)


if __name__ == '__main__':
    main()
