import flet
from flet import (
    Container,
    Stack,
    FloatingActionButton,
    Row,
    alignment,
    Column,
    Image,
    Page,
    margin,
    icons,
    Dropdown,
    dropdown,
)
from utils import HTMLSession


def main(page: Page):
    page.title = "太·极"
    c = Container(margin=10, alignment=alignment.center, expand=True)
    url = "https://imgapi.cn/api.php?fl=dongman&gs=images"
    c = Image(src=url)

    save_btn = Container(
        FloatingActionButton(
            icon=icons.SAVE_ALT_ROUNDED,
            on_click=save_img,
            width=50,
        ),
        opacity=0.2,
        right=20,
        bottom=20,
    )
    s = Stack(controls=[c, save_btn])
    page.add(s)


flet.app(target=main)
