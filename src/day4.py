import sys
from itertools import chain
from collections import defaultdict
from typing import Generator, Iterable, Optional, Sequence
import click

NUM_ROWS: int = 5


@click.group()
def main(): pass


def _make_marks(num_boards: int) -> list[list[list[bool]]]:
    marks: list[list[list[bool]]] = []
    for _ in range(num_boards):
        board_marks: list[list[bool]] = []
        for _ in range(NUM_ROWS):
            board_marks.append([False] * NUM_ROWS)
        marks.append(board_marks)

    return marks


def _make_rev_index(
    boards: list[list[list[int]]]
) -> dict[int, list[tuple[int, int, int]]]:
    res: dict[int, list[tuple[int, int, int]]] = defaultdict(list)
    for i, board in enumerate(boards):
        for j, row in enumerate(board):
            for k, val in enumerate(row):
                res[val].append((i, j, k))

    return res


class BingoBoards:
    _boards: list[list[list[int]]]
    _marks: list[list[list[bool]]]
    _rev_index: dict[int, list[tuple[int, int, int]]]
    _finished: list[bool]

    def __init__(self, boards: Iterable[list[list[int]]]) -> None:
        self._boards = list(boards)
        self._marks = _make_marks(len(self._boards))
        self._rev_index = _make_rev_index(self._boards)
        self._finished = [False] * len(self._boards)

    def _is_bingo_at(self, b: int, r: int, c: int) -> bool:
        return (all(self._marks[b][r][i]
                    for i in range(NUM_ROWS)) or
                all(self._marks[b][i][c]
                    for i in range(NUM_ROWS)))

    def mark_number(self, number: int) -> Sequence[int]:
        """
        Marks the specified value on all non-completed boards.

        Return the indices of all boards that are completed as a result of
        marking the number
        """
        completed_boards: list[int] = []
        for (b, r, c) in self._rev_index[number]:
            self._marks[b][r][c] = True
            if self._finished[b]:
                continue

            if (self._is_bingo_at(b, r, c)):
                self._finished[b] = True
                completed_boards.append(b)

        return completed_boards

    def get_score(self, board_idx: int) -> int:
        return sum(val for val, is_marked in
                   zip(chain.from_iterable(self._boards[board_idx]),
                       chain.from_iterable(self._marks[board_idx]))
                   if not is_marked)


def get_input() -> tuple[Sequence[int], BingoBoards]:
    inputs = sys.stdin.read().split("\n\n")
    number_order = [int(s) for s in inputs[0].split(",")]

    boards: list[list[list[int]]] = []
    for board_str in inputs[1:]:
        board: list[list[int]] = []
        for row in board_str.split("\n"):
            board.append([int(s) for s in row.split()])
        boards.append(board)

    return (number_order, BingoBoards(boards))


def get_results(
    number_order: Sequence[int],
    boards: BingoBoards
) -> Generator[int, None, None]:
    for number in number_order:
        if ((completed_boards := boards.mark_number(number))):
            for board_idx in completed_boards:
                yield number * boards.get_score(board_idx)


@main.command()
def part1():
    number_order, boards = get_input()

    res = next(get_results(number_order, boards))
    print(res)


@ main.command()
def part2():
    number_order, boards = get_input()

    res: Optional[int] = None
    for res in get_results(number_order, boards):
        pass

    print(res)


if __name__ == '__main__':
    main()
