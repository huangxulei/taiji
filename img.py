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
    TextField,
    TextAlign,
    alignment,
    IconButton,
)
import time, random


class ShowPic(Stack):
    def __init__(self, page: Page):
        self.page = page

        self.url = "https://imgapi.cn/api.php?fl=fengjing&gs=images"
        self.content_area = Container(
            margin=10, alignment=alignment.center, expand=True
        )
        self.content_area.content = Image(src=self.url)
        super(ShowPic, self).__init__(
            controls=[
                self.content_area,
                IconButton(icons.ADD, on_click=self.fresh_image),
            ],
            expand=True,
        )

    def fresh_image(self, e):
        num = random.randint(1, 100)
        self.url = self.url + "&{num}"
        self.content_area.content = Image(src=self.url)
        self.update()


def main(page: Page):
    page.title = "ToDo App"
    page.horizontal_alignment = "center"
    page.update()

    # create application instance
    todo = ShowPic(page)

    # add application's root control to the page
    page.add(todo)


flet.app(target=main)
