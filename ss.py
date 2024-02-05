import flet
from flet import (
    Stack,
    Text,
    Page,
    Column,
    Row,
    TextField,
    FloatingActionButton,
    colors,
    Image,
    Container,
    border,
    ResponsiveRow,
    Card,
    Divider,
    MainAxisAlignment,
    margin,
    ListTile,
    Icon,
    icons,
)

from methods.getmusic import HIFINI, DataSong
from utils import snack_bar


class Song(Container):
    def __init__(self, song: DataSong, select_callback):
        self.song: DataSong = song
        self.select_callback = select_callback
        self.photo = Image(
            src=song.photo_url,
            width=40,
            height=40,
            border_radius=10,
            fit="cover",
        )
        self.music = Text(
            song.music_name,
            width=200,
            height=20,
            weight="bold",
            color=colors.WHITE,
            tooltip=song.music_name,
        )
        self.singer = Text(
            song.singer_name,
            width=80,
            height=20,
            no_wrap=True,
            weight="bold",
            color=colors.WHITE,
            tooltip=song.singer_name,
        )
        super(Song, self).__init__(
            content=Row([self.photo, self.music, self.singer], spacing=10),
            on_click=self.on_click,
            bgcolor=colors.BLACK,
            padding=5,
            opacity=0.7,
            animate=300,
            border_radius=10,
            border=border.all(width=1),
            width=340,
            margin=margin.only(right=10, left=10),
        )
        self.__selected = False

    @property
    def selected(self):
        return self.__selected

    @selected.setter
    def selected(self, value: bool):
        self.__selected = value
        if value is True:
            self.container.bgcolor = colors.BLUE_GREY_700
            self.container.opacity = 1
            self.update()
            self.select_callback(self)
        else:
            self.container.bgcolor = colors.BLUE_GREY_300
            self.container.opacity = 0.7
            self.update()

    def on_click(self, e):
        self.selected = True

    def un_select(self):
        self.selected = False


class SearchCompoment(Row):
    def __init__(self, search_callback):
        self.music_api = HIFINI
        self.search_callback = search_callback
        self.search_input = TextField(
            label="请输入歌曲名称或歌手名称",
            width=300,
            height=40,
            on_submit=self.search,
        )
        self.submit_btn = FloatingActionButton(
            "搜索", on_click=self.search, height=40, width=80, autofocus=True
        )
        super(SearchCompoment, self).__init__(
            controls=[self.search_input, self.submit_btn],
            alignment="center",
            vertical_alignment="center",
        )

    # 执行这里
    def search(self, e):
        self.search_callback(self.search_input.value)


class MusicList(Container):
    def __init__(self, select_callback):
        self.select_callback = select_callback
        # row([])
        self.list = Row(wrap=True, spacing=85, run_spacing=40, expand=True)
        super(MusicList, self).__init__(content=self.list)

    def set_musics(self, data: DataSong, first=False):
        if first:
            self.list.controls.clear()  # 清空列表
        self.list.controls.append(
            Song(data, self.middle_select_callback)
        )  # 加进ListView
        self.update()

    def middle_select_callback(self, song: Song):
        for _song in self.list.controls:
            if _song.selected:
                if _song != song:
                    _song.un_select()
        self.select_callback(song)


class SearchSection(Row):
    def __init__(self, parent: "ViewPage"):
        self.parent = parent
        self.music_list = MusicList(self.parent.select_callback)
        self.search_content = SearchCompoment(self.parent.search_callback)
        super(SearchSection, self).__init__(
            controls=[self.music_list],
            wrap=True,
            scroll=True,
            expand=True,
        )


class AudioInfo(Container):
    def __init__(self):
        self.audio_name = Text("无题", size=18)
        self.audio_singer = Text("佚名", size=14)

        self.info = ListTile(
            leading=Image(width=100, height=100, src="imgs/taichi.svg"),
            title=self.audio_name,
            subtitle=self.audio_singer,
        )
        super(AudioInfo, self).__init__(
            content=self.info,
            margin=margin.Margin(0, 0, 0, 100),
        )


class PlaySection(Column):
    def __init__(self, parent):
        self.parent = parent
        self.audio_info = AudioInfo()
        self.row = Row(controls=[self.audio_info])
        self.tx = Container(
            self.row,
            bgcolor=colors.AMBER_100,
            border=border.only(top=border.BorderSide(1, "grey")),
        )

        super(PlaySection, self).__init__(
            controls=[self.tx],
            alignment="end",
        )


class ViewPage(Stack):
    def __init__(self, page):
        self.music_api = HIFINI
        self.top_widget = SearchSection(self)
        self.bottom_widget = PlaySection(self)
        super(ViewPage, self).__init__(
            controls=[self.top_widget, self.bottom_widget], expand=True
        )
        self.page = page

    def init_event(self):
        if not self.top_widget.music_list.list.controls:
            self.top_widget.search_content.search(None)

    def select_callback(self, song: Song):
        print("print ")

    def search_callback(self, target):  # 执行
        flag = False
        for song in self.music_api.search_musics(target):  # 1/ 循环歌曲添加进布局中..
            if isinstance(song, tuple):
                snack_bar(self.page, f"音乐api出错: {song[1]}")
                return
            else:  # 是否第一次
                if not flag:
                    self.top_widget.music_list.set_musics(song, first=True)
                    flag = True
                else:
                    self.top_widget.music_list.set_musics(song)


def main(page: Page):
    # Page.window_width
    page.title = "播放器"
    page.padding = 0
    t = ViewPage(page)
    page.add(t)
    t.init_event()


flet.app(target=main, assets_dir="assets")
