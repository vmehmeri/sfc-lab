#!/bin/bash

sudo ovs-vsctl del-br br-sfc &>/dev/null
sudo ovs-vsctl add-br br-sfc
sudo ovs-vsctl add-port br-sfc sff1-dpl -- set interface sff1-dpl type=vxlan options:remote_ip=flow options:dst_port=6633 options:key=flow options:nsp=flow options:nsi=flow options:nshc1=flow options:nshc2=flow options:nshc3=flow options:nshc4=flow
sudo ovs-vsctl set-manager tcp:192.168.137.110:6640
	
