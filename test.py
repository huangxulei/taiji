import flet as ft
from flet import Text, Container, Column, Row, IconButton, Icon, Image, colors, icons


# 音乐显示控制栏
class AudioInfo(Container):
    def __init__(self, page, showCont):
        self.page = page
        self.showCont = showCont
        self.is_sliding = False
        self.song_name = Text("")
        self.song_artist = Text("")
        self.current_time = Text(value="00:00")
        self.total_time = Text(value="00:00")
        self.song_slider = ft.Slider(
            width=400,
            value="0",
            height=8,
            min=0,
            max=100,
            divisions=100,
            label="{value}%",
        )
        self.play_btn = IconButton(
            icon=icons.PLAY_CIRCLE,
            selected_icon=icons.PAUSE_CIRCLE,
            icon_size=40,
        )
        self.volume_icon = Icon(name=icons.VOLUME_DOWN)
        self._img = Image(
            src=f"assets/album.png",
            width=90,
            height=90,
            fit=ft.ImageFit.CONTAIN,
        )

        self.song_cover = ft.Container(content=self._img, on_click=self.showCont[0])
        self.cont = Container(
            content=Row(
                controls=[
                    self.song_cover,
                    Container(
                        width=180,
                        height=70,
                        content=ft.ListTile(
                            leading=Icon(icons.MUSIC_NOTE_ROUNDED),
                            title=self.song_name,
                            subtitle=self.song_artist,
                        ),
                    ),
                    Column(
                        [
                            Row(
                                [
                                    self.current_time,
                                    self.song_slider,
                                    self.total_time,
                                ],
                            ),
                            Row(
                                [
                                    IconButton(
                                        icon=icons.SKIP_PREVIOUS,
                                        icon_size=40,
                                    ),
                                    self.play_btn,
                                    IconButton(
                                        icon=icons.SKIP_NEXT,
                                        icon_size=40,
                                    ),
                                    self.volume_icon,
                                    ft.Slider(
                                        width=150,
                                        active_color=colors.WHITE60,
                                        min=0,
                                        max=100,
                                        divisions=100,
                                        value=50,
                                        label="{value}",
                                    ),
                                    IconButton(
                                        icon=icons.PLAYLIST_PLAY,
                                        on_click=self.showCont[1],
                                    ),
                                ],
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ]
            ),
            padding=10,
            width=800,
        )
        super(AudioInfo, self).__init__(
            content=self.cont,
            height=105,
            alignment=ft.alignment.center,
            border_radius=20,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[colors.YELLOW_100, colors.BLUE_50],
            ),
        )


class ViewPage(ft.Stack):

    def __init__(self, page: ft.Page):
        self.is_first = True
        self.page = page
        # tabs
        self.ta = ft.Tabs(
            expand=True,
            selected_index=0,
            tabs=[
                ft.Tab(text="本地歌曲", content=Text("本地歌曲")),
                ft.Tab(text="我的歌单", content=Text("我的歌单")),
            ],
        )

        # 歌词
        self.lrc = ft.Container(
            bgcolor=ft.colors.GREY_200,
            content=Column(
                controls=[
                    Row(
                        [
                            Image(width=300, height=300, src="album.png"),
                            Container(
                                width=300, content=Text("歌词显示::::333333333333")
                            ),
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
            ),
            margin=ft.margin.only(bottom=105),
            visible=False,
        )

        self.song_list = ft.ListView(width=200, spacing=10)

        for i in range(10):
            self.song_list.controls.append(ft.Text(f"{i+1} 、第{i+1}首歌曲 "))
        self.page.update()

        self.song_cont = ft.Container(
            content=self.song_list,
            right=10,
            bottom=110,
            bgcolor=ft.colors.AMBER_200,
            offset=ft.transform.Offset(2, 0),
        )
        # 播放控制, 传递两个函数 显示歌词和播放列表
        self.ctr = AudioInfo(page, [self.showLrc, self.showSonglist])
        self.c = Column([self.ta, self.ctr], expand=True, spacing=0)
        super(ViewPage, self).__init__(
            controls=[self.c, self.lrc, self.song_cont],
            expand=True,
        )

    def showLrc(self, e):
        self.lrc.visible = not self.lrc.visible
        self.page.update()

    def showSonglist(self, e):
        offx = self.song_cont.offset.x
        if offx == 2:
            print("显示", offx)
            self.song_cont.offset = ft.transform.Offset(0, 0)
        else:
            print("隐藏", offx)
            self.song_cont.offset = ft.transform.Offset(2, 0)
        self.song_cont.update()


def main(page: ft.Page):
    page.padding = 0
    v = ViewPage(page)

    page.add(v)


ft.app(target=main)
