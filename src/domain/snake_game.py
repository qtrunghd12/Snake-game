import sys
from adapters.gui import snake_gui
from domain.interfaces import GameEventTypes, Result, Color
from domain.constants import (
    TILE_IMAGE,
    CELL_SIZE,
    SCORE_FONT,
    TURQUOISE,
    BLACK,
    LARGE_FONT,
    BLUE,
    RED,
    WHITE,
)
from domain.models.apple import Apple
from domain.models.snake import Snake
from domain.models.user import GameUser
from domain.models.walls import Walls, WallsType
from adapters.repository import save_result

class SnakeGame:
    def __init__(self, player: GameUser, difficulty: str):  # Thêm tham số độ khó
        self.game_over = False
        snake_gui.init_screen()
        self.player = player
        self._snake = Snake(TILE_IMAGE)
        self._apple = Apple(CELL_SIZE)
        self._seconds_before_start = 3
        self._points = 0

        snake_gui.set_caption(f'Snake-{player.get_name()}')

        # Chọn tường dựa trên độ khó
        if difficulty == 'Dễ':
            self.walls_list = Walls(WallsType.EASY_PARALLEL).get_list(CELL_SIZE)
        elif difficulty == 'Trung Bình':
            self.walls_list = Walls(WallsType.ROOM_FRAME).get_list(CELL_SIZE)
        else:  # 'Khó'
            self.walls_list = Walls(WallsType.COMPLEX).get_list(CELL_SIZE)

    @staticmethod
    def _print_text(text: str, color: Color, font=None, textpos=None):
        snake_gui.render_text(text, color, font, textpos)
        snake_gui.update_display_to_screen()

    def _show_status_text(self):
        text = "Số Táo: {}  Số Điểm: {}          Số Mạng còn lại: {}  ".format(self._apple.count, self._points, "♥" * self._snake.lives)
        snake_gui.render_text(text, WHITE, SCORE_FONT, (10, 10))

    def _draw_walls(self):
        for wall in self.walls_list:
            snake_gui.draw_rectangle(wall, ((205,196,170)))

    def _countdown(self):
        while self._seconds_before_start > 0:
            self._print_text("{}".format(self._seconds_before_start), RED, LARGE_FONT)
            snake_gui.wait(1000)
            snake_gui.fill_with((0, 0, 0))
            self._seconds_before_start -= 1

    def _draw_game_objects(self):
        snake_gui.fill_with((19, 138, 21))  # Thiết lập màu nền xanh lá
        self._show_status_text()
        self._draw_walls()
        objects = [self._snake, self._apple]
        for obj in objects:
            snake_gui.draw(obj.drawable_objects_and_destinations)
        snake_gui.update_display_to_screen()

    def _increase_points(self, points: int):
        self._points += points

    def quit(self):
        snake_gui.quit()
        sys.exit()

    def _handle_user_events(self):
        for event in snake_gui.get_events():
            if event.type.value == GameEventTypes.QUIT.value:
                self.quit()
            elif event.type.value == GameEventTypes.KEYDOWN.value:
                self._snake.set_direction(event.key)
            elif event.type.value == GameEventTypes.KEYUP.value:
                self._snake.slow_down_default()

    def _move_snake(self):
        self._snake.move_head()

        touched_apple = snake_gui.rectangles_collide(self._snake.head_position, self._apple.position)
        if touched_apple:
            self._increase_points(self._apple.size)
            self._apple.set_random_position(self.walls_list)
            Apple.count += 1
        else:
            self._snake.remove_tail()

        if self._snake.hit_walls(self.walls_list) or self._snake.hit_itself():
            if self._snake.is_alive():
                self._snake.start_new_live()
                self._apple.set_random_position(self.walls_list)
            else:
                self._print_text("Trò chơi kết thúc", RED, LARGE_FONT)
                self.game_over = True

    def _handle_one_frame(self):
        self._handle_user_events()
        self._draw_game_objects()
        self._move_snake()
        snake_gui.trigger_next_frame(self._snake.speed)

    def start(self):
        self._countdown()
        while not self.game_over:
            self._handle_one_frame()

        save_result(Result(player_name=self.player.get_name(), apples=Apple.count, points=self._points))
        snake_gui.wait(2000)
