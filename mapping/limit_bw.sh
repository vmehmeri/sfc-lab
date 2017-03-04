#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: limit_bw [interface]"
  exit 1
fi

sudo tc qdisc del dev $1 root &>/dev/null
sudo tc qdisc add dev $1 root handle 1:0 htb default 10
sudo tc class add dev $1 parent 1:0 classid 1:10 htb rate 512kbps ceil 640kbps prio 0
