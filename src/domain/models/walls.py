import enum
from typing import List
from ..constants import *
from ..interfaces import Position

class WallsType(enum.Enum):
    EASY_PARALLEL = "EASY_PARALLEL"
    ROOM_FRAME = "ROOM_FRAME"
    COMPLEX = "COMPLEX"  # Độ khó phức tạp mới

class Walls:
    def __init__(self, walls_type: WallsType):
        self.walls_type = walls_type
        self.color = BLUE

    def get_list(self, size) -> List[Position]:
        """Tạo danh sách các tọa độ tường"""
        horizontal_walls = [   # tường ngang trên dưới
            Position(coordinates=(0, 0), dimensions=(GAME_SCREEN_WIDTH, size)),
            Position(coordinates=(0, GAME_SCREEN_HEIGHT - size), dimensions=(GAME_SCREEN_WIDTH, size)),
        ]
        vertical_walls = [   # Tường dọc trái phải
            Position(coordinates=(GAME_SCREEN_WIDTH - size, 0), dimensions=(size, GAME_SCREEN_HEIGHT)),    # tường bên phải
            Position(coordinates=(0, 0), dimensions=(size, GAME_SCREEN_HEIGHT)),  # tường bên trái
        ]
        complex_walls = [   # Tạo một cấu trúc tường phức tạp hơn
            Position(coordinates=(GAME_SCREEN_WIDTH // 2, 0), dimensions=(size, GAME_SCREEN_HEIGHT // 2.3)),  # tường dọc ở giữa
            Position(coordinates=(GAME_SCREEN_WIDTH // 4, GAME_SCREEN_HEIGHT // 4), dimensions=(size, GAME_SCREEN_HEIGHT // 2)),  # tường ở một vị trí khác
            Position(coordinates=(3 * GAME_SCREEN_WIDTH // 4, GAME_SCREEN_HEIGHT // 4), dimensions=(size, GAME_SCREEN_HEIGHT // 2)),  # tường ở vị trí đối diện
        ]

        if self.walls_type == WallsType.EASY_PARALLEL:
            return horizontal_walls
        elif self.walls_type == WallsType.ROOM_FRAME:
            return horizontal_walls + vertical_walls
        elif self.walls_type == WallsType.COMPLEX:
            return horizontal_walls + complex_walls + vertical_walls
        return []
