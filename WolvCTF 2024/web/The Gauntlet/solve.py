import requests

url = 'https://gauntlet-okntin33tq-ul.a.run.app/hidden83365193635473293'
cookies = {}

for i in range(1000):
    req = requests.get(url, cookies=cookies)
    cookies['jwt-uncrackable-cookie-counter'] = req.cookies.get('jwt-uncrackable-cookie-counter')
    
    if i == 999:
        print(req.text)