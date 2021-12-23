from typing import TextIO, cast
from enum import Enum
from bitstring import BitStream
from dataclasses import dataclass
from math import prod
import click
import sys


class PacketType(Enum):
    Op_Sum = 0
    Op_Product = 1
    Op_Min = 2
    Op_Max = 3
    Literal = 4
    Op_Gt = 5
    Op_Lt = 6
    Op_Eq = 7


@dataclass
class Literal:
    value: int

    @staticmethod
    def parse(bits: BitStream) -> "Literal":
        int_bits = BitStream()
        keep_reading = True
        while keep_reading:
            keep_reading = cast('bool', bits.read('bool'))
            int_bits.append(bits.read(4))
        return Literal(value=int_bits.uint)

    def eval(self) -> int: return self.value


@dataclass
class OperatorData:
    op: PacketType
    subpackets: list["BITSPacket"]

    @staticmethod
    def parse_subp_by_length(bits: BitStream, length: int) -> list["BITSPacket"]:
        total_read = 0
        res: list["BITSPacket"] = []
        while total_read < length:
            next_subp = BITSPacket.parse(bits)
            res.append(next_subp)
            total_read += next_subp.length

        return res

    @staticmethod
    def parse_n_subp(bits: BitStream, n: int) -> list["BITSPacket"]:
        res: list["BITSPacket"] = []
        for _ in range(n):
            res.append(BITSPacket.parse(bits))

        return res

    @staticmethod
    def parse(op_type: PacketType, bits: BitStream) -> "OperatorData":
        length_type_id = cast('int', bits.read('uint:1'))
        match length_type_id:
            case 0:
                length = cast('int', bits.read('uint:15'))
                subpackets = OperatorData.parse_subp_by_length(bits, length)
            case 1:
                n = cast('int', bits.read('uint:11'))
                subpackets = OperatorData.parse_n_subp(bits, n)
            case _:
                raise ValueError

        return OperatorData(op_type, subpackets)

    def eval(self) -> int:
        match self.op:
            case PacketType.Op_Sum:
                return sum(subp.eval() for subp in self.subpackets)
            case PacketType.Op_Product:
                return prod(subp.eval() for subp in self.subpackets)
            case PacketType.Op_Min:
                return min(subp.eval() for subp in self.subpackets)
            case PacketType.Op_Max:
                return max(subp.eval() for subp in self.subpackets)
            case PacketType.Op_Gt:
                return int(self.subpackets[0].eval() >
                           self.subpackets[1].eval())
            case PacketType.Op_Lt:
                return int(self.subpackets[0].eval() <
                           self.subpackets[1].eval())
            case PacketType.Op_Eq:
                return int(self.subpackets[0].eval() ==
                           self.subpackets[1].eval())
            case _:
                raise NotImplementedError


@dataclass
class BITSPacket:
    length: int
    version: int
    data: Literal | OperatorData

    @staticmethod
    def parse(bits: BitStream) -> "BITSPacket":
        initial_pos = bits.pos
        version = cast('int', bits.read('uint:3'))
        type_id = PacketType(cast('int', bits.read('uint:3')))
        match type_id:
            case PacketType.Literal:
                data = Literal.parse(bits)
            case op:
                data = OperatorData.parse(op, bits)

        length = bits.pos - initial_pos
        return BITSPacket(length, version, data)

    def eval(self) -> int:
        return self.data.eval()


@click.group()
def main(): pass


def version_sum(packet: BITSPacket) -> int:
    total = packet.version
    if isinstance(packet.data, OperatorData):
        total += sum(version_sum(subp) for subp in packet.data.subpackets)

    return total


def get_packet(inp: TextIO) -> BITSPacket:
    return BITSPacket.parse(BitStream('0x' + inp.readline()))


@main.command()
def part1():
    packet = get_packet(sys.stdin)
    print(version_sum(packet))


@main.command()
def part2():
    packet = get_packet(sys.stdin)
    print(packet.eval())


if __name__ == '__main__':
    main()
