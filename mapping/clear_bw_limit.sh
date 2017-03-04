#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: clear_bw_limit [interface]"
fi

sudo tc qdisc del dev $1 root &>/dev/null
