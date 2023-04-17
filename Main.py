from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle


class TitleBox(BoxLayout):
    orientation = 'vertical'

    def __init__(self, **kwargs):
        super(TitleBox, self).__init__(**kwargs)
        self.add_widget(Label(text='JOGO DA VELHA', font_size=40, size_hint=(1, 0.2)))
        self.add_widget(TicTacToeBoard())


class TicTacToeBoard(GridLayout):
    def __init__(self, **kwargs):
        super(TicTacToeBoard, self).__init__(**kwargs)
        self.cols = 3
        self.buttons = []
        for _ in range(9):
            button = Button(text='', font_size=80, on_release=self.on_button_release)
            self.buttons.append(button)
            self.add_widget(button)
        self.player = 'X'
        self.game_over = False
        self.winning_combinations = (
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # horizontal
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # vertical
            (0, 4, 8), (2, 4, 6)  # diagonal
        )

    def on_button_release(self, button):
        if button.text == '' and not self.game_over:
            button.text = self.player
            button.disabled = True
            self.check_game_status()
            self.player = 'O' if self.player == 'X' else 'X'

    def check_game_status(self):
        for combination in self.winning_combinations:
            if all(self.buttons[i].text == 'X' for i in combination):
                self.show_game_over_popup('X venceu!')
                return
            elif all(self.buttons[i].text == 'O' for i in combination):
                self.show_game_over_popup('O venceu!')
                return

        if all(button.text != '' for button in self.buttons):
            self.show_game_over_popup('Empate!')

    def show_game_over_popup(self, message):
        self.game_over = True
        if message is None:
            message = 'Empate!'
        content = Label(text=message)
        popup = Popup(title='Fim de jogo', content=content, size_hint=(None, None), size=(400, 200))
        content.bind(on_release=popup.dismiss)
        popup.open()
        self.reset_game()

    def reset_game(self):
        for button in self.buttons:
            button.text = ''
            button.disabled = False
        self.player = 'X'
        self.game_over = False


class TicTacToeApp(App):
    def build(self):
        return TitleBox()


if __name__ == '__main__':
    Builder.load_string("""
<TitleBox>:
    orientation: 'vertical'
    """)
    TicTacToeApp().run()