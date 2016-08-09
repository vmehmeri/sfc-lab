#!/bin/bash

if [ $# -ne 1 ]; then
    echo $0: usage: run NUMBER_OF_CONTROLLERS
    exit 1
fi


sudo python sample_network.py $1

#echo "Stopping docker containers..."
#sudo docker stop $(docker ps -a -q) &>/dev/null
#echo "Removing docker containers..."
#sudo docker rm $(docker ps -a -q) &>/dev/null
echo "Cleaning up Mininet..."
sudo mn -c &>/dev/null
