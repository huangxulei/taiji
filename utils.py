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

PICTURE = os.path.join(os.path.expanduser("~"), "Pictures")


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
