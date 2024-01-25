import random
from typing import List, Generator, Optional
from utils import HTMLSession


class _Base:
    base_url = ""  # 基础地址
    page_url = ""  # 页面地址
    page_num = None  # 页码
    max_page = 0  # 最大页码
    page_list = Optional[list]  # 默认如果是个列表的话，子类会继承父类的列表，所以父类用None表示，子类重新初始化为列表

    # 设置页码
    @classmethod
    def set_page(cls, page_num: int):
        cls.page = page_num

    # 图片地址生成器 (src1,src2...)
    @classmethod
    def image_url_generator(cls):
        while True:
            ## 设置页码
            # 假如是初始 None 随机获取页码
            if cls.page_num is None:
                cls.page_num = random.randint(1, cls.max_page)
            else:  # 假如超过最大值 重置为第一页
                if cls.page_num > cls.max_page:
                    cls.page_num = 1
            # 假如page_list (图片list)
            if not cls.page_list:
                cls.page_list.extend(cls._get_page_list(cls.page_num))
            detail_url = cls.page_list.pop(0)  # 详情页地址 page_list
            for src in cls._get_image_url(detail_url):
                # return
                yield src

            cls.page_num += 1

    @classmethod
    def _get_image_url(cls, detail_url) -> Generator[str, None, None]:
        raise NotImplementedError  # 被子类调用必须重写相当于接口 interface

    @classmethod
    def _get_page_list(cls, page_num: int) -> List[str]:
        raise NotImplementedError


class CiYuanDao(_Base):
    base_url = "http://ciyuandao.com"
    page_url = "http://ciyuandao.com/photo/list/0-0-{page_num}"
    max_page = 451
    page_list = []

    @classmethod
    def _get_image_url(cls, detail_url):
        # 获取里面的图片
        session = HTMLSession()
        resp = session.get(detail_url)
        a_list = resp.html.xpath('//div[@class="talk_pic hauto"]//img[@src]')
        for img in a_list:
            img_src = img.attrs.get("src")
            if img_src:
                yield img_src

    @classmethod
    def _get_page_list(cls, page_num: int):
        # 获取此page下面的所有相关url
        url = cls.page_url.format(page_num=page_num)  # 拼装地址
        session = HTMLSession()
        resp = session.get(url)
        hrefs = resp.html.xpath('//div[@class="pics"]//a[@class="tits grey" and @href]')
        res = []
        for a in hrefs:
            a = a.attrs.get("href", "")
            if a:
                res.append(cls.base_url + a)
        return res


class Imgapi:
    def get_img():
        return "https://imgapi.cn/api.php?fl=dongman&gs=images"


APIS = {"次元岛cosplay": CiYuanDao}
