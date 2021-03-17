'''
sudo docker run --rm \
    --memory 6144MB \
    --name iotFace \
    --cpu-period=100000 --cpu-quota=300000 \
    -v ~/iot_face:/iot_face \
    okh8609/face:test  /bin/bash /iot_face/run.sh
'''

import docker
client = docker.DockerClient(base_url='tcp://192.168.50.122:2375').api
container = client.create_container(
    image='okh8609/face:test',
    command='/bin/bash /iot_face/run.sh',
    volumes=['/iot_face'],
    host_config=client.create_host_config(
        binds=['/home/kh/iot_face:/iot_face'],
        cpu_period=100000, cpu_quota=300000,
        mem_limit=6442450944,
        auto_remove=True
    )
)
response = client.start(container=container.get('Id'))
print(response)

