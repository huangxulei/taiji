import urllib.request as requests

headers = {"referer": "https://www.hifini.com"}
search_url = "https://www.hifini.com/search-{target}-{page}.htm"
recommend_url = "https://www.hifini.com/"
base_url = "https://www.hifini.com/"

proxies = {"https": "127.0.0.1:7890"}

# 使用 requests模块得到响应对象
request = requests.Request(recommend_url, headers=headers)
handler = requests.ProxyHandler(proxies=proxies)
opener = requests.build_opener(handler)
res = opener.open(request)


# 更改编码格式
res.encoding = "utf-8"
if res.status_code != 200:
    print("没有数据")
else:
    body = res.html.xpath('//div[@class="media-body"]/div/a')  # 列表
    if body:
        for a in body:
            if a.absolute_links:
                detail_url = a.absolute_links.pop()
                if not detail_url:
                    print("无数据")
                else:
                    print(detail_url)  # 展开detiail
