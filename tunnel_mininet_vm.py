#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf

def exampleNet():

	IP_PREFIX='192.168.137.'
	MININET_VM_IP=IP_PREFIX+'100'
	CONTROLLER_IP=IP_PREFIX+'200'
	MANAGER_IP=IP_PREFIX+'100'
	H1_VM_IP=IP_PREFIX+'10'
	H2_VM_IP=IP_PREFIX+'20'
	H3_VM_IP=IP_PREFIX+'30'

	net = Mininet( topo=None, controller=None, build=False)

	net.addController(  'c0',
						controller=RemoteController,
						ip=CONTROLLER_IP,
						port=6653 )



	# Add hosts and switches
	#h1 = net.addHost( 'h1', ip='10.0.0.1/24', mac='00:00:00:00:00:01' )
	#h2 = net.addHost( 'h2', ip='10.0.0.2/24', mac='00:00:00:00:00:02' )
	#h3 = net.addHost( 'h3', ip='10.0.0.3/24', mac='00:00:00:00:00:03' )
	h4 = net.addHost( 'h4', ip='10.0.0.4')
	h5 = net.addHost( 'h5', ip='10.0.0.5' )
	h6 = net.addHost( 'h6', ip='10.0.0.6' )

	s1 = net.addSwitch( 's1' )
	s2 = net.addSwitch( 's2' )
	s3 = net.addSwitch( 's3' )
	s4 = net.addSwitch( 's4' )
	s5 = net.addSwitch( 's5' )
	s6 = net.addSwitch( 's6' )
	s7 = net.addSwitch( 's7' )

	# Add links
	#net.addLink( h1, s1 )
	#net.addLink( h2, s2 )
	#net.addLink( h3, s4 )
	net.addLink( h4, s4 )
	net.addLink( h5, s2 )
	net.addLink( h6, s3 )

	net.addLink( s1, s5 )
	net.addLink( s1, s2 )
	net.addLink( s2, s4 )
	net.addLink( s2, s3 )
	net.addLink( s2, s7 )
	net.addLink( s3, s4 )
	net.addLink( s3, s6 )
	net.addLink( s4, s5 )
	net.addLink( s4, s7 )
	net.addLink( s6, s7 )


	## Configure GRE tunnel ##

	# Delete old tunnel if still exists
	s1.cmd('ip tun del s1-gre1')
	s2.cmd('ip tun del s2-gre1')
	s4.cmd('ip tun del s4-gre1')

	# Create GRE tunnels
	print "Creating GRE tunnels..."

	s1.cmd('ip li ad s1-gre1 type gretap local '+MININET_VM_IP+' remote '+H1_VM_IP+' ttl 64')
	s1.cmd('ip li se dev s1-gre1 up')
	Intf( 's1-gre1', node=s1 )

	s2.cmd('ip li ad s2-gre1 type gretap local '+MININET_VM_IP+' remote '+H2_VM_IP+' ttl 64')
	s2.cmd('ip li se dev s2-gre1 up')
	Intf( 's2-gre1', node=s2 )

	s4.cmd('ip li ad s4-gre1 type gretap local '+MININET_VM_IP+' remote '+H3_VM_IP+' ttl 64')
	s4.cmd('ip li se dev s4-gre1 up')
	Intf( 's4-gre1', node=s4 )

	#print "Configuring ARP entries..."
	#h1.cmd("arp -s 10.0.0.7 00:00:00:00:00:07 -i h1-eth0")
	#h2.cmd("arp -s 10.0.0.1 00:00:00:00:00:01 -i h2-eth0")

	net.start()
	CLI( net )
	net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    exampleNet()
