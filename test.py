import math
from flet import *


def main(page: Page):
    page.padding = 0

    # top_area = Row([Text("第一个显示区域"), Text("第一个显示区域")])
    # lvs = ListView(expand=1, spacing=10, padding=20)
    grs = GridView(runs_count=3, spacing=30)

    # lv = Row(expand=True, spacing=50, wrap=True, run_spacing=20, scroll=True)
    for i in range(100):
        grs.controls.append(
            Container(
                content=Text(f"第{i}个"), bgcolor=colors.BLACK38, width=100, height=200
            )
        )

    # topc = Column(
    #     [top_area, lvs],
    #     alignment="end",
    # )
    next_btn = Column(
        [
            Container(
                Row(
                    [
                        Container(
                            FloatingActionButton(
                                icon=icons.DOUBLE_ARROW_ROUNDED,
                                width=100,
                            ),
                            margin=margin.Margin(0, 0, 0, 100),
                        )
                    ],
                    alignment="center",
                ),
                bgcolor=colors.AMBER_100,
                border=border.only(top=border.BorderSide(2, "grey")),
            )
        ],
        alignment="end",
    )
    c = Stack(
        controls=[grs, next_btn],
        expand=True,
    )

    page.add(c)


app(target=main, assets_dir="assets")
