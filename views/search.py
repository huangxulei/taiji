import flet
from flet import Stack, Text


class ViewPage(Stack):
    def __init__(self, page):
        self.page = page
