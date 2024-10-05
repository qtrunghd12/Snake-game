from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout  # Import FloatLayout for better positioning
from kivy.graphics import Color, Rectangle  # Import Color and Rectangle for background

from domain.snake_game import SnakeGame

# Set window size
Window.size = (600, 500)

class NewUserGreeting(FloatLayout):  # Change to FloatLayout for flexibility
    def __init__(self, quit_callback, **kwargs):
        super(NewUserGreeting, self).__init__(**kwargs)
        from domain.models.user import GameUser
        self.quit_callback = quit_callback
        self._user = GameUser(name="Bob")

        # Thêm Background (Màu cam)
        with self.canvas.before:
            Color(1, 0.65, 0, 1)  # RGBA for orange
            self.rect = Rectangle(size=Window.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)


        # Creating a GridLayout to structure the widgets / Define "grid"
        grid = GridLayout(cols=1, size_hint=(0.7, 0.8), pos_hint={"center_x": 0.5, "center_y": 0.5})

        # Thêm ảnh và chỉnh kích cỡ của ảnh
        grid.add_widget(Image(source="images/SnakeLogo.png", size_hint=(20, 2)))

        # Thêm tên
        self.label = Label(
            text="Nhập Tên: ",
            font_size=40,
            color="#228B22",
        )
        grid.add_widget(self.label)

        # Thêm phần nhập tên
        self.name_input = TextInput(
            multiline=False,
            font_size=40,
            padding=[10, 10, 10, 10],
            size_hint=(1, 0.5)
        )
        # Bind the TextInput to the on_name_enter method
        self.name_input.bind(on_text_validate=self.on_name_enter)
        grid.add_widget(self.name_input)

        # Thêm nút bắt đầu
        self.start_button = Button(
            text="Bắt đầu",
            size_hint=(1, 0.5),
            bold=True,
            background_color="#228B22",
            background_normal="",
        )
        self.start_button.bind(on_press=self.close_window)
        grid.add_widget(self.start_button)

        # Add the grid to the layout
        self.add_widget(grid)

    # Method to handle pressing Enter after typing the name
    def on_name_enter(self, instance):
        user_name = self.name_input.text  # Get the entered name
        print(f"Entered name: {user_name}")  # Print it for debugging
        self.label.text = f"Tên: {user_name}"  # Update label text with the entered name
        self._user.set_name(user_name)  # Set the name in the user object
        self.quit_callback()  # Close the window or proceed with the game

    # Method to close the window
    def close_window(self, instance):
        self._user.set_name(self.name_input.text)
        print(f"USER NAME FORM INPUT: {self._user.get_name()}")
        self.quit_callback()

    # Method to update the background rectangle size and position
    def _update_rect(self, instance, value):
        self.rect.size = Window.size  # Cập nhật để cho màu của background lấp hết cửa sổ
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

    def build(self):
        return self.window

    def open_new_user_window(self):
        self.window = NewUserGreeting(self.quit)

    def quit(self, *args):
        print("Trò chơi bắt đầu!")
        self.user = self.window.get_user()
        self.stop()
        SnakeGame(self.user).start()

    def set_user_name(self, name):
        self.user_name = name


app = SnakeApp()

def main():
    app.run()


if __name__ == "__main__":
    main()
