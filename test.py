import requests

url = "https://www.hifini.com/"

res = requests.get(url)

print(res.status_code)
