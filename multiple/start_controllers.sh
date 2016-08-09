#!/bin/bash

sudo docker build -t vmehmeri/pox . &>/dev/null
sudo python3.4 multiple-controllers.py $1

