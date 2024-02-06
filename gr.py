from flet import *


def main(page: Page):
    page.padding = 0
    page.scroll

    def getImgSrc(i):
        return f"https://picsum.photos/200/200?{i}"

    grs = Row(
        wrap=True,
        scroll=ScrollMode.ALWAYS,
        expand=1,
        run_spacing=30,
    )

    for i in range(1, 200):
        grs.controls.append(
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
                            f"title{i}",
                            width=180,
                            height=20,
                            weight="bold",
                            color=colors.WHITE,
                        ),
                        Text(
                            f"writer{i}",
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
                margin=margin.only(right=60, left=10),
            ),
        )

    page.add(grs)


app(target=main)
