#!/bin/bash

sudo apt-get install libssl-dev openssl libnetfilter-queue-dev python3-flask python3-pip -y
sudo pip3 install sfc paramiko flask click docker-py

./install_docker.sh
cd sfc-py/sfc/sf-docker
./build.sh
echo "Setup complete"
echo "Start agent by running ./start_agent.sh <CONTROLLER_IP:PORT>"
