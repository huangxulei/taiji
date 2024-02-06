from flet import *


def main(page: Page):
    page.title = "上中下布局"
    page.padding = 0

    top = Container(
        bgcolor=colors.AMBER,
        height=100,
        border=border.only(bottom=border.BorderSide(2, "black")),
    )
    crow = Row(
        controls=[Text("中间自适应高度,设置expand=1")],
        alignment="center",
    )
    center = Container(
        content=crow,
        expand=1,
        # 全部边框
        border=border.all(10, colors.PINK_600),
    )
    bottom = Container(
        bgcolor=colors.BLUE,
        height=100,
        # 设置顶部边框颜色和宽度
        border=border.only(top=border.BorderSide(2, "black")),
    )
    # spacing = 0 为子元素的之间的空隙为0
    col = Column([top, center, bottom], expand=True, spacing=0)

    page.add(col)


app(target=main)
