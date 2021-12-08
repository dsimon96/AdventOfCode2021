from typing import Generator, Iterable, TextIO
import sys
import click
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, auto


@click.group()
def main(): pass


class Segment(Enum):
    T = auto()
    M = auto()
    B = auto()
    UL = auto()
    UR = auto()
    LL = auto()
    LR = auto()


class Signal(Enum):
    A = auto()
    B = auto()
    C = auto()
    D = auto()
    E = auto()
    F = auto()
    G = auto()


DIGITS: dict[frozenset[Segment], int] = {
    frozenset((Segment.T, Segment.UL, Segment.UR, Segment.LL, Segment.LR,
               Segment.B)): 0,
    frozenset((Segment.UR, Segment.LR)): 1,
    frozenset((Segment.T, Segment.UR, Segment.M, Segment.LL, Segment.B)): 2,
    frozenset((Segment.T, Segment.UR, Segment.M, Segment.LR, Segment.B)): 3,
    frozenset((Segment.UL, Segment.M, Segment.UR, Segment.LR)): 4,
    frozenset((Segment.T, Segment.UL, Segment.M, Segment.LR, Segment.B)): 5,
    frozenset((Segment.T, Segment.UL, Segment.M, Segment.LL, Segment.LR,
               Segment.B)): 6,
    frozenset((Segment.T, Segment.UR, Segment.LR)): 7,
    frozenset((Segment.T, Segment.UL, Segment.UR, Segment.M, Segment.LL,
               Segment.LR, Segment.B)): 8,
    frozenset((Segment.T, Segment.UL, Segment.UR, Segment.M, Segment.LR,
               Segment.B)): 9,
}


@dataclass(eq=True, frozen=True)
class SignalPattern:
    signals: frozenset[Signal]

    @staticmethod
    def from_str(s: str) -> "SignalPattern":
        signals: set[Signal] = set()
        for c in s:
            signals.add(Signal[c.upper()])

        return SignalPattern(frozenset(signals))


@dataclass
class Observation:
    patterns: list[SignalPattern]
    output: list[SignalPattern]

    @staticmethod
    def from_str(s: str) -> "Observation":
        seq_str, output_str = s.split("|")

        return Observation(
            patterns=[SignalPattern.from_str(tok)
                      for tok in seq_str.strip().split()],
            output=[SignalPattern.from_str(tok)
                    for tok in output_str.strip().split()])


def get_observations(inp: TextIO) -> Generator[Observation, None, None]:
    for line in inp:
        yield Observation.from_str(line)


def can_only_be_one_digit(pattern: SignalPattern) -> bool:
    return len(pattern.signals) in (2, 3, 4, 7)


@main.command()
def part1():
    num_unique_digits = 0
    for observation in get_observations(sys.stdin):
        for pattern in observation.output:
            if can_only_be_one_digit(pattern):
                num_unique_digits += 1

    print(num_unique_digits)


def determine_mapping(
    patterns: Iterable[SignalPattern]
) -> dict[SignalPattern, int]:
    patterns_by_num_signals: dict[int, set[SignalPattern]] = defaultdict(set)
    num_on_by_signal: dict[Signal, int] = defaultdict(int)

    for pattern in patterns:
        patterns_by_num_signals[len(pattern.signals)].add(pattern)
        for signal in pattern.signals:
            num_on_by_signal[signal] += 1

    p1, = patterns_by_num_signals[2]
    p4, = patterns_by_num_signals[4]
    p7, = patterns_by_num_signals[3]
    p8, = patterns_by_num_signals[7]

    signals_by_num_on: dict[int, set[Signal]] = defaultdict(set)
    for signal, count in num_on_by_signal.items():
        signals_by_num_on[count].add(signal)

    sig_t, = p7.signals - p1.signals
    sig_ul, = signals_by_num_on[6]
    sig_ll, = signals_by_num_on[4]
    sig_lr, = signals_by_num_on[9]
    sig_ur, = p1.signals - set((sig_lr,))
    sig_m, = p4.signals - set((sig_ul, sig_ur, sig_lr))
    sig_b, = p8.signals - set((sig_t, sig_ul, sig_ur, sig_m, sig_ll, sig_lr))

    sig_to_seg: dict[Signal, Segment] = {
        sig_t: Segment.T,
        sig_ul: Segment.UL,
        sig_ur: Segment.UR,
        sig_ll: Segment.LL,
        sig_lr: Segment.LR,
        sig_m: Segment.M,
        sig_b: Segment.B,
    }

    res: dict[SignalPattern, int] = {}
    for pattern in patterns:
        segments = frozenset({sig_to_seg[sig] for sig in pattern.signals})
        res[pattern] = DIGITS[segments]

    return res


def decode_output_seq(
    output: Iterable[SignalPattern],
    mapping: dict[SignalPattern, int]
) -> int:
    res = 0
    for pattern in output:
        res *= 10
        res += mapping[pattern]
    return res


@main.command()
def part2():
    tot = 0
    for observation in get_observations(sys.stdin):
        mapping = determine_mapping(observation.patterns)
        tot += decode_output_seq(observation.output, mapping)
    print(tot)


if __name__ == '__main__':
    main()
