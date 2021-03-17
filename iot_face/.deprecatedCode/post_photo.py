import requests
url = 'http://192.168.50.122:50000'
files = {'myFile': open('./test_image/t2.jpg', 'rb')}
response = requests.request("POST", url, files=files)
print(response.text)