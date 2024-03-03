import flet as ft
from flet import Stack, Text, Container, ElevatedButton, Row, icons, colors
from methods.getlocal import DataSong, LocalSong


# 点击 1.播放歌曲 2.更新page.overlay内容 3.更改index
class Song(Container):
    def __init__(self, song: DataSong, song_list, songItemClick):

        self.song: DataSong = song
        self.song_list = song_list
        self.songItemClick = songItemClick
        self.cover = ft.Image(
            width=40, height=40, border_radius=10, fit="cover", src=song.cover
        )
        if song.isLocal:
            if song.cover != "album.png":
                self.cover.src_base64 = song.cover
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
            # 循环所有子项
            for _song in self.song_list.controls:
                if _song.selected:  # 如果子项之前被点击
                    if _song != self:  # 如果不是当前
                        _song.un_select()
            self.songItemClick(self.song)

        else:
            self.bgcolor = colors.BLUE_GREY_300
            self.opacity = 0.7
            self.update()

    # 点击操作
    def clickIt(self, e):
        self.selected = True

    def un_select(self):
        self.selected = False


class ViewPage(Stack):
    def __init__(self, page, songItemClick, playAll):
        self.page = page
        self.songItemClick = songItemClick
        self.playAll = playAll
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
        self.add_btn = ElevatedButton(
            "添加音乐",
            icon=icons.FILE_OPEN,
            on_click=lambda _: self.pick_files_dialog.get_directory_path(),
        )
        self.clean_btn = ElevatedButton(
            "清 空",
            icon=icons.CLEAR,
            on_click=self.clear_list,
            disabled=True,
        )
        self.playall_btn = ElevatedButton(
            "播放所有",
            icon=icons.PLAYLIST_PLAY,
            on_click=self.play_all,
            disabled=True,
        )

        self.panel = Container(
            margin=ft.margin.only(left=10, top=10),
            content=ft.Column(
                controls=[
                    Row(
                        controls=[self.add_btn, self.clean_btn, self.playall_btn],
                        spacing=20,
                    ),
                    Row(
                        controls=[self.song_list],
                        spacing=10,
                        expand=True,
                    ),
                ],
                alignment=ft.alignment.top_left,
            ),
        )
        super(ViewPage, self).__init__(
            controls=[self.panel],
            expand=True,
        )

    def play_all(self, e):
        self.playAll(self.song_list)

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        songPath = e.path if e.path else None
        if songPath != None:
            self.songs = LocalSong.getFiles(songPath)
            for song in self.songs:
                self.song_list.controls.append(
                    Song(song, self.song_list, self.songItemClick)
                )
            self.setBtn(True)
            self.page.update()

    def init_event(self):
        print("local start")

    def clear_list(self, e):
        self.song_list.clean()
        self.setBtn(False)
        self.update()

    def setBtn(self, flag):
        if flag:
            self.clean_btn.disabled = False
            self.playall_btn.disabled = False
        else:
            self.clean_btn.disabled = True
            self.playall_btn.disabled = True

    # def playAll(self, e: ElevatedButton):
    #     if self.song_list.controls:
    #         self.play_all(self.song_list.controls)
    # 添加所有
