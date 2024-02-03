import flet
from flet import Stack, Text, Page


# 结构性
class ViewPage(Stack):
    def __init__(self, page):  # self为ViewPage类本身,作为引用
        self.page = page  # self.xx 添加属性
        self.tx = Text("显示内容")
        super(ViewPage, self).__init__(controls=[self.tx], expand=True)

    def fun(self):  # 给类添加方法
        pass


def main(page: Page):
    page.title = "flet"
    t = Text("显示内容")
    page.add(t)


flet.app(target=main, assets_dir="assets")
