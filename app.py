#!/usr/bin/env python3

from typing import Dict
import logging
import paho.mqtt.client as mqtt
import git
import yaml
import os

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s', level=logging.DEBUG)

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


def getConfig(project: str) -> Dict:
    name = f'config/{project}.yml'
    with open(name, 'r') as f:
        return yaml.load(f, yaml.Loader)


def deployGit(config: Dict):
    branch = config["git"]["branch"]
    command = config["git"]["command"]
    dir = config["directory"]
    os.system(f'git -C {dir} {command} origin {branch}')


def handleDeploy(config: Dict):
    logging.info(f'Deploying {config["name"]}')

    match config["type"]:
        case 'git':
            deployGit(config)
        case _:
            logging.warn(
                f'Unable to handle deployment for type "{config["type"]}"')


def on_message(client, userdata, message):
    logging.debug(f'Topic: "{message.topic}" - Payload: {message.payload}')

    project = message.payload
    config = getConfig(project)
    if not config:
        logging.warn(f'No config for project "{project}" was found')
        return

    logging.debug(config)


client.on_message = on_message
client.subscribe("deploy")

logging.info("Controller READY")

client.loop_forever()
