#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: add_delay [interface]"
  exit 1
fi

sudo tc qdisc add dev $1 handle 1: root htb default 11
sudo tc class add dev $1 parent 1: classid 1:1 htb rate 1000Mbps
sudo tc class add dev $1 parent 1:1 classid 1:11 htb rate 100Mbit
sudo tc qdisc add dev $1 parent 1:11 handle 10: netem delay 50ms
