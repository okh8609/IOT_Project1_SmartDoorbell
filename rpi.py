from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import requests
import json
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.IN)
out = 15
GPIO.setup(out,GPIO.OUT)

camera = PiCamera()
camera.resolution = (800, 600) # (3280, 2464)
try:
    while True:
        inputValue = GPIO.input(11)
        if inputValue==False:
            camera.start_preview()
            sleep(1)
            camera.capture('./img.jpg')
            camera.stop_preview()
            url = 'https://khaos.tw/uploaded/guest'
            files = {'myFile': open('./img.jpg', 'rb')}
            response = requests.request("POST", url, files=files)
            print(response.text)
            #sleep(0.5)
        
        r = requests.get("https://khaos.tw/door_status")
        status = r.json()
        #print(status)
        
        if status:
            GPIO.output(out,GPIO.LOW)
            sleep(0.25)
        else:
            GPIO.output(out,GPIO.HIGH)
            sleep(0.25)
except KeyboardInterrupt:
    print("STOP")
finally:
    GPIO.cleanup()
