#!/bin/bash

## INSTALL Docker on Ubuntu 14.04

sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates -y
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
touch docker.list
echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" > docker.list
sudo mv docker.list /etc/apt/sources.list.d/docker.list
sudo apt-get update
sudo apt-get purge lxc-docker -y
sudo apt-get install linux-image-extra-$(uname -r) -y
sudo apt-get install docker-engine -y
sudo service docker start

sudo groupadd docker &>/dev/null
sudo usermod -aG docker $USER

echo "Installation complete."
echo "You must log out and back in to be able to run docker commands without sudo privileges"
echo "You can test docker now by running: sudo docker run hello-world"
#sudo docker run hello-world


