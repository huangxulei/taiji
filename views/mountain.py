
from flet import Container, alignment, animation, transform, Stack, Text

class ViewPage(Stack):
    def __init__(self, page):
        self.page = page

        self.t = Text('山脉')
        super(ViewPage,self).__init__(
            controls=[self.t],
            expand=True,
        )
