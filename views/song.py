from typing import Optional
import flet as ft
from flet import Text, Container, Column, Row, IconButton, Icon, Image, colors, icons

from importlib import import_module
from methods.getlocal import DataSong
from settings import song_tabs
from utils import ms_to_time
from tinytag import TinyTag
from .my_list import ViewPage as MyList
from .song_local import ViewPage as SongList
from functools import partial

gl = {"index": 1, "state": "", "song_list": [], "volume": 0.5}


# 继承audio控件,添加song以及during 歌曲时长属性
class PlayAudio(ft.Audio):
    def __init__(self, song: DataSong, *args, **kwargs):
        self.song = song
        self.during: Optional[int] = None
        super(PlayAudio, self).__init__(*args, **kwargs)

    def update_during(self, during):
        self.during = during


# 播放列表类
class audioTile(ft.UserControl):
    def __init__(self, page, song: DataSong, _index, duration):
        super().__init__()
        self.page = page
        self.song = song
        self._index = _index
        self.index_text = Text(f"{_index}、", width=20)
        self.name_text = Text(song.name, width=100, no_wrap=True)
        self.singer_text = Text(song.singer, width=50, no_wrap=True)
        self.duration_text = Text(duration, width=40, no_wrap=True)

    def build(self):
        return ft.Row(
            controls=[
                self.index_text,
                self.name_text,
                self.singer_text,
                self.duration_text,
                ft.IconButton(
                    icon=ft.icons.PLAY_CIRCLE_FILLED_OUTLINED,
                    on_click=self.playSong,
                ),
                ft.IconButton(
                    icon=ft.icons.DELETE_FOREVER,
                    on_click=self.playSong,
                ),
            ],
            width=300,
        )

    def playSong(self, e):
        self.page.overlay[gl["index"]].release()
        self.page.overlay[gl["index"]].update()
        gl["index"] = self._index


