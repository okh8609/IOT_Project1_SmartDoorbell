import requests
url = 'https://khaos.tw/uploaded/guest'
files = {'myFile': open('C:\\Users\\KaiHao\\Desktop\\iot_project1\\.test_image\\0\\test.jpg', 'rb')}
response = requests.request("POST", url, files=files)
print(response.text)