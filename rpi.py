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

url = 'http://khaos.tw:58888/uploaded/guest'
files = {'myFile': open('./img.jpg', 'rb')}
requests.post(url, files=files)
