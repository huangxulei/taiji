from typing import Optional
import flet as ft
from flet import Text, Container, Column, Row, IconButton, Icon, Image, colors, icons

from importlib import import_module
from methods.getlocal import DataSong
from settings import song_tabs

gl = {"index": 0, "state": "", "song_list": [], "volume": 0.5}


# 继承audio控件,添加song以及during 歌曲时长属性
class PlayAudio(ft.Audio):
    def __init__(self, song: DataSong, *args, **kwargs):
        self.song = song
        self.during: Optional[int] = None
        super(PlayAudio, self).__init__(*args, **kwargs)

    def update_during(self, during):
        self.during = during


# 音乐显示控制栏
class AudioInfo(Container):
    def __init__(self, page):
        self.page = page
        self.playing_audio: Optional[PlayAudio] = None
        self.song: Optional[DataSong] = None
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
            # on_change=self.ld_change,
        )
        self.play_btn = IconButton(
            icon=icons.PLAY_CIRCLE,
            selected_icon=icons.PAUSE_CIRCLE,
            # on_click=self.toggle_play,
            icon_size=40,
        )
        self.volume_icon = Icon(name=icons.VOLUME_DOWN)
        self.song_cover = Image(
            src=f"assets/album.png",
            width=90,
            height=90,
            fit=ft.ImageFit.CONTAIN,
            rotate=ft.transform.Rotate(0, alignment=ft.alignment.center),
            animate_rotation=ft.animation.Animation(
                300, ft.AnimationCurve.EASE_IN_CIRC
            ),
        )
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
                                        # on_click=self.previous_track,
                                    ),
                                    self.play_btn,
                                    IconButton(
                                        icon=icons.SKIP_NEXT,
                                        icon_size=40,
                                        # on_click=self.next_track,
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
                                        # on_change=self.volume_change,
                                    ),
                                    IconButton(
                                        icon=icons.PLAYLIST_ADD_ROUNDED,
                                        # on_click=lambda _: pick_files_dialog.pick_files(
                                        #     allow_multiple=True,
                                        #     file_type=FilePickerFileType.AUDIO,
                                        # ),
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

    def play_music(self, song: DataSong):
        print(song)
        self.playing_audio = PlayAudio(
            song=song,
            src=song.url,
            autoplay=True,
        )
        self.page.overlay.append(self.playing_audio)
        self.page.update()
        self.playing_audio.autoplay = False
        self.play_btn.selected = True
        self.playing_audio.play()
        self.song_slider.value = "0"


class NavigationBar(ft.Stack):
    def __init__(self, page: ft.Page, songItemClick):
        self.page = page
        self.songItemClick = songItemClick
        self.tabs = ft.Tabs(expand=1)
        self.tabs_list = []
        for navigation in song_tabs:
            content = self.get_page(navigation[1])  # 内容
            if not content:
                continue
            text = navigation[0]
            self.tabs_list.append(ft.Tab(content=content, text=text))
        self.tabs.tabs.extend(self.tabs_list)
        self.tabs.on_change = lambda e: self.tab_init_event(e.data)  # 点击后的执行
        super(NavigationBar, self).__init__(
            controls=[
                self.tabs,
            ],
            expand=True,
        )

    def tab_init_event(self, index):
        index = int(index)
        if hasattr(self.tabs_list[index].content, "init_event"):
            getattr(self.tabs_list[index].content, "init_event")()

    def get_page(self, module_name):
        try:
            module_file = import_module("views." + module_name)
            return module_file.ViewPage(self.page, self.songItemClick)
        except Exception as e:
            print("getpage", e)


class ViewPage(ft.Stack):
    global gl

    def __init__(self, page):
        self.is_first = True
        self.page = page
        self.t = NavigationBar(page, self.songItemClick)
        self.b = AudioInfo(page)
        self.c = Column([self.t, self.b], expand=True, spacing=0)
        super(ViewPage, self).__init__(
            controls=[self.c],
            expand=True,
        )

    # 获取子项点击后的操作
    def songItemClick(self, song: DataSong):
        self.b.play_music(song)

    def init_event(self):  # 获取tabs第一页内容
        search_view = self.t.controls[0].tabs[0].content

        # if not search_view.right_widget.music_list.list.controls:
        #     search_view.right_widget.search_content.search(None)
