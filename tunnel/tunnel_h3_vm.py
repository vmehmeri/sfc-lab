#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf

def exampleNet():

	IP_PREFIX='192.168.137.'
	MININET_VM_IP=IP_PREFIX+'110'
	#CONTROLLER_IP=IP_PREFIX+'100'
	MANAGER_IP=IP_PREFIX+'100'
	H1_VM_IP=IP_PREFIX+'10'
	H2_VM_IP=IP_PREFIX+'20'
	H3_VM_IP=IP_PREFIX+'30'

	net = Mininet( topo=None, controller=None, build=False)

	#net.addController( 'c0',
	#				  controller=RemoteController,
	#				  ip=MANAGER_IP,
	#				  port=6633)

	# Add hosts and switches
	#h3 = net.addHost( 'h3', ip='10.0.0.3', mac='00:00:00:00:00:03' )
	s44 = net.addSwitch( 's44' )
		
	# Add links
	#net.addLink( h3, s44 )
	
	## Configure GRE tunnel ##

	# Delete old tunnel if still exists
	s44.cmd('ip tun del s44-gre1')
	
	# Create GRE tunnels
	print "Creating GRE tunnels..."
	
	#s44.cmd('ip li ad s44-gre1 type gretap local '+H3_VM_IP+' remote '+MININET_VM_IP+' ttl 64')
	#s44.cmd('ip li se dev s44-gre1 up')
	#Intf( 's44-gre1', node=s44 )
	s44.cmd('sudo ovs-vsctl add-port s44 s44-gre1 -- set interface s44-gre1 type=gre options:local_ip='+H3_VM_IP+',remote_ip='+MININET_VM_IP)

	print "Setting OVSDB manager to " + MANAGER_IP + ":6640"
	s44.cmd('ovs-vsctl set-manager tcp:'+MANAGER_IP+':6640')
	net.start()
	s44.cmd('sudo ovs-vsctl add-port s44 sff3-dpl -- set interface sff3-dpl type=vxlan options:remote_ip=flow options:dst_port=6633 options:key=flow options:nsp=flow options:nsi=flow options:nshc1=flow options:nshc2=flow options:nshc3=flow options:nshc4=flow')
	s44.cmd('ovs-vsctl set-controller s44 tcp:'+MANAGER_IP+':6653')
	#s44.cmd('ovs-ofctl add-flow s44 priority=100,in_port=1,action=output:2')
	#s44.cmd('ovs-ofctl add-flow s44 priority=100,in_port=2,action=output:1')
	#h3.cmd('arp -s 10.0.0.1 00:00:00:00:00:01 -i h3-eth0')
	CLI( net )
	net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    exampleNet()
