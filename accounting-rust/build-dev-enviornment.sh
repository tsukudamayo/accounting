#!/bin/bash

export DOCKER_BUILDKIT=1

docker build -t rust-python-dev -f dev.arm64.Dockerfile .

if [[ "$OSTYPE" == "darwin"* ]]; then
    xhost +$(multipass list | grep docker-vm | awk '{print $3}')
    docker run -it --rm \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
	-v $(pwd):/workspace:delegated \
        -e DISPLAY=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}'):0.0 \
        --name accounting-rust \
        rust-python-dev \
        /bin/bash
    xhost -$(multipass list | grep docker-vm | awk '{print $3}')
else
    xhost +local:
    docker run -it --rm \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
	-v $(pwd):/workspace:delegated \
        -e DISPLAY=$DISPLAY \
        --name accounting-rust \
        rust-python-dev \
        /bin/bash
    xhost -local:
fi
