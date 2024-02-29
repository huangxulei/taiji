import flet as ft


class Song(ft.UserControl):
    def __init__(self, _i, lv):
        super().__init__()
        self._i = _i
        self.lv = lv
        self.btn = ft.ElevatedButton(
            text=self._i, on_click=self.ck, bgcolor=ft.colors.BLUE
        )

    def build(self):
        return self.btn

    # how can I get lv?
    def ck(self, e):
        for item in self.lv.controls:
            print(item.btn)
            item.btn.bgcolor = ft.colors.BLUE
            item.update()
        self.btn.bgcolor = ft.colors.AMBER_100
        self.update()


def main(page: ft.Page):
    page.title = "Auto-scrolling ListView"

    lv = ft.ListView(expand=1, spacing=10, padding=20)

    for i in range(0, 3):
        lv.controls.append(Song(i, lv))

    page.add(lv)


ft.app(target=main)
