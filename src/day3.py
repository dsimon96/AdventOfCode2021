import sys
from typing import Collection, Generator, Iterable, List, Optional, Sequence, cast
import click


@click.group()
def main():
    pass


BitSequence = Sequence[int]


def get_bit_sequences() -> Generator[BitSequence, None, None]:
    for line in sys.stdin.readlines():
        bit_seq: List[int] = []
        for char in line.rstrip():
            bit_seq.append(int(char))
        yield bit_seq


def get_most_common_bit(bit_seq: BitSequence) -> Optional[int]:
    one_count = sum(bit_seq)
    zero_count = len(bit_seq) - one_count
    if one_count > zero_count:
        return 1
    elif one_count < zero_count:
        return 0
    else:
        return None


def get_most_common_bits_by_place(
    bit_sequences: Iterable[BitSequence]
) -> BitSequence:
    return [cast(int, get_most_common_bit(place_bit_seq))
            for place_bit_seq in zip(*bit_sequences)]


def bit_seq_to_int(bit_seq: BitSequence) -> int:
    res = 0
    for bit in bit_seq:
        res <<= 1
        res |= bit
    return res


@main.command()
def part1():
    most_common_bits = get_most_common_bits_by_place(get_bit_sequences())

    gamma_rate = bit_seq_to_int(most_common_bits)
    bit_mask = 2 ** len(most_common_bits) - 1
    epsilon_rate = gamma_rate ^ bit_mask

    print(gamma_rate * epsilon_rate)


def do_filter_by_bit(
    bit_seqs: Collection[BitSequence],
    *,
    keep_most_common: bool
) -> BitSequence:
    place = 0
    bit_seqs = list(bit_seqs)
    while len(bit_seqs) > 1:
        place_bit_seq = [bit_seq[place] for bit_seq in bit_seqs]
        most_common_bit = get_most_common_bit(place_bit_seq)
        if most_common_bit is not None:
            bit_to_keep = (
                most_common_bit if keep_most_common else most_common_bit ^ 1)
        else:
            bit_to_keep = int(keep_most_common)

        bit_seqs = [
            bit_seq for bit_seq in bit_seqs if bit_seq[place] == bit_to_keep]
        place += 1

    return bit_seqs[0]


@main.command()
def part2():
    all_bit_seqs = list(get_bit_sequences())
    oxygen_generator_rating = bit_seq_to_int(do_filter_by_bit(
        all_bit_seqs, keep_most_common=True))
    co2_scrubber_rating = bit_seq_to_int(do_filter_by_bit(
        all_bit_seqs, keep_most_common=False))

    print(oxygen_generator_rating * co2_scrubber_rating)


if __name__ == "__main__":
    main()
