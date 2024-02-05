from flet import *


def main(page: Page):
    page.padding = 0

    top = Container(height=30, bgcolor=colors.AMBER_300)
    center = Container(expand=1, bgcolor=colors.GREEN_100)
    bottom = Container(height=30, bgcolor=colors.BLUE)
    col = Column(
        spacing=0,
        controls=[top, center, bottom],
    )

    page.add(col)


app(target=main)
