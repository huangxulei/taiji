import flet
from flet import Stack, Text


class ViewPage(Stack):
    def __init__(self, page):
        self.tx = Text("本地")
        self.page = page
        super(ViewPage, self).__init__(
            controls=[self.tx],
            expand=True,
        )

    def init_event(self):
        print("local start")
