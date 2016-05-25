#!/bin/bash

sudo apt-get update -y
sudo apt-get install git -y
sudo apt-get install libssl-dev openssl libnetfilter-queue-dev python3-flask python3-pip -y
sudo pip3 install sfc paramiko flask
git clone https://git.opendaylight.org/gerrit/p/sfc.git --branch stable/beryllium
cp -r sfc/sfc-py .
cp -r sfc/sfc-test/nsh-tools/vxlan_tool.py .

