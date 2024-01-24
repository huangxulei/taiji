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
)

from methods.getimages import CiYuanDao, APIS
from utils import snack_bar


class ViewPage(Stack):
    def __init__(self, page: Page):
        self.page = page
        self.urls = {k: {"index": -1, "values": []} for k in APIS}
        self.resource_select = Dropdown(
            text_size=10,
            width=80,
            height=50,
            content_padding=10,
            value=list(APIS.keys())[0],
            options=[dropdown.Option(k) for k in APIS],
        )
        self.content_area = Container(
            margin=10, alignment=alignment.center, expand=True
        )

        super(ViewPage, self).__init__(controls=[self.content_area], expand=True)

        self.generators = {k: v.image_url_generator() for k, v in APIS.items()}

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
