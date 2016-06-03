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
	#				  port=6653)

	# Add hosts and switches
	#h1 = net.addHost( 'h1', ip='10.0.0.1', mac='00:00:00:00:00:01' )
	s11 = net.addSwitch( 's11' )
	# Add links
	#net.addLink( h1, s11 )

	## Configure GRE tunnel ##

	# Delete old tunnel if still exists
	s11.cmd('ip tun del s11-gre1')

	# Create GRE tunnels
	print "Creating GRE tunnels"

	#s11.cmd('ip li ad s11-gre1 type gretap local '+H1_VM_IP+' remote '+MININET_VM_IP+' ttl 64')
	#s11.cmd('ip li se dev s11-gre1 up')
	#Intf( 's11-gre1', node=s11 )

	s11.cmd('sudo ovs-vsctl add-port s11 s11-gre1 -- set interface s11-gre1 type=gre options:local_ip='+H1_VM_IP+',remote_ip='+MININET_VM_IP)

	print "Setting OVSDB manager to " + MANAGER_IP + ":6640"
	s11.cmd('ovs-vsctl set-manager tcp:'+MANAGER_IP+':6640')
	net.start()
	s11.cmd('sudo ovs-vsctl add-port s11 sff0-dpl -- set interface sff0-dpl type=vxlan options:remote_ip=flow options:dst_port=6633 options:key=flow options:nsp=flow options:nsi=flow options:nshc1=flow options:nshc2=flow options:nshc3=flow options:nshc4=flow')
	s11.cmd('ovs-vsctl set-controller s11 tcp:'+MANAGER_IP+':6653')
	#s11.cmd('ovs-ofctl add-flow s11 priority=100,in_port=1,action=output:2')
	#s11.cmd('ovs-ofctl add-flow s11 priority=100,in_port=2,action=output:1')
	#h1.cmd('arp -s 10.0.0.3 00:00:00:00:00:03 -i h1-eth0')
	CLI( net )
	net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    exampleNet()
