#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import os

# Configuration
mnt = "/host/host_mnt"
# workdir = f'{mnt}/Users/oliver/projects/deployment_ctrl'
# branch = 'main'

# os.system(f'git -C {workdir} pull origin {branch}')

# MQTT Config
url = 'paletten.oliverflecke.me'
port = 1883
client = mqtt.Client()
client.connect(url, port, 60)

def on_message(client, userdata, message):
    print('Got message')
    print(f'Topic: "{message.topic}" - Payload: {message.payload}')

client.on_message = on_message

client.subscribe("deploy")

print("Controller READY")

client.loop_forever()
