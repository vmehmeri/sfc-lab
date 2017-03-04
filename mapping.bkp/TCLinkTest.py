#!/usr/bin/env python
import utils

from optical import LINCNet, LINCSwitch, LINCLink

from mininet.node import OVSSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import Intf, TCLink
from mininet.net import Mininet
from mininet.log import lg, info, error, debug, output

def start(ip="192.168.137.150",port=6633):

    classifier1_intfName = 'eth1'
    classifier2_intfName = 'eth2'
    sff1_intfName = 'eth3'
    sff2_intfName = 'eth4'

    # Set up logging etc.
    lg.setLogLevel('info')
    lg.setLogLevel('output')

    ctrlr = lambda n: RemoteController(n, ip=ip, port=port, inNamespace=False)
    ctrlr2 = RemoteController('2', ip='192.168.137.160', port=port, inNamespace=False)
    net = LINCNet(switch=OVSSwitch, controller=ctrlr, autoStaticArp=True, listenPort=6634)
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

    # Add optical switches
    r1 = net.addSwitch('r1', dpid='00:00:00:00:00:00:00:11', cls=LINCSwitch)
    r2 = net.addSwitch('r2', dpid='00:00:00:00:00:00:00:12', cls=LINCSwitch)
    r3 = net.addSwitch('r3', dpid='00:00:00:00:00:00:00:13', cls=LINCSwitch)
    r4 = net.addSwitch('r4', dpid='00:00:00:00:00:00:00:14', cls=LINCSwitch)
    r5 = net.addSwitch('r5', dpid='00:00:00:00:00:00:00:15', cls=LINCSwitch)
    r6 = net.addSwitch('r6', dpid='00:00:00:00:00:00:00:16', cls=LINCSwitch)
    r7 = net.addSwitch('r7', dpid='00:00:00:00:00:00:00:17', cls=LINCSwitch)
    r8 = net.addSwitch('r8', dpid='00:00:00:00:00:00:00:18', cls=LINCSwitch)

    # Connect hosts to packet switches
    #print "Adding physical hosts to mininet network..."
    _intf1 = Intf( classifier1_intfName, node=s1, port=1 )
    _intf2 = Intf( sff1_intfName, node=s1, port=2 )
    _intf3 = Intf( classifier2_intfName, node=s2, port=1 )
    _intf4 = Intf( sff2_intfName, node=s2, port=2 )

    #net.addLink(h1, s1)
    #net.addLink(h2, s2)
    #net.addLink(h101, s1)
    #net.addLink(h102, s2)
    linkopts = dict(bw=100, delay='1ms', max_queue_size=500, loss=0, use_htb=True)
    print "Adding Links..."
    # Connect packet switches to optical switches
    net.addLink(s1, r1, port1=3, port2=1, speed1=100, annotations={ "bandwidth": 100, "durable": "true" }, cls=LINCLink)
    net.addLink(s1, r1, port1=4, port2=2, speed1=100, annotations={ "bandwidth": 100, "durable": "true" }, cls=LINCLink)
    net.addLink(s2, r2, port1=3, port2=1, speed1=100, annotations={ "bandwidth": 100, "durable": "true" }, cls=LINCLink)
    net.addLink(s2, r2, port1=4, port2=2, speed1=100, annotations={ "bandwidth": 100, "durable": "true" }, cls=LINCLink)

    # Connect optical switches to each other
    net.addLink(r1, r3, port1=3, port2=1, speed1=100, annotations={ "bandwidth": 100, "durable": "true" }, cls=LINCLink)
    net.addLink(r1, r5, port1=4, port2=1, speed1=100, annotations={ "bandwidth": 100, "durable": "true" }, cls=LINCLink)
    net.addLink(r1, r6, 5, 1, cls=LINCLink)
    net.addLink(r1, r7, 6, 1, cls=LINCLink)
    net.addLink(r2, r4, 3, 2, cls=LINCLink)
    net.addLink(r2, r5, 4, 2, cls=LINCLink)
    net.addLink(r2, r6, 5, 2, cls=LINCLink)
    net.addLink(r2, r8, 6, 2, cls=LINCLink)
    net.addLink(r3, r4, 2, 1, cls=LINCLink)
    net.addLink(r7, r8, 2, 1, cls=LINCLink)

    # Start the network and prime other ARP caches
    net.start()
    # Uncomment below if using virtal hosts
    #net.staticArp()

    #Uncomment below if using physical hosts
    #print "Configuring ARP entries..."
    #utils.setStaticArp()

    # Enter CLI mode
    output("Network ready\n")
    output("Press Ctrl-d or type exit to quit\n")
    CLI(net)
    net.stop()

start()
