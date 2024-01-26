from flet import (
    Container,
    Stack,
    FloatingActionButton,
    Row,
    alignment,
    Column,
    Image,
    Page,
    margin,
    icons,
    Dropdown,
    dropdown,
    MainAxisAlignment,
    colors,
)

from methods.getimages import APIS
from utils import download_named_image, snack_bar


class ViewPage(Stack):
    def __init__(self, page: Page):
        self.page = page
        self.urls = {k: {"index": -1, "values": []} for k in APIS}
        self.resource_select = Dropdown(
            text_size=10,
            width=200,
            height=50,
            content_padding=10,
            value=list(APIS.keys())[0],
            options=[dropdown.Option(k) for k in APIS],
            on_change=self.fresh_image,
            border_color=colors.BLUE_500,
            border_width=2,
        )
        self.content_area = Container(
            margin=10, alignment=alignment.center, expand=True
        )
        self.next_btn = Column(
            [
                Row(
                    [
                        Container(
                            FloatingActionButton(
                                icon=icons.SKIP_PREVIOUS,
                                on_click=self.back_look_image,
                                width=30,
                                height=30,
                                tooltip="上一张",
                            ),
                        ),
                        Container(
                            FloatingActionButton(
                                icon=icons.SKIP_NEXT,
                                on_click=self.fresh_image,
                                width=30,
                                height=30,
                                tooltip="下一张",
                            ),
                        ),
                        Container(
                            FloatingActionButton(
                                icon=icons.DOWNLOAD,
                                on_click=self.save_img,
                                width=30,
                                height=30,
                                tooltip="下载",
                            ),
                        ),
                    ],
                )
            ],
            opacity=0.8,
            animate_opacity=300,
        )

        super(ViewPage, self).__init__(
            controls=[
                self.content_area,
                Container(self.resource_select, top=10, left=10),
                Container(
                    self.next_btn,
                    width=150,
                    height=40,
                    bottom=10,
                    right=20,
                    bgcolor=colors.BLUE_GREY_100,
                    padding=5,
                    border_radius=10,
                ),
            ],
            expand=True,
        )
        #
        self.generators = {k: v.image_url_generator() for k, v in APIS.items()}

    def init_event(self):
        if self.content_area.content is None:
            self.fresh_image(None)

    def fresh_image(self, e):
        self.page.splash.visible = True
        self.page.update()
        try:
            _type = self.resource_select.value  # 获取网站地址
            img_url = next(self.generators[_type])

            self.urls[_type]["values"].append(img_url)
            self.urls[_type]["index"] += 1
            self.content_area.content = Image(
                src=self.urls[_type]["values"][self.urls[_type]["index"]]
            )
            self.update()
        except Exception as e:
            snack_bar(self.page, f"获取失败: {e}")
        self.page.splash.visible = False
        self.page.update()

    def back_look_image(self, e):
        self.page.splash.visible = True
        self.page.update()
        try:
            _type = self.resource_select.value
            self.urls[_type]["index"] -= 1
            if self.urls[_type]["index"] >= 0:
                self.content_area.content = Image(
                    src=self.urls[_type]["values"][self.urls[_type]["index"]]
                )
                self.update()
        except Exception as e:
            snack_bar(self.page, f"获取失败: {e}")
        self.page.splash.visible = False
        self.page.update()

    def save_img(self, e):
        try:
            _type = self.resource_select.value
            _index = self.urls[_type]["index"]
            if _index >= 0:
                f = download_named_image(
                    self.urls[_type]["values"][self.urls[_type]["index"]]
                )
                snack_bar(self.page, f"{f}已保存")
        except Exception as e:
            snack_bar(self.page, f"保存失败: {e}")

    def btn_opacity(self, e):
        if self.next_btn.opacity == 0.5:
            self.next_btn.opacity = 0.05
        else:
            self.next_btn.opacity = 0.5
        self.update()

    def back_btn_opacity(self, e):
        if self.back_look_btn.opacity == 1:
            self.back_look_btn.opacity = 0.8
        else:
            self.back_look_btn.opacity = 1
        self.update()
