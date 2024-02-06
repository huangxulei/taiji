from flet import *


def main(page: Page):
    page.padding = 0
    page.title = "黄老五 播放器"

    def getImgSrc(i):
        return f"https://picsum.photos/200/200?{i}"

    top_row = Row(
        [
            ElevatedButton(
                "探索",
                icon=icons.SEARCH,
            ),
            ElevatedButton(
                "我的歌单",
                icon=icons.LIST,
            ),
            ElevatedButton(
                "本地歌曲",
                icon=icons.LOCAL_ACTIVITY,
            ),
        ]
    )
    top = Container(
        padding=5,
        content=top_row,
        height=50,
    )

    center = Container(
        expand=1,
    )
    bottom = Container(
        bgcolor=colors.BLUE,
        height=100,
        border=border.only(top=border.BorderSide(1, "black")),
    )

    row_list = Row(
        scroll=ScrollMode.ALWAYS, expand=True, wrap=True, spacing=0, run_spacing=10
    )

    for i in range(1, 51):
        row_list.controls.append(
            Container(
                content=Row(
                    [
                        Image(
                            src=getImgSrc(i),
                            width=40,
                            height=40,
                            fit="cover",
                            border_radius=10,
                        ),
                        Text(
                            f"歌曲名字{i}",
                            width=180,
                            height=20,
                            weight="bold",
                            color=colors.WHITE,
                        ),
                        Text(
                            f"歌手{i}",
                            width=80,
                            height=20,
                            no_wrap=True,
                            weight="bold",
                            color=colors.WHITE,
                        ),
                    ]
                ),
                bgcolor=colors.BLACK,
                padding=5,
                opacity=0.7,
                animate=300,
                border_radius=10,
                border=border.all(width=1),
                width=320,
                margin=margin.only(right=90, left=10, top=10, bottom=10),
            ),
        )
    center.content = row_list

    c = Column([top, center, bottom], expand=True, spacing=0)

    page.add(c)


app(target=main)
