# Deployment Controller

The idea behind this app is to have a simple controller to help with deployment of various services.
Currently these are served as static files or in docker containers, which manually has to be deployed.

## Features

- [ ] Pull new changes for a git repo to serve static files
- [ ] Pull new docker image and start new container

## Runing container

Because we want to execute commands against the host, the host file system has to be mounted into the container

```sh
docker run -ti --rm --name test \
    --pid=host \
    -e ROOT_DIR="/host/host_mnt" \
    -e MQTT_URL=paletten.oliverflecke.me \
    --privileged \
    --volume $(pwd)/config:/config \
    --volume /:/host \
    oliverflecke/deployment_ctrl \
    chroot /host
```

Note that some suggest that the following should be added to allow full access, but so far it does not seems like this is needed: `--net=host --pid=host --ipc=host`
