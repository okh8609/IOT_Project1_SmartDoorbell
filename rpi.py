from picamera import PiCamera
from time import sleep
import requests

camera = PiCamera()
# camera.rotation = 180
camera.resolution = (800, 600) # (3280, 2464)
# camera.start_preview()
# sleep(3)
camera.capture("./img.jpg")
# camera.stop_preview()

url = 'https://khaos.tw/uploaded/guest'
files = {'myFile': open('./img.jpg', 'rb')}
response = requests.request("POST", url, files=files)
print(response.text)
