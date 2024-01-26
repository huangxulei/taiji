import flet as ft


class MyButton(ft.FloatingActionButton):
    def __init__(self, seconds):
        super().__init__()
        self.seconds = seconds


ft.app(target=main)
