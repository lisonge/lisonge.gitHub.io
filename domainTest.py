'''
@Date: 2020-02-13 00:29:26
@LastEditors  : code
@Author: code
@LastEditTime : 2020-02-13 00:31:21
'''
import requests


proxies = {
	"http": "http://127.0.0.1:1080",
	"https": "http://127.0.0.1:1080",
}

url = 'https://dev.songe.li'

resp = requests.get(url, proxies=proxies)

print(resp.text)

