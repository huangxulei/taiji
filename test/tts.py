# proxies = {"http": "http://127.0.0.1:7890", "https": "https://127.0.0.1:7890"}
# response = requests.get("https://www.ip.cn/api/index?ip=&type=0", proxies=proxies)
# print(response.text)


from urllib import request, parse

# 测试ip网站
# url = "http://icanhazip.com/"
# headers = {
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.188.400 QQBrowser/11.4.5226.400"
# }

headers = {"referer": "https://www.hifini.com"}
url = "https://www.hifini.com/"

proxies = {"https": "127.0.0.1:7890"}
# req = request.Request(url=url, headers=headers)
# handler = request.ProxyHandler(proxies=proxies)
# opener = request.build_opener(handler)
# response = opener.open(req)

# content = response.read().decode("utf-8")


# with open("iptest.text", "w", encoding="utf-8") as fp:
#     fp.write(content)
