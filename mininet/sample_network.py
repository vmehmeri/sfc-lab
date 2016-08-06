#!/usr/bin/env python
from mininet.node import OVSSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import Intf
from mininet.net import Mininet
from mininet.log import lg, info, error, debug, output

def start(controllers=[{'ip':'127.0.0.1', 'port': 6633}]):

    # Set up logging
    lg.setLogLevel('info')
    lg.setLogLevel('output')

    net = Mininet(switch=OVSSwitch, controller=None, autoStaticArp=True, listenPort=6634)

    for indx, ctl in enumerate(controllers):
        net.addController(('c%d' % indx), controller=RemoteController, ip=ctl['ip'], port=ctl['port'])


    # Add hosts
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')

    #physical_intf = 'eth1'

    #Add switch that accepts only OpenFlow 1.0
    s1 = net.addSwitch('s1', dpid='00:00:00:00:00:00:00:01', protocols='OpenFlow10')

    #Will accept both OpenFlow 1.0 and 1.3
    #s2 = net.addSwitch('s2', dpid='00:00:00:00:00:00:00:02', protocols='OpenFlow10,OpenFlow13')

    #Will accept all protocols support by openvswitch
    #s3 = net.addSwitch('s2', dpid='00:00:00:00:00:00:00:02')

    # Connect physical interface
    #print "Adding physical hosts to mininet network..."
    #_intf1 = Intf( physical_intf, node=s1, port=1 )


    net.addLink(h1, s1)
    net.addLink(h2, s1)


    # Start the network and prime other ARP caches
    net.start()
    net.staticArp()

    # Enter CLI mode
    output("Network ready\n")
    output("Press Ctrl-d or type exit to quit\n")
    CLI(net)
    net.stop()

if __name__ == "__main__":
    controllers = []
    for i in range(2,22):
        ctrl = {}
        ctrl['ip'] = '172.17.0.%d' % i
        ctrl['port'] = 6633
        controllers.append(ctrl)

    start(controllers)
