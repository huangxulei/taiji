import base64
import os
import re
from threading import Thread
import time
from typing import Optional
from flet import SnackBar, Text, Image as _Image
from requests_html import HTMLSession as _HTMLSession, HTMLResponse
from pathlib import Path
import urllib.parse as uparse
from pathlib import Path
from flet import IconButton, ButtonStyle, MaterialState, colors, BorderSide

CURR_PATH = Path(__file__).absolute().parent
DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")
PICTURE = os.path.join(os.path.expanduser("~"), "Pictures")
PROXY_IP = "http://127.0.0.1:7890"


def one_shot_thread(func, timeout=0.0):
    def run(func, timeout):
        time.sleep(timeout)
        try:
            func()
        except Exception as e:
            print(f"one_shot_thread:{func} {e}")

    Thread(target=run, args=(func, timeout), daemon=True).start()


Threads = []


class HTMLSession(_HTMLSession):
    def __init__(self, headers: Optional[dict] = None, **kwargs):
        super(HTMLSession, self).__init__(**kwargs)
        if headers:
            self.headers.update(headers)


"""
ibs 是一个dict
 {
    "icon": icons.DOWNLOAD, #图标
    "tooltip": "下载", #提示语言
    "fun": self.save_img, #点击后的函数
    "size": 15, #大小 icon的尺寸,height width 为 1.5*15 
}
"""


class MyButton(IconButton):
    def __init__(self, ibs):
        self.style = ButtonStyle(
            color={
                MaterialState.HOVERED: colors.BLUE,
                MaterialState.DEFAULT: colors.GREY_700,
            },
            overlay_color=colors.TRANSPARENT,
            # bgcolor=colors.GREY_200,
        )
        super(MyButton, self).__init__(
            icon=ibs["icon"],
            style=self.style,
            tooltip=ibs["tooltip"],
            on_click=ibs["fun"],
            icon_size=ibs["size"],
            # height=ibs["size"] * 1.5,
            # width=ibs["size"] * 1.5,
        )


def snack_bar(page, message):
    page.snack_bar = SnackBar(content=Text(message), action="好的")
    page.snack_bar.open = True
    page.update()


def get_filename(url):
    parsed = uparse.urlsplit(url)
    filename = Path(parsed.path).name
    return filename


def download_named_image(url):
    file_name = get_filename(url)
    session = HTMLSession()
    p = Path(PICTURE).joinpath("taiji")
    p.mkdir(exist_ok=True)
    resp = session.get(url)
    f = p.joinpath(file_name)
    f.write_bytes(resp.content)
    return f


def download_url_content(url) -> HTMLResponse:
    session = HTMLSession()
    resp = session.get(url)
    return resp


def handle_redirect(url, session=None):
    if session is None:
        session = HTMLSession()
    resp = session.get(url, stream=True)
    return resp.url


def ms_to_time(ms):
    # 毫秒转换为时间格式
    ms = int(ms)
    minute, second = divmod(ms / 1000, 60)
    minute = min(99, minute)
    return "%02d:%02d" % (minute, second)
