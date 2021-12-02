import sys
from enum import Enum, auto
from dataclasses import dataclass, replace
from typing import Callable, Generator, Iterable, TypeVar
import click


@click.group()
def main():
    pass


class Direction(Enum):
    FORWARD = auto()
    DOWN = auto()
    UP = auto()


@dataclass
class Command:
    direction: Direction
    units: int


def get_input() -> Generator[Command, None, None]:
    for line in sys.stdin.readlines():
        dir_s, units_s = line.split()
        yield Command(direction=Direction[dir_s.upper()], units=int(units_s))


@dataclass
class Position:
    depth: int = 0
    horizontal_pos: int = 0


@dataclass
class PositionAndAim:
    position: Position = Position()
    aim: int = 0


def update_position(pos: Position, command: Command) -> Position:
    match command:
        case Command(Direction.FORWARD, units):
            return replace(pos, horizontal_pos=pos.horizontal_pos+units)
        case Command(Direction.UP, units):
            return replace(pos, depth=pos.depth-units)
        case Command(Direction.DOWN, units):
            return replace(pos, depth=pos.depth+units)
        case _:
            raise ValueError


State = TypeVar('State')


def do_command_sequence(
    commands: Iterable[Command],
    initial_state: State,
    update_fn: Callable[[State, Command], State]
) -> State:
    state = initial_state
    for command in commands:
        state = update_fn(state, command)
    return state


@main.command()
def part1():
    pos = do_command_sequence(get_input(), Position(), update_position)
    print(pos.depth * pos.horizontal_pos)


def update_position_and_aim(
    pos_and_aim: PositionAndAim,
    command: Command
) -> PositionAndAim:
    pos = pos_and_aim.position
    aim = pos_and_aim.aim
    match command:
        case Command(Direction.FORWARD, units):
            new_pos = replace(pos,
                              horizontal_pos=pos.horizontal_pos+units,
                              depth=pos.depth+aim*units)
            return replace(pos_and_aim, position=new_pos)
        case Command(Direction.UP, units):
            return replace(pos_and_aim, aim=aim-units)
        case Command(Direction.DOWN, units):
            return replace(pos_and_aim, aim=aim+units)
        case _:
            raise ValueError


@main.command()
def part2():
    pos = do_command_sequence(
        get_input(), PositionAndAim(), update_position_and_aim).position
    print(pos.depth * pos.horizontal_pos)


if __name__ == "__main__":
    main()
