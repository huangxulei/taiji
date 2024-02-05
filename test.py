from flet import *


def main(page: Page):
    page.padding = 0

<<<<<<< HEAD
    row = Row(wrap=True, run_spacing=80, scroll=True)
    for i in range(20):
        row.controls.append(
=======
    # top_area = Row([Text("第一个显示区域"), Text("第一个显示区域")])
    # lvs = ListView(expand=1, spacing=10, padding=20)
    # grs = GridView(runs_count=3, spacing=30)

    lv = Row(expand=True, spacing=50, wrap=True, run_spacing=20, scroll=True)
    for i in range(100):
        lv.controls.append(
>>>>>>> 4414a9434d1f972856e17492e48ab113aaec2755
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
<<<<<<< HEAD
        controls=[m, next_btn],
=======
        controls=[lv, next_btn],
>>>>>>> 4414a9434d1f972856e17492e48ab113aaec2755
        expand=True,
    )

    page.add(c)


app(target=main, assets_dir="assets")
