from importlib import import_module

try:
    from views import index, mountain, rain
except:
    pass

import flet
from flet import Tabs, Tab, Page, Stack, ProgressBar
from settings import navigation_tabs


class NavigationBar(Stack):
    def __init__(self, page: Page):
        self.page = page
        self.tabs = Tabs(expand=1, selected_index=0)
        self.tabs_list = []
        for navigation in navigation_tabs:
            content = self.get_page(navigation[2])  # 内容
            if not content:
                continue
            icon = navigation[0]
            text = navigation[1]
            self.tabs_list.append(Tab(content=content, icon=icon, text=text))
        self.tabs.tabs.extend(self.tabs_list)
        self.tabs.on_change = lambda e: self.tab_init_event(e.data)  # 点击后的执行
        super(NavigationBar, self).__init__(controls=[self.tabs], expand=True)

    def tab_init_event(self, index):
        index = int(index)
        if hasattr(self.tabs_list[index].content, "init_event"):
            getattr(self.tabs_list[index].content, "init_event")()

    def get_page(self, module_name):
        try:
            module_file = import_module("views." + module_name)
            return module_file.ViewPage(self.page)
        except Exception as e:
            print("getpage", e)


def main(page: Page):
    page.title = "flet"
    progress_bar = ProgressBar(visible=False)
    page.splash = progress_bar
    t = NavigationBar(page)
    page.add(t)


flet.app(target=main, assets_dir="assets")
