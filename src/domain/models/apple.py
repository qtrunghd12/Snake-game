from typing import Tuple, List
from random import randrange

from ..interfaces import Drawable, Displayable, Position
from ..constants import *
from adapters.gui import snake_gui  # Import snake_gui


class Apple(Drawable):

    count = 0

    def __init__(self, size):
        self.x, self.y = self.generate_random_coordinates()
        self.size = size

    @staticmethod
    def generate_random_coordinates() -> Tuple[int, int]:
        return randrange(1, COL_COUNT - 1), randrange(1, ROW_COUNT-1)

    def set_random_position(self, walls: List[Position]):                    # change apple position
        while True:
            self.x, self.y = self.generate_random_coordinates()

            # Check if the new apple position collides with any wall
            apple_position = Position(
                coordinates=(self.x * CELL_SIZE, self.y * CELL_SIZE),
                dimensions=(self.size, self.size)
            )

            if not any(snake_gui.rectangles_collide(apple_position, wall) for wall in walls):
                break  # Valid position found

        if Apple.count % 3 == 0:    # each 3d apple is going to be bigger
            self.size = CELL_SIZE + 6
        else:
            self.size = CELL_SIZE

    @property
    def position(self) -> Position:
        return Position(
            coordinates=(self.x * CELL_SIZE, self.y * CELL_SIZE),
            dimensions=(self.size, self.size)
        )

    @property
    def drawable_objects_and_destinations(self):
        return Displayable(
            figures=[{
                "color": YELLOW,
                "destination": self.position,
            }],
            images=[]
        )
