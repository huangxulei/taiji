import flet
from flet import Stack, Text


class ViewPage(Stack):
    def __init__(self, page, songItemClick):
        self.tx = Text("我的列表")
        self.songItemClick = songItemClick
        self.page = page
        super(ViewPage, self).__init__(
            controls=[self.tx],
            expand=True,
        )

    def init_event(self):
        print("mylist start")
