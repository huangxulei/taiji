from typing import Optional
import flet as ft
from flet import Text, Container, Column, Row, IconButton, Icon, Image, colors, icons

from importlib import import_module
from methods.getlocal import DataSong
from settings import song_tabs
from utils import ms_to_time
from tinytag import TinyTag

gl = {"index": 1, "state": "", "song_list": [], "volume": 0.5}


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
            on_change=self.ld_change,
        )
        self.play_btn = IconButton(
            icon=icons.PLAY_CIRCLE,
            selected_icon=icons.PAUSE_CIRCLE,
            on_click=self.toggle_play,
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
                self.song_cover.src = None
                self.song_cover.src_base64 = _audio.song.cover
            else:
                self.song_cover.src_base64 = None
                self.song_cover.src = "album.png"
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
                self.song_cover.src_base64 = song.cover
            else:
                self.song_cover.src_base64 = None
                self.song_cover.src = song.cover
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
