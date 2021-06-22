import requests

url = 'http://icanhazip.com/'

proxies ={
  'http': 'socks5://127.0.0.1:9050',
  'https': 'socks5://127.0.0.1:9050'
}
res= requests.get(url, proxies=proxies)
print(res.text)
