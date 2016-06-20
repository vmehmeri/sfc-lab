#!/bin/bash

FLA_SERVER1_IP='10.0.0.1'
FLA_SERVER3_IP='10.0.0.2'
SFF1_IP='10.0.0.3'
SFF2_IP='10.0.0.4'
H1_IP='10.0.0.10'
H2_IP='10.0.0.20'

FLA_SERVER1_MAC='00:1b:21:a6:8f:fd'
FLA_SERVER3_MAC='00:1b:21:a6:90:1f'
SFF1_MAC='aa:aa:aa:33:33:33'
SFF2_MAC='aa:aa:aa:44:44:44'
H1_MAC='00:00:00:11:11:11'
H2_MAC='00:00:00:22:22:22'

ssh fla-server1 sudo arp -s $FLA_SERVER3_IP $FLA_SERVER3_MAC -i eth1
ssh fla-server1 sudo arp -s $SFF1_IP $SFF1_MAC -i eth1
ssh fla-server1 sudo arp -s $SFF2_IP $SFF2_MAC -i eth1
ssh fla-server1 sudo ip netns exec h1 arp -s $H2_IP $H2_MAC -i h1-eth0

ssh fla-server3 sudo arp -s $FLA_SERVER1_IP $FLA_SERVER1_MAC -i eth1
ssh fla-server3 sudo arp -s $SFF1_IP $SFF1_MAC -i eth1
ssh fla-server3 sudo arp -s $SFF2_IP $SFF2_MAC -i eth1
ssh fla-server3 sudo ip netns exec h2 arp -s $H1_IP $H1_MAC -i h2-eth0

ssh sff-vm1 sudo arp -s $FLA_SERVER1_IP $FLA_SERVER1_MAC -i eth1
ssh sff-vm1 sudo arp -s $FLA_SERVER3_IP $FLA_SERVER3_MAC -i eth1
ssh sff-vm1 sudo arp -s $SFF2_IP $SFF2_MAC -i eth1

ssh sff-vm2 sudo arp -s $FLA_SERVER1_IP $FLA_SERVER1_MAC -i eth1
ssh sff-vm2 sudo arp -s $FLA_SERVER3_IP $FLA_SERVER3_MAC -i eth1
ssh sff-vm2 sudo arp -s $SFF1_IP $SFF1_MAC -i eth1
