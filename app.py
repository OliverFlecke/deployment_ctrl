#!/usr/bin/env python3

# import paho.mqtt.client as mqtt
import git
import os

print("Started controller")

workdir = "/host/host_mnt/Users/oliver/projects/deployment_ctrl"

# g = git.cmd.Git(workdir)
# g.pull()

os.chdir(workdir)
os.system(f'git pull origin main')
