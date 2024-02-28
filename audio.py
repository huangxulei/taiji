from typing import Optional
import flet as ft
from flet import (
    Page,
    GridView,
    Column,
    Container,
    Image,
    Text,
    colors,
    Row,
    border,
    margin,
    Slider,
    Audio,
    IconButton,
    icons,
    Icon,
    ListTile,
    ImageFit,
    transform,
    animation,
    AnimationCurve,
    alignment,
    MainAxisAlignment,
    LinearGradient,
)

from methods.getlocal import LocalSong, DataSong
from utils import snack_bar, ms_to_time, byte_to_base64
from tinytag import TinyTag

g_curr = {"index": 0, "state": "", "song_list": [], "volume": 0.5}


# 带有数据,事件的显示单元,
# 点击歌曲,然后假如播放列表以及播放
class SongItem(Container):
    def __init__(self, song: DataSong, select_callback):

        self.song: DataSong = song
        self.select_callback = select_callback
        self.cover = Image(
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
            color=colors.WHITE,
            tooltip=song.name,
        )
        self.singer = Text(
            song.singer,
            width=80,
            height=20,
            no_wrap=True,
            weight="bold",
            color=colors.WHITE,
            tooltip=song.singer,
        )

        super(SongItem, self).__init__(
            content=Row([self.cover, self.name, self.singer], spacing=10),
            on_click=self.clickIt,  # 点击操作
            bgcolor=colors.BLUE_GREY_300,
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
        if value is True:  # 接受按钮点击后执行
            self.bgcolor = colors.BLUE_GREY_700
            self.opacity = 1
            self.update()
            self.select_callback(self)  # 点击操作 AudioInfo.play_music(songItem)
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
class PlayAudio(Audio):
    def __init__(self, song: DataSong, *args, **kwargs):
        self.song = song
        self.during: Optional[int] = None
        super(PlayAudio, self).__init__(*args, **kwargs)

    def update_during(self, during):
        self.during = during


class AudioInfo(Container):

    def __init__(self):
        self.song: Optional[DataSong] = None
        self.playing_audio: Optional[PlayAudio] = None
        self.is_sliding = False
        self.track_name = Text("")
        self.track_artist = Text("")
        self.current_time = Text(value="00:00")
        self.total_time = Text(value="00:00")
        self.track_slider = Slider(
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
        self.disc_image = Image(
            src=f"assets/album.png",
            width=90,
            height=90,
            fit=ImageFit.CONTAIN,
            rotate=transform.Rotate(0, alignment=alignment.center),
            animate_rotation=animation.Animation(300, AnimationCurve.EASE_IN_CIRC),
        )
        self.cont = Container(
            content=Row(
                controls=[
                    self.disc_image,
                    Container(
                        width=180,
                        height=70,
                        content=ListTile(
                            leading=Icon(icons.MUSIC_NOTE_ROUNDED),
                            title=self.track_name,
                            subtitle=self.track_artist,
                        ),
                    ),
                    Column(
                        [
                            Row(
                                [
                                    self.current_time,
                                    self.track_slider,
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
                                    Slider(
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
                                        icon=icons.PLAYLIST_ADD_ROUNDED,
                                        # on_click=lambda _: pick_files_dialog.pick_files(
                                        #     allow_multiple=True,
                                        #     file_type=FilePickerFileType.AUDIO,
                                        # ),
                                    ),
                                ],
                            ),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                    ),
                ]
            ),
            padding=10,
            width=800,
        )
        super(AudioInfo, self).__init__(
            content=self.cont,
            height=105,
            alignment=alignment.center,
            border_radius=20,
            gradient=LinearGradient(
                begin=alignment.top_center,
                end=alignment.bottom_center,
                colors=[colors.YELLOW_100, colors.BLUE_50],
            ),
        )

    def play_music(self, songItem: SongItem):
        self.set_info(songItem)  # 播放栏显示
        self.play(songItem.song)

    def set_info(self, songItem: SongItem):
        self.track_name.value = songItem.song.name
        self.track_artist.value = songItem.song.singer
        if songItem.cover.src_base64:
            self.disc_image.src_base64 = songItem.cover.src_base64
        else:
            self.disc_image.src_base64 = None
            self.disc_image.src = songItem.song.cover
        # self.total_time.value = ms_to_time(self.play_audio.during)
        self.update()

    def volume_change(self, e):
        v = e.control.value
        self.page.overlay[g_curr["index"]].volume = 0.01 * v
        g_curr["volume"] = 0.01 * v
        if v == 0:
            self.volume_icon.name = icons.VOLUME_OFF
        elif 0 < v <= 50:
            self.volume_icon.name = icons.VOLUME_DOWN
        elif 50 < v:
            self.volume_icon.name = icons.VOLUME_UP
        self.page.update()

    def ld_change(self, e):
        v = e.control.value  # 获取当前距离 v百分比
        audio = self.page.overlay[g_curr["index"]]
        audio_info = TinyTag.get(audio.src)
        postion = int(v * audio_info.duration * 10)
        self.page.overlay[g_curr["index"]].seek(postion)

    # 播放歌曲
    def play(self, song: DataSong):
        print("play", song.name)
        g_curr["state"] = "playing"
        if song is None:
            if self.song is not None:
                self.playing_audio.play()
                self.play_btn.selected = True
                self.update()
                return
            else:
                return
        if self.song and self.song.url == song.url:
            self.playing_audio.play()
        else:
            self.song = song
            res = self.isInOverlay(song)
            print(res)
            if res == -1:
                if self.playing_audio:
                    self.playing_audio.release()
                self.playing_audio = PlayAudio(
                    song=song,
                    src=song.url,
                    autoplay=True,
                    on_duration_changed=self.during_changed,
                    on_position_changed=self.position_changed,
                    volume=g_curr["volume"],
                    on_state_changed=self.check_state,
                )
                self.page.overlay.append(self.playing_audio)
                self.page.update()
                self.playing_audio.autoplay = False
                g_curr["index"] = len(self.page.overlay) - 1
            else:
                print("老歌曲", res)
                self.playing_audio.release()
                self.playing_audio = self.page.overlay[res]
                g_curr["index"] = res
            self.play_btn.selected = True
            self.playing_audio.play()
            self.track_slider.value = "0"

    def play_new(self):
        # cover 处理
        _audio = self.page.overlay[g_curr["index"]]
        _isLocal = _audio.song.isLocal
        if _isLocal:
            if _audio.song.cover != "album.png":
                self.disc_image.src = None
                self.disc_image.src_base64 = _audio.song.cover
            else:
                self.disc_image.src_base64 = None
                self.disc_image.src = "album.png"
        self.track_name.value = _audio.song.name
        self.track_artist.value = _audio.song.singer
        self.current_time.value = "00:00"
        self.total_time.value = ms_to_time(_audio.during)
        if g_curr["state"] == "playing":
            _audio.volume = g_curr["volume"]
            _audio.play()

    def previous_track(self, e):
        self.page.overlay[g_curr["index"]].release()
        self.page.overlay[g_curr["index"]].update()
        g_curr["index"] = g_curr["index"] - 1
        if g_curr["index"] == -1:
            g_curr["index"] = len(self.page.overlay) - 1
        self.play_new()
        self.page.update()

    def next_track(self, e):
        self.page.overlay[g_curr["index"]].release()
        self.page.overlay[g_curr["index"]].update()
        g_curr["index"] = g_curr["index"] + 1
        if g_curr["index"] == len(self.page.overlay):
            g_curr["index"] = 0
        self.play_new()
        self.page.update()

    def check_state(self, e):
        if e.data == "completed":
            print("complete!")
            self.page.overlay[g_curr["index"]].release()
            self.page.overlay[g_curr["index"]].update()
            g_curr["index"] = g_curr["index"] + 1
            if g_curr["index"] == len(self.page.overlay):
                g_curr["index"] = 0
            self.play_new()
            self.play_btn.icon = icons.PAUSE_CIRCLE
            self.page.update()

    def position_changed(self, e):
        during = self.page.overlay[g_curr["index"]].during
        if during:
            self.current_time.value = ms_to_time(int(e.data))
            self.track_slider.value = int(int(e.data) / during * 100)
            self.update()

    def isInOverlay(self, song: DataSong):
        if len(self.page.overlay) > 0:
            for index, _playing_audio in enumerate(self.page.overlay):
                if _playing_audio.song.url == song.url:
                    return index
        return -1

    def during_changed(self, e):
        during = int(e.data)
        self.playing_audio.update_during(during)
        self.total_time.value = ms_to_time(during)
        self.update()

    def resume(self):
        print("继续")
        self.page.overlay[g_curr["index"]].resume()
        self.play_btn.selected = True
        g_curr["state"] = "playing"
        self.update()

    def pause(self):
        print("暂停")
        self.page.overlay[g_curr["index"]].pause()
        self.play_btn.selected = False
        g_curr["state"] = "pause"
        self.update()

    def toggle_play(self, e):
        print("toggle", e.control.selected)
        if e.control.selected:
            self.pause()
        else:
            self.resume()


class ViewPage(Column):
    def __init__(self, page):
        self.page = page
        self.add_btn = ft.ElevatedButton(text="测试", on_click=self.test_slider)
        self.songs = LocalSong.getFiles("E:\music")
        self.mylist = GridView(
            expand=1,
            spacing=30,
            child_aspect_ratio=8,
            max_extent=page.window_width // 3,
            padding=10,
        )
        self.bottom_widget = AudioInfo()

        for song in self.songs:
            self.mylist.controls.append(SongItem(song, self.select_callback))

        super(ViewPage, self).__init__(
            controls=[self.add_btn, self.mylist, self.bottom_widget],
            expand=True,
            spacing=0,
        )

    def test_slider(self, e):
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("test"),
                action="ok",
                open=True,
            )
        )

    def select_callback(self, songItem: SongItem):
        # 循环所有子项
        for _song in self.mylist.controls:
            if _song.selected:  # 如果子项之前被点击
                if _song != songItem:  # 如果不是当前
                    _song.un_select()
        self.bottom_widget.play_music(songItem)


def main(page: Page):
    global g_curr
    page.title = "黄老五播放器"
    page.padding = 0

    local = ViewPage(page)
    page.add(local)


ft.app(target=main, assets_dir="assets")
