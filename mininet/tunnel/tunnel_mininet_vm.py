#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf

def exampleNet():

	IP_PREFIX='192.168.137.'
	MININET_VM_IP=IP_PREFIX+'110'
	CONTROLLER_IP=IP_PREFIX+'110'
	#MANAGER_IP=IP_PREFIX+'100'
	H1_VM_IP=IP_PREFIX+'10'
	H2_VM_IP=IP_PREFIX+'20'
	H3_VM_IP=IP_PREFIX+'30'
	
	#intfName = 'eth1'
	#_intf = Intf( intfName, node=s1 )

	net = Mininet( topo=None, controller=None, build=False)

	net.addController(  'c0',
						controller=RemoteController,
						ip=CONTROLLER_IP,
						port=6633 )



	# Add hosts and switches
	h1 = net.addHost( 'h1', ip='10.0.0.1', mac='00:00:00:00:00:01')
	h2 = net.addHost( 'h2', ip='10.0.0.2', mac='00:00:00:00:00:02' )
	h3 = net.addHost( 'h3', ip='10.0.0.3', mac='00:00:00:00:00:03' )
	h4 = net.addHost( 'h4', ip='10.0.0.4' )
	h5 = net.addHost( 'h5', ip='10.0.0.5' )
	h6 = net.addHost( 'h6', ip='10.0.0.6' )

	s1 = net.addSwitch( 's1', protocols='OpenFlow10' )
	s2 = net.addSwitch( 's2', protocols='OpenFlow10' )
	s3 = net.addSwitch( 's3', protocols='OpenFlow10' )
	s4 = net.addSwitch( 's4', protocols='OpenFlow10' )
	s5 = net.addSwitch( 's5', protocols='OpenFlow10' )
	s6 = net.addSwitch( 's6', protocols='OpenFlow10' )
	s7 = net.addSwitch( 's7', protocols='OpenFlow10' )

	# Add links
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
	
	
	net.addLink( h1, s1 )
	net.addLink( h2, s2 )
	net.addLink( h3, s4 )
	net.addLink( h4, s4 )
	net.addLink( h5, s2 )
	net.addLink( h6, s3 )
	
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
	
	net.start()
	print "Configuring ARP entries..."
	net.staticArp()
	
	s1.cmd('sudo ovs-ofctl add-flow s1 priority=65535,tcp,in_port=3,nw_src=10.0.0.0/8,nw_dst=10.0.0.0/8,tp_dst=80,actions=output:4')
	s4.cmd('sudo ovs-ofctl add-flow s4 priority=65535,tcp,in_port=5,actions=output:3')
	
	CLI( net )
	net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    exampleNet()
