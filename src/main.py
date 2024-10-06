from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.spinner import Spinner  # Import Spinner

from domain.snake_game import SnakeGame

# Set window size
Window.size = (600, 500)

class NewUserGreeting(FloatLayout):
    def __init__(self, quit_callback, **kwargs):
        super(NewUserGreeting, self).__init__(**kwargs)
        from domain.models.user import GameUser
        self.quit_callback = quit_callback
        self._user = GameUser(name="Bob")

        with self.canvas.before:
            Color(1, 0.65, 0, 1)
            self.rect = Rectangle(size=Window.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        grid = GridLayout(cols=1, size_hint=(0.7, 0.8), pos_hint={"center_x": 0.5, "center_y": 0.5})

        grid.add_widget(Image(source="images/Logo1.png", size_hint=(35, 4)))

        self.label = Label(
            text="Nhập Tên: ",
            font_size=30,
            color="#228B22",
        )
        grid.add_widget(self.label)

        self.name_input = TextInput(
            multiline=False,
            font_size=40,
            padding=[10, 10, 10, 10],
            size_hint=(1, 0.5)
        )
        self.name_input.bind(on_text_validate=self.on_name_enter)
        grid.add_widget(self.name_input)

        # Spinner để chọn độ khó
        self.difficulty_spinner = Spinner(
            text='Chọn Độ Khó',
            values=('Dễ', 'Trung Bình', 'Khó'),
            size_hint=(1, 0.5)
        )
        grid.add_widget(self.difficulty_spinner)

        self.start_button = Button(
            text="Bắt đầu",
            size_hint=(1, 0.5),
            bold=True,
            background_color="#228B22",
            background_normal="",
        )
        self.start_button.bind(on_press=self.close_window)
        grid.add_widget(self.start_button)

        self.add_widget(grid)

    def on_name_enter(self, instance):
        user_name = self.name_input.text
        print(f"Entered name: {user_name}")
        self.label.text = f"Tên: {user_name}"
        self._user.set_name(user_name)
        self.quit_callback(self.difficulty_spinner.text)  # Gửi độ khó đến callback

    def close_window(self, instance):
        self._user.set_name(self.name_input.text)
        self.quit_callback(self.difficulty_spinner.text)  # Gửi độ khó đến callback

    def _update_rect(self, instance, value):
        self.rect.size = Window.size
        self.rect.pos = self.pos

    def get_user(self):
        return self._user

class SnakeApp(App):
    def __init__(self):
        super(SnakeApp, self).__init__()
        self.window = None
        self.open_new_user_window()
        self.user = None
        self.user_name = None
        self.difficulty = None  # Thêm thuộc tính cho độ khó

    def build(self):
        return self.window

    def open_new_user_window(self):
        self.window = NewUserGreeting(self.quit)

    def quit(self, difficulty, *args):  # Nhận độ khó từ NewUserGreeting
        print("Trò chơi bắt đầu!")
        self.user = self.window.get_user()
        self.difficulty = difficulty  # Lưu độ khó
        self.stop()
        SnakeGame(self.user, self.difficulty).start()  # Truyền độ khó vào SnakeGame

    def set_user_name(self, name):
        self.user_name = name


app = SnakeApp()

def main():
    app.run()

if __name__ == "__main__":
    main()
