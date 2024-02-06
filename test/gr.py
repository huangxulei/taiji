from flet import *


def main(page: Page):

    child = Column(
        [
            Image(
                src="https://picsum.photos/150/150?1",
            ),
        ]
    )
    item = Container(
        content=child, border=border.all(10, colors.PINK_600), width=300, height=200
    )

    row = Row(expand=True, spacing=50, wrap=True, run_spacing=20)

    for i in range(60):
        row.controls.append(item)

    s = Stack([row])

    page.add(s)


app(target=main, assets_dir="assets")
