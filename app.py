#!/usr/bin/env python3

from typing import Dict
import logging
import paho.mqtt.client as mqtt
import yaml
import json
import os


def getLoggingLevel() -> int:
    match os.environ.get('LOG_LEVEL', 'INFO').upper():
        case 'ERROR': return logging.ERROR
        case 'WARNING': return logging.WARNING
        case 'DEBUG': return logging.DEBUG
        case _: return logging.INFO


logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s', level=getLoggingLevel())

# Configuration
root_dir = os.environ.get('ROOT_DIR', '/')
url = os.environ.get('MQTT_URL')
if not url or url == '':
    logging.error('MQTT_URL not provided')
    exit(1)

port = 1883
client = mqtt.Client()
client.connect(url, port, 60)


def getConfig(project: str) -> Dict:
    name = f'config/{project}.yml'
    if not os.path.isfile(name):
        return

    with open(name, 'r') as f:
        return yaml.load(f, yaml.Loader)


def handleDeploy(config: Dict):
    logging.info(f'Deploying {config["name"]}')

    tool = config['type']
    dir = root_dir + \
        config['directory'] if root_dir != '/' else config['directory']

    current = os.getcwd()
    os.chdir(dir)

    for command in config['commands']:
        os.system(f'{tool} {command}')

    os.chdir(current)

    logging.info(f'Deployment of {config["name"]} completed')


def on_message(client, userdata, message):
    try:
        payload = message.payload.decode("utf-8")
        logging.debug(f'Topic: "{message.topic}" - Payload: {payload}')

        msg = json.loads(payload)
        project = msg['project']
        config = getConfig(project)

        if not config:
            logging.warning(f'No config for project "{project}" was found')
            return

        handleDeploy(config)
    except Exception as e:
        logging.error(e)


client.on_message = on_message
client.subscribe("deploy")

logging.info("Controller READY")

client.loop_forever()
