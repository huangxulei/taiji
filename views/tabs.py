from flet import Stack, Text, Tab, Tabs, Page
from importlib import import_module


class NavigationBar(Stack):
    def __init__(self, page: Page):
        self.page = page
        self.tabs = Tabs(expand=1)
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


class ViewPage(Stack):
    def __init__(self, page):
        self.page = page
        self.t = NavigationBar(page)
        super(ViewPage, self).__init__(
            controls=[self.t],
            expand=True,
        )
