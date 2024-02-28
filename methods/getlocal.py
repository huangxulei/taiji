from dataclasses import dataclass, field
from typing import Generator, Optional
import os
from utils import byte_to_base64, get_file_type
from tinytag import TinyTag


@dataclass
class DataSong:
    isLocal: bool  # 是否本地
    cover: str  # 封面
    name: str  # 歌曲名称
    singer: str  # 歌手名称
    url: Optional[str] = field(default=None)  # 音乐链接


class LocalSong:
    song_exts = [".mp3", ".flac", ".wma"]  # 支持的歌曲类型

    @classmethod
    def getFiles(cls, file_dir) -> Generator[DataSong, None, None]:
        path = os.path.join(os.getcwd(), file_dir)
        files = os.listdir(path)
        if files != 0:
            for file in files:
                if get_file_type(file) in cls.song_exts:
                    file_path = os.path.join(file_dir, file)
                    res = cls.get_detail_song(file_path)
                    if res:
                        yield DataSong(**res)

    @classmethod
    def get_detail_song(cls, file_path):
        try:
            song_info = TinyTag.get(file_path, image=True)  # 获取歌曲
            img = song_info.get_image()
            if song_info.get_image():
                cover = byte_to_base64(img)
            else:
                cover = "album.png"
        except:
            return False  # 报错处理
        result = {
            "isLocal": True,
            "cover": cover,
            "name": song_info.title,
            "singer": song_info.artist,
            "url": file_path,
        }
        return result
