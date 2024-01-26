import random
import requests


# def getNumList(max):
#     numbers = []
#     while len(numbers) < max:
#         # 生成一个范围在1到99之间的随机数
#         num = random.randint(1, 9999)

#         if num not in numbers:
#             # 如果该随机数还未被添加到列表中，则将其添加进去
#             numbers.append(num)
#     return numbers


url = "https://imgapi.cn/api.php?&zt=pc"
pics = []


# while len(pics) < 20:
#     pics.append(requests.get(url).url)
# print(pics)
def get_imgs(url, num):
    for i in range(num):
        pic_url = requests.get(url).url
        if pic_url:
            yield pic_url


imgs = get_imgs(url, 10)
for img in imgs:
    print(img, sep="\n")


# res = requests.get(url)
# redirected_url = res.url  # 获取跳转后的URL
# print("跳转后的URL为：", redirected_url)
