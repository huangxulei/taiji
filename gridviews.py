from flet import *


def main(page: Page):
    page.padding = 0

    grs = GridView(runs_count=3, spacing=30)

    for i in range(100):
        grs.controls.append(
            Container(
                content=Text(f"第{i}个"), bgcolor=colors.BLACK38, width=200, height=100
            )
        )

    c = Stack(
        controls=[grs],
        expand=True,
    )

    page.add(c)


app(target=main)
