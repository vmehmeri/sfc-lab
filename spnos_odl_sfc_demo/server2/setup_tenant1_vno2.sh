#!/bin/bash

NS_NAME='h4'
IFACE_NAME='vno2-eth'
IP_ADDRESS='10.0.0.20/8'
MAC_ADDRESS='00:00:00:23:23:23'
REMOTE_IP_ADDRESS='10.0.0.10'
REMOTE_MAC_ADDRESS='00:00:00:12:12:12'

sudo ip netns del $NS_NAME &>/dev/null
sudo ip li del $IFACE_NAME &>/dev/null
sudo ovs-vsctl del-port br-sfc $IFACE_NAME &>/dev/null

sudo ip netns add $NS_NAME
sudo ip link add $NS_NAME-eth0 type veth peer name $IFACE_NAME
sudo ovs-vsctl add-port br-sfc $IFACE_NAME
sudo ip link set dev $IFACE_NAME up
sudo ip link set $NS_NAME-eth0 netns $NS_NAME

sudo ip netns exec $NS_NAME ifconfig $NS_NAME-eth0 $IP_ADDRESS up
sudo ip netns exec $NS_NAME ip link set dev $NS_NAME-eth0 addr $MAC_ADDRESS
sudo ip netns exec $NS_NAME arp -s $REMOTE_IP_ADDRESS $REMOTE_MAC_ADDRESS -i $NS_NAME-eth0
sudo ip netns exec $NS_NAME ip link set dev $NS_NAME-eth0 up
sudo ip netns exec $NS_NAME ip link set lo up
sudo ip netns exec $NS_NAME ifconfig $NS_NAME-eth0 mtu 1400

