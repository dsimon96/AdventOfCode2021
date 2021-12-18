from typing import Optional, TypeAlias, Union
import click
import sys
from dataclasses import dataclass
from enum import Enum, auto
from statistics import median_low


@click.group()
def main(): pass


class DelimType(Enum):
    Parenthesis = auto()
    SquareBracket = auto()
    CurlyBracket = auto()
    AngleBracket = auto()


class DelimDirection(Enum):
    Open = auto()
    Close = auto()


@dataclass(frozen=True)
class Delim:
    t: DelimType
    d: DelimDirection


DELIM_LOOKUP_TABLE = {
    "(": Delim(t=DelimType.Parenthesis, d=DelimDirection.Open),
    "[": Delim(t=DelimType.SquareBracket, d=DelimDirection.Open),
    "{": Delim(t=DelimType.CurlyBracket, d=DelimDirection.Open),
    "<": Delim(t=DelimType.AngleBracket, d=DelimDirection.Open),
    ")": Delim(t=DelimType.Parenthesis, d=DelimDirection.Close),
    "]": Delim(t=DelimType.SquareBracket, d=DelimDirection.Close),
    "}": Delim(t=DelimType.CurlyBracket, d=DelimDirection.Close),
    ">": Delim(t=DelimType.AngleBracket, d=DelimDirection.Close),
}


ILLEGAL_DELIM_POINTS: dict[DelimType, int] = {
    DelimType.Parenthesis: 3,
    DelimType.SquareBracket: 57,
    DelimType.CurlyBracket: 1197,
    DelimType.AngleBracket: 25137
}

AUTOCOMPLETE_DELIM_POINTS: dict[DelimType, int] = {
    DelimType.Parenthesis: 1,
    DelimType.SquareBracket: 2,
    DelimType.CurlyBracket: 3,
    DelimType.AngleBracket: 4
}


@dataclass
class Corrupted:
    illegal_delim_type: DelimType


@dataclass
class Incomplete:
    chunk_stack: list[DelimType]


class Valid:
    pass


ParseResult: TypeAlias = Union[Corrupted, Incomplete, Valid]


def parse_line(s: str) -> ParseResult:
    chunk_stack: list[DelimType] = []

    for c in s:
        delim = DELIM_LOOKUP_TABLE[c]
        if delim.d == DelimDirection.Open:
            chunk_stack.append(delim.t)
        elif delim.d == DelimDirection.Close:
            last_chunk_t = chunk_stack.pop() if len(chunk_stack) > 0 else None
            if delim.t != last_chunk_t:
                return Corrupted(illegal_delim_type=delim.t)
        else:
            raise ValueError

    if len(chunk_stack) > 0:
        return Incomplete(chunk_stack=chunk_stack)

    return Valid()


def syntax_error_score(s: str) -> Optional[int]:
    parse_result = parse_line(s)
    if not isinstance(parse_result, Corrupted):
        return None

    return ILLEGAL_DELIM_POINTS[parse_result.illegal_delim_type]


@main.command()
def part1():
    print(sum(filter(lambda x: x is not None,
          (syntax_error_score(line.rstrip()) for line in sys.stdin))))


def autocomplete_score(s: str) -> Optional[int]:
    parse_result = parse_line(s)
    if not isinstance(parse_result, Incomplete):
        return None

    total = 0
    for delim_type in reversed(parse_result.chunk_stack):
        total *= 5
        total += AUTOCOMPLETE_DELIM_POINTS[delim_type]

    return total


@main.command()
def part2():
    print(median_low(filter(lambda x: x is not None,
          (autocomplete_score(line.rstrip()) for line in sys.stdin))))


if __name__ == '__main__':
    main()