# 音乐显示控制栏
class AudioInfo(Container):
    def __init__(self, page, showCont):
        self.page = page
        self.showCont = showCont
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
            on_change=self.ld_change,
        )
        self.play_btn = IconButton(
            icon=icons.PLAY_CIRCLE,
            selected_icon=icons.PAUSE_CIRCLE,
            on_click=self.toggle_play,
            icon_size=40,
        )
        self.volume_icon = Icon(name=icons.VOLUME_DOWN)
        self.song_img = Image(
            src=f"assets/album.png",
            width=90,
            height=90,
            fit=ft.ImageFit.CONTAIN,
        )

        self.song_cover = Container(content=self.song_img, on_click=self.showCont[0])

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
                                        on_click=self.previous_track,
                                    ),
                                    self.play_btn,
                                    IconButton(
                                        icon=icons.SKIP_NEXT,
                                        icon_size=40,
                                        on_click=self.next_track,
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
                                        on_change=self.volume_change,
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

    # 添加到overlay中,修改播放内容
    # songlist中的歌曲列表, overlay中的列表(播放列表)
    def play_music(self, song: DataSong):
        # 判断是否正式播放的歌曲
        # 获取播放
        print(f"播放{song.name}")
        if self.playing_audio and song == self.playing_audio.song:
            if gl["state"] == "playing":
                print(f"{song.name}同一首歌曲,并且正在播放,不做任何操作")
                pass
            else:
                print("同一首歌曲,没有播放,开启播放")
                self.play()
        else:
            self.set_Info(song)
            _index = self.isInOverlay(song)
            print(f"overlay中的索引{_index}")
            if _index == -1:
                print(f"新歌曲:{song.name}")
                if self.playing_audio:
                    self.playing_audio.release()
                self.playing_audio = PlayAudio(
                    song=song,
                    src=song.url,
                    autoplay=True,
                    on_duration_changed=self.during_changed,
                    on_position_changed=self.position_changed,
                    on_state_changed=self.check_state,
                )
                self.page.overlay.append(self.playing_audio)
                self.page.update()
                self.playing_audio.autoplay = False
                gl["index"] = len(self.page.overlay) - 1
            else:
                print("老歌曲")
                gl["index"] = _index
                self.playing_audio.release()
                self.playing_audio = self.page.overlay[_index]
            self.play()

    def play(self):
        if gl["state"] == "pause":
            self.playing_audio.resume()
        else:
            self.playing_audio.volume = gl["volume"]
            self.song_slider.value = "0"
            self.playing_audio.play()
        gl["state"] = "playing"
        self.play_btn.selected = True

    def play_new(self):
        # cover 处理
        _audio: PlayAudio = self.page.overlay[gl["index"]]
        _isLocal = _audio.song.isLocal
        if _isLocal:
            if _audio.song.cover != "album.png":
                self.song_img.src = None
                self.song_img.src_base64 = _audio.song.cover
            else:
                self.song_img.src_base64 = None
                self.song_img.src = "album.png"
        self.song_name.value = _audio.song.name
        self.song_artist.value = _audio.song.singer
        self.current_time.value = "00:00"
        self.total_time.value = ms_to_time(_audio.during)
        if gl["state"] == "playing":
            _audio.volume = gl["volume"]
            _audio.play()

    def previous_track(self, e):
        self.page.overlay[gl["index"]].release()
        self.page.overlay[gl["index"]].update()
        gl["index"] = gl["index"] - 1
        if gl["index"] == 0:
            gl["index"] = len(self.page.overlay) - 1
        self.play_new()
        self.page.update()

    def next_track(self, e):
        self.page.overlay[gl["index"]].release()
        self.page.overlay[gl["index"]].update()
        gl["index"] = gl["index"] + 1
        if gl["index"] == len(self.page.overlay):
            gl["index"] = 1
        self.play_new()
        self.page.update()

    def isInOverlay(self, song: DataSong):
        if len(self.page.overlay) > 0:
            for index, _playing_audio in enumerate(self.page.overlay[1:]):
                if _playing_audio.song.url == song.url:
                    return index + 1
        return -1

    def set_Info(self, song: DataSong):
        self.song_name.value = song.name
        self.song_artist.value = song.singer
        if song.isLocal:
            if song.cover != "album.png":
                self.song_img.src_base64 = song.cover
            else:
                self.song_img.src_base64 = None
                self.song_img.src = song.cover
        self.update()

    def check_state(self, e):
        if e.data == "completed":
            print("complete!")
            self.page.overlay[gl["index"]].release()
            self.page.overlay[gl["index"]].update()
            gl["index"] = gl["index"] + 1
            if gl["index"] == len(self.page.overlay):
                gl["index"] = 1
            self.play_new()
            self.play_btn.icon = icons.PAUSE_CIRCLE
            self.page.update()

    def during_changed(self, e):
        during = int(e.data)
        self.playing_audio.update_during(during)
        self.total_time.value = ms_to_time(during)
        self.update()

    def position_changed(self, e):
        during = self.page.overlay[gl["index"]].during
        if during:
            self.current_time.value = ms_to_time(int(e.data))
            self.song_slider.value = int(int(e.data) / during * 100)
            self.update()

    def ld_change(self, e):
        v = e.control.value  # 获取当前距离 v百分比
        audio = self.page.overlay[gl["index"]]
        audio_info = TinyTag.get(audio.src)
        postion = int(v * audio_info.duration * 10)
        self.page.overlay[gl["index"]].seek(postion)

    def resume(self):
        print("继续")
        self.page.overlay[gl["index"]].resume()
        self.play_btn.selected = True
        gl["state"] = "playing"
        self.update()

    def pause(self):
        print("暂停")
        self.page.overlay[gl["index"]].pause()
        self.play_btn.selected = False
        gl["state"] = "pause"
        self.update()

    def toggle_play(self, e):
        print("toggle", e.control.selected)
        if e.control.selected:
            self.pause()
        else:
            self.resume()

    def volume_change(self, e):
        v = e.control.value
        self.page.overlay[gl["index"]].volume = 0.01 * v
        gl["volume"] = 0.01 * v
        if v == 0:
            self.volume_icon.name = icons.VOLUME_OFF
        elif 0 < v <= 50:
            self.volume_icon.name = icons.VOLUME_DOWN
        elif 50 < v:
            self.volume_icon.name = icons.VOLUME_UP
        self.page.update()


class ViewPage(ft.Stack):
    global gl

    def __init__(self, page: ft.Page):
        self.is_first = True
        self.page = page
        # tabs
        self.ta = ft.Tabs(
            expand=True,
            selected_index=0,
            tabs=[
                ft.Tab(text="本地歌曲", content=SongList(page, self.songItemClick)),
                ft.Tab(text="我的歌单", content=MyList(page, self.songItemClick)),
            ],
        )

        # 播放控制
        self.ctr = AudioInfo(page, [self.showLrc, self.showSonglist])
        self.c = Column([self.ta, self.ctr], expand=True, spacing=0)
        self.lrc = Container(
            bgcolor=ft.colors.GREY_200,
            content=ft.Column(
                controls=[
                    Row(
                        [
                            ft.Image(width=300, height=300, src="album.png"),
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

        self.song_list = ft.ListView(width=400, spacing=10)

        self.song_cont = ft.Container(
            content=self.song_list,
            right=10,
            bottom=110,
            bgcolor=ft.colors.SURFACE_VARIANT,
            border_radius=6,
            padding=8,
            offset=ft.transform.Offset(2, 0),
        )

        super(ViewPage, self).__init__(
            controls=[self.c, self.lrc, self.song_cont],
            expand=True,
        )

    def playsong(self, index, e):
        if index != gl["index"]:
            self.page.overlay[gl["index"]].release()
            self.page.overlay[gl["index"]].update()
            gl["index"] = index
            self.ctr.play_new()
            self.page.update()

    def freshSonglist(self):
        songLength = len(self.page.overlay)
        if songLength > 1:
            self.song_list.clean()
            song_item = ft.Text(f"正在播放", size=20, weight=ft.FontWeight.W_900)
            self.song_list.controls.append(song_item)
            for index, _playing_audio in enumerate(self.page.overlay[1:]):
                _s: DataSong = _playing_audio.song
                if _playing_audio.during:
                    _duration = ms_to_time(_playing_audio.during)
                else:
                    _duration = ""
                song_item = Container(
                    content=Row(
                        controls=[
                            Text(f"{index+1}、", width=20),
                            Text(_s.name, width=100, no_wrap=True),
                            Text(_s.singer, width=50, no_wrap=True),
                            Text(_duration, width=40, no_wrap=True),
                            ft.IconButton(
                                icon=ft.icons.PLAY_CIRCLE_FILLED_OUTLINED,
                                on_click=partial(self.playsong, index + 1),
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE_FOREVER,
                                # on_click=self.playSong,
                            ),
                        ],
                        spacing=2,
                    ),
                )
                self.song_list.controls.append(song_item)
            self.song_list.update()
        else:
            self.song_list.clean()
            song_item = ft.Text(f"当前没有歌曲")
            self.song_list.controls.append(song_item)
            self.song_list.update()

    def showLrc(self, e):
        self.lrc.visible = not self.lrc.visible
        self.page.update()

    def showSonglist(self, e):
        offx = self.song_cont.offset.x
        self.freshSonglist()
        if offx == 2:
            self.song_cont.offset = ft.transform.Offset(0, 0)
        else:
            self.song_cont.offset = ft.transform.Offset(2, 0)
        self.song_cont.update()

    # 获取子项点击后的操作
    def songItemClick(self, song: DataSong):
        self.ctr.play_music(song)
        self.freshSonglist()

    def init_event(self):  # 获取tabs第一页内容
        pass
        # search_view = self.t.controls[0].tabs[0].content

        # if not search_view.right_widget.music_list.list.controls:
        #     search_view.right_widget.search_content.search(None)
