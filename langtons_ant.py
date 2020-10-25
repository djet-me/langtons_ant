from dataclasses import dataclass
import os
import random
import time
from typing import List, Optional, NamedTuple


@dataclass
class Point:
    x: int
    y: int


class Direction(NamedTuple):
    x: int
    y: int


UP = Direction(0, -1)
RIGHT = Direction(1, 0)
DOWN = Direction(0, 1)
LEFT = Direction(-1, 0)

DIRECTION_CHOICES = (UP, RIGHT, DOWN, LEFT)


class LangtonsAnt:
    """
    Langton's Ant Automata.
    https://doi.org/10.1016%2F0167-2789%2886%2990237-X
    """

    def __init__(
        self,
        initial_state: List[List[bool]],
        start_position: Optional[List[int]] = None,
        direction: Optional[List[int]] = None,
    ) -> None:
        """
        Init Langton's Ant instance. Raise ValueError if invalid input values are provided.
        :param initial_state: Two-dimensional list of booleans for automata grid
        :param start_position: Optional list with integers [X, Y] position for ant
        :param direction: Optional list with integers [X, Y] direction for ant
        """
        if not initial_state:
            raise ValueError("`initial_state` must contain at least one nested list.")
        self.__height = len(initial_state)
        self.__width = len(initial_state[0])
        if self.__width == 0:
            raise ValueError(
                "`initial_state` nested lists must contain at least one element."
            )
        errors_in_initial_state = [self.__width != len(row) for row in initial_state]
        if any(errors_in_initial_state):
            raise ValueError(
                "`initial_state` must contain lists with equal number of elements."
            )
        self.__state = initial_state
        if start_position:
            if len(start_position) != 2:
                raise ValueError(
                    "`start_position` must contain 2 integers for ant position."
                )
            self.__position = Point(
                x=start_position[0] % self.__width, y=start_position[1] % self.__height
            )
        else:
            self.__position = Point(x=int(self.__width / 2), y=int(self.__height / 2))
        if direction in DIRECTION_CHOICES:
            self.__direction = direction
        else:
            self.__direction = random.choice(DIRECTION_CHOICES)

    @property
    def state(self) -> List[List[bool]]:
        """
        :return: Current state of automata without ant
        """
        return self.__state

    @property
    def position_and_direction(self) -> List[int]:
        """
        :return: Current position and direction of ant
        """
        direction_text = ""
        if self.__direction == UP:
            direction_text = "UP"
        elif self.__direction == RIGHT:
            direction_text = "RIGHT"
        elif self.__direction == DOWN:
            direction_text = "DOWN"
        elif self.__direction == LEFT:
            direction_text = "LEFT"
        return [
            self.__position,
            direction_text,
            self.__state[self.__position.x][self.__position.y],
        ]

    def next(self) -> None:
        """
        Move and rotate ant on grid.
        :return: None
        """
        x, y = self.__position.x, self.__position.y
        if self.__state[x][y]:
            self.__direction = Direction(self.__direction.y, -self.__direction.x)
        else:
            self.__direction = Direction(-self.__direction.y, self.__direction.x)
        self.__state[x][y] = not self.__state[x][y]  # change color of cell
        self.__position.x = (self.__position.x + self.__direction.x) % self.__width
        self.__position.y = (self.__position.y + self.__direction.y) % self.__height

    def draw(self) -> None:
        """
        Draw grid and ant on it.
        :return: None
        """
        final_state = ""
        for index, el in enumerate(self.state):
            row = [self.__translate(x) for x in el]
            if index == self.__position.x:
                row[self.__position.y] = "x"
            final_state += "".join(row) + "\n"
        print(final_state)

    def run(
        self, delay: float = 0.5, epoch: int = 111, clear_each_step: bool = True
    ) -> None:
        """
        Run Langton's Ant Automata and redraw grid and ant after each step.
        :param delay: Float delay in seconds before step
        :param epoch: Integer number of steps
        :param clear_each_step: Optional bool flag for screen cleaning before automata step, True by default
        :return: None
        """
        for current_epoch in range(epoch):
            try:
                if clear_each_step:
                    self.__clear()
                print(f"epoch: {current_epoch + 1}\n{'=' * 10}")
                self.draw()
                time.sleep(delay)
                self.next()
            except KeyboardInterrupt:
                exit()

    @staticmethod
    def __translate(value: bool) -> str:
        """
        Translates bool value to ' ' or '.' char
        :param value: bool
        :return: ' ' if value=False or '.' if value=True
        """
        if value:
            return "."
        return " "

    @staticmethod
    def __clear() -> None:
        """
        Clear console screen in unix/nt systems
        :return: None
        """
        os.system("cls" if os.name == "nt" else "clear")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-gs", "--grid_size", type=int, help="grid size for automata")
    parser.add_argument(
        "-d", "--delay", type=int, help="delay before each step", default=0.5
    )
    parser.add_argument(
        "-e", "--epoch", type=int, help="count of steps for automata", default=111
    )
    args = parser.parse_args()
    if not args.grid_size:
        raise ValueError("`grid_size` parameter required")
    grid = list()
    for i in range(int(args.grid_size)):
        row = list()
        for j in range(int(args.grid_size)):
            row.append(False)
        grid.append(row)
    ant = LangtonsAnt(grid)
    ant.run(delay=args.delay, epoch=args.epoch)
