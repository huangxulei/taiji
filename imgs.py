import flet
from flet import (
    Image,
    Container,
    Stack,
    FloatingActionButton,
    Page,
    Row,
    UserControl,
    icons,
    Text,
    MainAxisAlignment,
    TextField,
    TextAlign,
    IconButton,
)


class Counter(UserControl):
    def build(self):
        self.txt_number = TextField(value="0", text_align=TextAlign.RIGHT, width=100)
        return Row(
            [
                IconButton(icons.REMOVE, on_click=self.minus_click),
                self.txt_number,
                IconButton(icons.ADD, on_click=self.plus_click),
            ],
            alignment=MainAxisAlignment.CENTER,
        )

    def minus_click(self, e):
        self.txt_number.value = str(int(self.txt_number.value) - 1)
        self.update()

    def plus_click(self, e):
        self.txt_number.value = str(int(self.txt_number.value) + 1)
        self.update()


def main(page: Page):
    page.title = "Flet counter example"
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.update()

    counter = Counter()

    page.add(counter)


flet.app(main)
