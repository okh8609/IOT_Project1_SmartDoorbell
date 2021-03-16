'''
sudo docker run --rm \
    --memory 6144MB \
    --name iotFace \
    --cpu-period=100000 --cpu-quota=300000 \
    -v ~/iot_face:/iot_face \
    okh8609/face:test  /bin/bash /iot_face/run.sh
'''

import requests
import json

myURL = 'http://192.168.50.122:2375/containers/create'

myHeader = {
    'Content-type': 'application/json'
}

myData = {
  "Image": "okh8609/face:test",
  "Cmd": ["/bin/bash", "/iot_face/run.sh"],
  "HostConfig": {
        "AutoRemove": True,
        "Memory": 6442450944,
        "CpuPeriod": 100000,
        "CpuQuota": 300000,
        "Binds": ["/home/kh/iot_face:/iot_face"]
    }
}
response = requests.post(myURL, data=json.dumps(myData), headers=myHeader)
print(json.dumps( json.loads(response.text) , indent=2))

# http://192.168.50.122:2375/containers/{CONTAINER_ID}/start

myURL = 'http://192.168.50.122:2375/containers/'+json.loads(response.text)["Id"]+'/start'
response = requests.post(myURL)
print(response.text)


