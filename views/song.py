from flet import Stack, Text, Tab, Tabs, Page
from importlib import import_module
from settings import song_tabs


class NavigationBar(Stack):
    def __init__(self, page: Page):
        self.page = page
        self.tabs = Tabs(expand=1)
        self.tabs_list = []
        for navigation in song_tabs:
            content = self.get_page(navigation[1])  # 内容
            if not content:
                continue
            text = navigation[0]
            self.tabs_list.append(Tab(content=content, text=text))
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
        self.is_first = True
        self.page = page
        self.t = NavigationBar(page)
        super(ViewPage, self).__init__(
            controls=[self.t],
            expand=True,
        )

    def init_event(self):  # 获取tabs第一页内容
        search_view = self.t.controls[0].tabs[0].content
        print(search_view.info)

        if not search_view.right_widget.music_list.list.controls:
            search_view.right_widget.search_content.search(None)
