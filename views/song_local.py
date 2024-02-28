from typing import Optional
import flet as ft
from flet import Stack, Text, Container, ElevatedButton, Row, icons, colors
import os
from methods.getlocal import DataSong, LocalSong


# 点击 1.播放歌曲 2.更新page.overlay内容 3.更改index
#
class Song(Container):
    def __init__(self, song: DataSong, songItemClick):

        self.song: DataSong = song
        self.songItemClick = songItemClick
        self.cover = ft.Image(
            width=40, height=40, border_radius=10, fit="cover", src=song.cover
        )
        if song.isLocal:
            # a_info = TinyTag.get(song.url, image=True)
            # img = a_info.get_image()
            if song.cover != "album.png":
                self.cover.src_base64 = song.cover
            # if img:
            #     img64 = byte_to_base64(img)
            #     self.cover.src_base64 = img64
        self.name = Text(
            song.name,
            width=100,
            height=20,
            weight="bold",
            color=ft.colors.WHITE,
            tooltip=song.name,
        )
        self.singer = Text(
            song.singer,
            width=80,
            height=20,
            no_wrap=True,
            weight="bold",
            color=ft.colors.WHITE,
            tooltip=song.singer,
        )

        super(Song, self).__init__(
            content=Row([self.cover, self.name, self.singer], spacing=10),
            on_click=self.clickIt,  # 点击操作
            bgcolor=ft.colors.BLUE_GREY_300,
            padding=5,
            opacity=0.7,
            animate=300,
            border_radius=10,
            border=ft.border.all(width=1),
            width=340,
            margin=ft.margin.only(right=10, left=10),
        )
        self.__selected = False

    @property
    def selected(self):
        return self.__selected

    @selected.setter
    def selected(self, value: bool):
        self.__selected = value
        if value is True:  # 接受按钮点击后执行
            self.bgcolor = colors.BLUE_GREY_700
            self.opacity = 1
            self.update()
            self.songItemClick(self.song)  # 点击操作 AudioInfo.play_music(songItem)
        else:
            self.bgcolor = colors.BLUE_GREY_300
            self.opacity = 0.7
            self.update()

    # 点击操作
    def clickIt(self, e):
        self.selected = True

    def un_select(self):
        self.selected = False


# 继承audio控件,添加song以及during 歌曲时长属性
class PlayAudio(ft.Audio):
    def __init__(self, song: DataSong, *args, **kwargs):
        self.song = song
        self.during: Optional[int] = None
        super(PlayAudio, self).__init__(*args, **kwargs)

    def update_during(self, during):
        self.during = during


class ViewPage(Stack):
    def __init__(self, page, songItemClick):
        self.page = page
        self.songItemClick = songItemClick
        self.songs = []
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.page.overlay.append(self.pick_files_dialog)
        self.song_list = ft.GridView(
            expand=1,
            spacing=30,
            child_aspect_ratio=8,
            max_extent=page.window_width // 3,
            padding=10,
        )
        self.panel = Container(
            margin=ft.margin.only(left=10, top=10),
            content=ft.Column(
                controls=[
                    Row(
                        controls=[
                            ElevatedButton(
                                "添加音乐",
                                icon=icons.FILE_OPEN,
                                on_click=lambda _: self.pick_files_dialog.get_directory_path(),
                            ),
                            ElevatedButton(
                                "清 空", icon=icons.CLEAR, on_click=self.clear_list
                            ),
                        ],
                        spacing=20,
                    ),
                    self.song_list,
                ],
                alignment=ft.alignment.top_left,
            ),
        )

        super(ViewPage, self).__init__(
            controls=[self.panel],
            expand=True,
        )

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        songPath = e.path if e.path else None
        if songPath != None:
            self.songs = LocalSong.getFiles(songPath)
            for song in self.songs:
                self.song_list.controls.append(Song(song, self.songItemClick))

            self.page.update()

    def init_event(self):
        print("local start")

    def clear_list(self, e):
        self.song_list.clean()
