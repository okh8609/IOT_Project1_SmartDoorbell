import requests
url = 'https://khaos.tw/uploaded/guest'
files = {'myFile': open('test2.jpg', 'rb')}
response = requests.request("POST", url, files=files)
print(response.text)