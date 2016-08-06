#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf

def exampleNet():

	LOCAL_IP='10.13.13.110'
	REMOTE_IP='10.13.13.105'
	CONTROLLER_IP='10.13.13.105'

	net = Mininet( topo=None,
				   build=False)

	net.addController( 'c0',
					  controller=RemoteController,
					  ip=CONTROLLER_IP,
					  port=6633)

	# Add hosts and switches
	h7 = net.addHost( 'h6', ip='10.0.0.7/24', mac='00:00:00:00:00:07' )
	s8 = net.addSwitch( 's8' )
	

	# Add links
	net.addLink( h7, s8 )
	
	## Configure GRE tunnel ##

	# Delete old tunnel if still exists
	s8.cmd('ip tun del s8-gre1')
	# Create GRE tunnel
	#print "Creating GRE tunnel..."
	s8.cmd('ip li ad s8-gre1 type gretap local '+LOCAL_IP+' remote '+REMOTE_IP+' ttl 64')
	s8.cmd('ip li se dev s8-gre1 up')
	Intf( 's8-gre1', node=s8 )
	
	print "Configuring ARP entries..."
	#h1.cmd("arp -s 10.0.0.7 00:00:00:00:00:07 -i h1-eth0")
	h7.cmd("arp -s 10.0.0.1 00:00:00:00:00:01 -i h7-eth0")

	net.start()
	CLI( net )
	net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    exampleNet()
