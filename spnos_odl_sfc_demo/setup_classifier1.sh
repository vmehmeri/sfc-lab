#!/bin/bash

sudo ip netns del h1 &>/dev/null
sudo ip li del br-sfc-eth1 &>/dev/null
sudo ovs-vsctl del-br br-sfc &>/dev/null

sudo ovs-vsctl add-br br-sfc

sudo ip netns add h1
sudo ip link add h1-eth0 type veth peer name br-sfc-eth1
sudo ovs-vsctl add-port br-sfc br-sfc-eth1
sudo ip link set dev br-sfc-eth1 up
sudo ip link set h1-eth0 netns h1

sudo ip netns exec h1 ifconfig h1-eth0 10.0.0.10/8 up
sudo ip netns exec h1 ip link set dev h1-eth0 addr 00:00:00:11:11:11
sudo ip netns exec h1 arp -s 10.0.0.20 00:00:00:22:22:22 -i h1-eth0
sudo ip netns exec h1 ip link set dev h1-eth0 up
sudo ip netns exec h1 ip link set lo up
sudo ip netns exec h1 ifconfig h1-eth0 mtu 1400

sudo ovs-vsctl add-port br-sfc sff0-dpl -- set interface sff0-dpl type=vxlan options:remote_ip=flow options:dst_port=6633 options:key=flow options:nsp=flow options:nsi=flow options:nshc1=flow options:nshc2=flow options:nshc3=flow options:nshc4=flow
sudo ovs-vsctl set-manager tcp:192.168.137.110:6640