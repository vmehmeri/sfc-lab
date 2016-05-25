#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf

def exampleNet():

	IP_PREFIX='192.168.137.'
	MININET_VM_IP=IP_PREFIX+'100'
	CONTROLLER_IP=IP_PREFIX+'100'
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
	h2 = net.addHost( 'h2', ip='10.0.0.2', mac='00:00:00:00:00:02' )
	s22 = net.addSwitch( 's22' )
		
	# Add links
	net.addLink( h2, s22 )
	
	## Configure GRE tunnel ##

	# Delete old tunnel if still exists
	s22.cmd('ip tun del s22-gre1')
	
	# Create GRE tunnels
	print "Creating GRE tunnels..."
	
	s22.cmd('ip li ad s22-gre1 type gretap local '+H2_VM_IP+' remote '+MININET_VM_IP+' ttl 64')
	s22.cmd('ip li se dev s22-gre1 up')
	Intf( 's22-gre1', node=s22 )

	print "Setting OVSDB manager to " + MANAGER_IP + ":6640"
	s22.cmd('ovs-vsctl set-manager tcp:'+MANAGER_IP+':6640')
	net.start()
	s22.cmd('sudo ovs-vsctl add-port s22 sff1-dpl -- set interface sff1-dpl type=vxlan options:remote_ip=flow options:dst_port=6633 options:key=flow options:nsp=flow options:nsi=flow options:nshc1=flow options:nshc2=flow options:nshc3=flow options:nshc4=flow')
	s22.cmd('ovs-vsctl set-controller s22 tcp:'+MANAGER_IP+':6653')
	s22.cmd('ovs-ofctl add-flow s22 priority=100,in_port=1,action=output:2')
	s22.cmd('ovs-ofctl add-flow s22 priority=100,in_port=2,action=output:1')
	CLI( net )
	net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    exampleNet()
