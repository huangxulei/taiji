# import requests_html

# # 创建 Session 对象
# session = requests_html.HTMLSession()

# # 设置代理服务器地址和端口号（这里以 IPv4 为例）
# proxy = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7980"}

# # 将代理信息添加到 Session 中
# session.proxies = proxy

# # 发送 GET 请求
# response = session.get("https://www.baidu.com")
# print(response.text)

# import requests

# # 设置代理，多用于爬虫
# proxies = {"https": "https://127.0.0.1:7890"}
# headers = {"referer": "https://www.hifini.com"}
# # 1,普通的代理
# res = requests.get(url="https://www.hifini.com", headers=headers, proxies=proxies)
# print(res.content.decode("utf-8"))


import requests

url = "http://ip.chinaz.com/getip.aspx"
proxy = {"https": "https://127.0.0.1:7890"}

r = requests.get(url, proxies=proxy, timeout=1)
print(r.text)
