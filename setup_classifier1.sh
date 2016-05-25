#!/bin/bash

while true; do
    read -p "Name of ovs-bridge? " BR_NAME
    break;
done

while true; do
    read -p "Name of namespace? " NS_NAME
    break;
done

while true; do
    read -p "Name of namespace virtual endpoint? " NS_IF_NAME
    break;
done

while true; do
    read -p "Name of bridge virtual endpoint? " BR_IF_NAME
    break;
done


echo "Removing existing configuration..."
sudo ip netns del app &>/dev/null
sudo ovs-vsctl del-br $BR_NAME &>/dev/null


echo "Creating ovs bridge..."
sudo ovs-vsctl add-br $BR_NAME
echo "Adding network namespace..."
sudo ip netns add $NS_NAME
echo "Creating IP configuration..."
sudo ip link add $NS_IF_NAME type veth peer name $BR_IF_NAME
sudo ovs-vsctl add-port $BR_NAME $BR_IF_NAME
sudo ip link set dev $BR_IF_NAME up
sudo ip link set $NS_IF_NAME netns app

sudo ip netns exec app ifconfig veth-app 10.0.0.1/24 up
sudo ip netns exec app ip link set dev veth-app  addr 00:00:00:00:00:01
sudo ip netns exec app arp -s 10.0.0.3 00:00:00:00:00:03 -i veth-app
sudo ip netns exec app ip link set dev veth-app up
sudo ip netns exec app ip link set dev lo up
sudo ip netns exec app ifconfig veth-app mtu 1400

echo "Done."

#sudo ip tun del br-sfc-gre1 &>/dev/null
#sudo ip li ad br-sfc-gre1 type gretap local 10.13.13.107 remote 10.13.13.105 ttl 64
#sudo ip li se dev br-sfc-gre1 up
#sudo ovs-vsctl add-port br-sfc br-sfc-gre1
