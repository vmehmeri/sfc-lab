#!/usr/bin/env python
import arp
import os

from optical import LINCNet, LINCSwitch, LINCLink

from mininet.node import OVSSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import Intf, TCLink
from mininet.net import Mininet
from mininet.log import lg, info, error, debug, output

def start(ip="192.168.137.111",port=6633):

    dc1_intfName = 'eth1'
    dc2_intfName = 'eth2'
    dc3_intfName = 'eth3'
    dc3_2_intfName = 'eth4'
    #sff1_intfName = 'eth3'
    #sff2_intfName = 'eth4'

    # Set up logging etc.
    lg.setLogLevel('info')
    lg.setLogLevel('output')

    print ("Adding controller")
    ctrlr = lambda n: RemoteController(n, ip=ip, port=port, inNamespace=False)
    ctrlr2 = RemoteController('2', ip='192.168.137.150', port=port, inNamespace=False)
    net = LINCNet(switch=OVSSwitch, link=LINCLink, controller=ctrlr, autoStaticArp=True, listenPort=6634)
    c1 = net.addController('c1')
    #c2 = net.addController('c2',controller=RemoteController, ip='192.168.137.62',port=6633)
    c2 = net.addController(ctrlr2)

    # Add hosts
    #h1 = net.addHost('h1')
    #h2 = net.addHost('h2')
    #h101 = net.addHost('h101')
    #h102 = net.addHost('h102')

    # Add packet switches to connect hosts to the optical network
    s1 = net.addSwitch('s1', dpid='00:00:00:00:00:00:00:01', protocols='OpenFlow10')
    s2 = net.addSwitch('s2', dpid='00:00:00:00:00:00:00:02', protocols='OpenFlow10')
    s3 = net.addSwitch('s3', dpid='00:00:00:00:00:00:00:03', protocols='OpenFlow10')

    # Add optical switches
    r1 = net.addSwitch('r1', dpid='00:00:00:00:00:00:00:11', cls=LINCSwitch)
    r2 = net.addSwitch('r2', dpid='00:00:00:00:00:00:00:12', cls=LINCSwitch)
    r3 = net.addSwitch('r3', dpid='00:00:00:00:00:00:00:13', cls=LINCSwitch)
    r4 = net.addSwitch('r4', dpid='00:00:00:00:00:00:00:14', cls=LINCSwitch)
    r5 = net.addSwitch('r5', dpid='00:00:00:00:00:00:00:15', cls=LINCSwitch)
    r6 = net.addSwitch('r6', dpid='00:00:00:00:00:00:00:16', cls=LINCSwitch)
    r7 = net.addSwitch('r7', dpid='00:00:00:00:00:00:00:17', cls=LINCSwitch)

    # Connect hosts to packet switches
    print ("Adding physical hosts to mininet network...")
    _intf1 = Intf( dc1_intfName, node=s1, port=1 )
    _intf2 = Intf( dc2_intfName, node=s2, port=1 )
    _intf3 = Intf( dc3_intfName, node=s3, port=1 )
    _intf3 = Intf( dc3_2_intfName, node=s3, port=6 )

    #net.addLink(h1, s1)
    #net.addLink(h2, s2)

    #linkopts = dict(bw=1, delay='1ms', max_queue_size=500,loss=10,use_htb=True)

    # Connect packet switches to optical switches
    net.addLink(s1, r1, 2, 1, cls=LINCLink) #, bw=10, delay='5ms', loss=10, max_queue_size=1000, use_htb=True
    net.addLink(s1, r1, 3, 2, cls=LINCLink)
    net.addLink(s2, r3, 2, 1, cls=LINCLink)
    net.addLink(s2, r3, 3, 2, cls=LINCLink)
    net.addLink(s3, r5, 2, 3, cls=LINCLink)
    net.addLink(s3, r5, 3, 4, cls=LINCLink)
    net.addLink(s3, r5, 4, 5, cls=LINCLink)
    net.addLink(s3, r5, 5, 6, cls=LINCLink)

    # Connect optical switches to each other
    net.addLink(r1, r2, 3, 1, cls=LINCLink)
    net.addLink(r1, r7, 4, 1, cls=LINCLink)
    net.addLink(r2, r3, 2, 3, cls=LINCLink)
    net.addLink(r3, r4, 4, 1, cls=LINCLink)
    net.addLink(r3, r6, 5, 2, cls=LINCLink)
    net.addLink(r4, r7, 3, 2, cls=LINCLink)
    net.addLink(r4, r5, 2, 1, cls=LINCLink)
    net.addLink(r5, r6, 2, 3, cls=LINCLink)
    net.addLink(r6, r7, 1, 3, cls=LINCLink)

    # Start the network and prime other ARP caches
    net.start()

    
    # Uncomment below if using virtual hosts
    #net.staticArp()

    #Uncomment below if using physical hosts
    print "Configuring ARP entries..."
    arp.setStaticArp()
    os.system("./setup_links.sh")
    
    # Enter CLI mode
    output("Network ready\n")
    output("Press Ctrl-d or type exit to quit\n")
    CLI(net)
    net.stop()

try:
    start()
finally:
    os.system("sudo pkill epmd")
