import flet as ft

# 用于是否显示右边栏的辅助变量
rightFlag = False


def main(page: ft.Page):
    page.title = "上中下布局"
    page.padding = 0
    page.window_width = 500
    page.window_height = 600

    top = ft.Container(
        bgcolor=ft.colors.AMBER,
        height=100,
        border=ft.border.only(bottom=ft.border.BorderSide(2, "black")),
    )
    crow = ft.Row(
        controls=[ft.Text("中间自适应高度,设置expand=1")],
        alignment="center",
    )
    center = ft.Container(
        content=crow,
        expand=1,
        # 全部边框
        border=ft.border.all(10, ft.colors.PINK_600),
    )

    top_widget = ft.Container(
        bgcolor=ft.colors.YELLOW,
        content=ft.Column(
            controls=[
                ft.Row(
                    [
                        ft.Container(width=300, content=ft.Text("这是一段文字")),
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
        ),
        expand=True,
        visible=False,
        margin=ft.margin.only(bottom=100),
    )

    def showTop(e):
        if top_widget.visible:
            top_widget.visible = False
        else:
            top_widget.visible = True
        page.update()

    right_width = ft.Container(
        bgcolor=ft.colors.GREEN_100,
        width=100,
        height=300,
        content=ft.Text("右边栏"),
        offset=ft.transform.Offset(4, 0),
        bottom=100,
        right=10,
    )

    page.overlay.append(right_width)

    def showRight(e):
        global rightFlag
        if rightFlag:
            print("隐藏")
            rightFlag = False
            right_width.offset = ft.transform.Offset(4, 0)
        else:
            print("显示")
            rightFlag = True
            right_width.offset = ft.transform.Offset(0, 0)
        right_width.update()

    top_btn = ft.IconButton(
        icon=ft.icons.ARROW_DROP_UP,
        icon_size=20,
        tooltip="显示上面一个布局",
        on_click=showTop,
    )

    right_btn = ft.IconButton(
        icon=ft.icons.ARROW_RIGHT,
        icon_size=20,
        tooltip="显示右边一个布局",
        on_click=showRight,
    )

    bottom = ft.Container(
        bgcolor=ft.colors.GREY_100,
        height=100,
        # 设置顶部边框颜色和宽度
        border=ft.border.only(top=ft.border.BorderSide(2, "black")),
        content=ft.Row(controls=[top_btn, right_btn]),
    )

    col = ft.Column([center, bottom], expand=True, spacing=0)

    st = ft.Stack(
        controls=[top, col, top_widget],
        expand=True,
    )

    page.add(st)


ft.app(target=main)
