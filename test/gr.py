from flet import *


def main(page: Page):
    page.padding = 0

    grs = GridView(runs_count=3, spacing=10, auto_scroll=True)

    ListTile_Item = ListTile(
        leading=Image(src="../assets/imgs/taichi.svg"),
        title=Text("最好是名字"),
        subtitle=Text("作者"),
    )

    item = Container(
        content=ListTile_Item,
        # height=50,
        # width=200,
        border=border.all(10, colors.PINK_600),
    )
    # item = Text("测试,,,,")
    for i in range(40):
        grs.controls.append(item)

    page.add(grs)


app(target=main, assets_dir="assets")
