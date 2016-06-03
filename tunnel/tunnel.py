#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf

def exampleNet():

	LOCAL_IP='10.13.13.105'
	REMOTE1_IP='10.13.13.107'
	#REMOTE2_IP='10.13.13.108'
	CONTROLLER_IP='10.13.13.105'

	net = Mininet( topo=None,
				   build=False)

	net.addController( 'c0',
					  controller=RemoteController,
					  ip=CONTROLLER_IP,
					  port=6633)

	# Add hosts and switches
	h10 = net.addHost( 'h10', ip='10.0.0.10' )
	#h2 = net.addHost( 'h2', ip='10.0.0.2/24', mac='00:00:00:00:00:02' )
	#h3 = net.addHost( 'h3', ip='10.0.0.2/24', mac='00:00:00:00:00:03' )
	h4 = net.addHost( 'h4', ip='10.0.0.4/24' )
	h5 = net.addHost( 'h5', ip='10.0.0.5/24' )
	h6 = net.addHost( 'h6', ip='10.0.0.6/24' )
	s1 = net.addSwitch( 's1' )
	s2 = net.addSwitch( 's2' )
	s3 = net.addSwitch( 's3' )
	s4 = net.addSwitch( 's4' )
	s5 = net.addSwitch( 's5' )
	s6 = net.addSwitch( 's6' )
	s7 = net.addSwitch( 's7' )
	
	#s1 = net.addSwitch( 's1',protocols='OpenFlow10')
	#s2 = net.addSwitch( 's2',protocols='OpenFlow10')
	#s3 = net.addSwitch( 's3',protocols='OpenFlow10')
	#s4 = net.addSwitch( 's4',protocols='OpenFlow10')
	#s5 = net.addSwitch( 's5',protocols='OpenFlow10')
	#s6 = net.addSwitch( 's6',protocols='OpenFlow10')
	#s7 = net.addSwitch( 's7',protocols='OpenFlow10')

	

	# Add links
	net.addLink( h10, s1 )
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

	# Delete old tunnels if still exists
	s1.cmd('ip tun del s1-gre1')
	s2.cmd('ip tun del s2-gre1')
	# Create GRE tunnel
	print "Creating GRE tunnels..."
	s1.cmd('ip li ad s1-gre1 type gretap local '+LOCAL_IP+' remote '+REMOTE1_IP+' ttl 64')
	#s2.cmd('ip li ad s2-gre1 type gretap local '+LOCAL_IP+' remote '+REMOTE2_IP+' ttl 64')
	s1.cmd('ip li se dev s1-gre1 up')
	#s2.cmd('ip li se dev s2-gre1 up')
	Intf( 's1-gre1', node=s1 )
	#Intf( 's2-gre1', node=s2 )
	s1.cmdPrint('ovs-vsctl show')
	#print "Configuring ARP entries..."
	#h1.cmd("arp -s 10.0.0.2 00:00:00:00:00:02 -i h1-eth0")
	#h2.cmd("arp -s 10.0.0.1 00:00:00:00:00:01 -i h2-eth0")

	net.start()
	CLI( net )
	net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    exampleNet()
