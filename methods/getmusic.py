import json, re, time
from urllib.parse import quote
from dataclasses import dataclass, field
from hashlib import md5
from typing import Generator, Optional, List
from flet import Container, alignment, animation, transform, Stack, Text
from utils import HTMLSession, PROXY_IP


# 实体类??
@dataclass
class DataSong:
    photo_url: str  # 图片链接
    big_photo_url: str  # 大图链接
    music_name: str  # 歌曲名称
    singer_name: str  # 歌手名称
    music_url: Optional[str] = field(default=None)  # 音乐链接


class HIFINI:
    headers = {"referer": "https://www.hifini.com"}
    search_url = "https://www.hifini.com/search-{target}-{page}.htm"
    recommend_url = "https://www.hifini.com/"
    base_url = "https://www.hifini.com/"

    @classmethod
    def search_musics(cls, target, page=1) -> Generator[DataSong, None, None]:
        if not target:
            for music in cls.recommend_musics():
                yield music
        else:
            session = HTMLSession(cls.headers)
            quota_target = quote(target).replace("%", "_")
            url = cls.search_url.format(target=quota_target, page=page)
            res = session.post(url)
            if res.status_code != 200:
                yield False, res.text
            else:
                body = res.html.xpath('//div[@class="media-body"]/div/a')

    # 推荐歌曲 列表页
    @classmethod
    def recommend_musics(cls) -> List[Generator[DataSong, None, None]]:
        session = HTMLSession(cls.headers)
        res = session.get(cls.recommend_url)
        if res.status_code != 200:
            yield False, res.text
        else:
            body = res.html.xpath('//div[@class="media-body"]/div/a')  # 列表
            if body:
                for a in body:
                    if a.absolute_links:
                        detail_url = a.absolute_links.pop()
                        detail = cls.get_detail_music(detail_url, session)
                        if not detail:
                            continue
                        else:
                            yield DataSong(**detail)  # 展开detiail

    # 详情页 获取歌曲信息
    @classmethod
    def get_detail_music(cls, url, session=None):
        if session is None:
            session = HTMLSession(cls.headers)
        result = {}
        res = session.get(url)
        aplayer = res.html.xpath('//div[@class="aplayer"]')
        if not aplayer:
            return result
        else:
            strr2 = res.text
            music_url = re.findall(" url: '(.*?)',", strr2, re.S)
            if not music_url:
                return result
            music_name = re.findall(" title: '(.*?)',", strr2, re.S)
            if not music_name:
                return result
            photo_url = re.findall(" pic: '(.*?)'", strr2, re.S)
            if not photo_url:
                return result
            singer_name = re.findall(" author:'(.*?)',", strr2, re.S)
            if not singer_name:
                return result
            result.update(
                {
                    "music_url": cls.base_url + music_url[0],
                    "music_name": music_name[0],
                    "photo_url": photo_url[0],
                    "big_photo_url": photo_url[0],
                    "singer_name": singer_name[0],
                }
            )
            return result
