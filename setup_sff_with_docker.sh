#!/bin/bash

./install_docker.sh
cd sfc-py/sfc/sf-docker
./build.sh
echo "Setup complete"
echo "Start agent by running ./start_agent.sh <CONTROLLER_IP:PORT>"
