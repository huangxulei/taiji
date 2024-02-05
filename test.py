from flet import *


def main(page: Page):
    page.padding = 0

    row = Row(wrap=True, run_spacing=80, scroll=True)
    for i in range(20):
        row.controls.append(
            Container(
                content=Text(f"This is {i}"),
                bgcolor=colors.BLACK38,
                width=300,
                height=100,
                margin=margin.only(right=50),
            )
        )
    m = Container(content=row, margin=margin.only(bottom=205), bgcolor=colors.RED_200)

    next_btn = Column(
        [
            Container(
                Row(
                    [Text("show info")],
                    alignment="center",
                ),
                height=200,
                bgcolor=colors.AMBER_100,
                border=border.only(top=border.BorderSide(2, "grey")),
                padding=0,
            )
        ],
        alignment="end",
    )
    c = Stack(
        controls=[m, next_btn],
        expand=True,
    )

    page.add(c)


app(target=main, assets_dir="assets")
