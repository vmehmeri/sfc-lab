# sfc-lab

INSTALL OVS-NSH-v8
sudo apt-get update
sudo apt-get install curl git autoconf libtool
curl https://raw.githubusercontent.com/priteshk/ovs/nsh-v8/third-party/start-ovs-deb.sh | bash

ODL SFC-BERYLLIUM
git clone https://git.opendaylight.org/gerrit/p/sfc.git --branch stable/beryllium

Or from the full beryllium release, install features:
odl-sfc-model odl-sfc-provider odl-sfc-provider-rest odl-sfc-netconf odl-sfc-ovs odl-sfc-scf-openflow odl-sfcofl2 odl-sfclisp odl-sfc-sb-rest odl-sfc-ui

odl-config-manager-facade-xml odl-config-startup odl-config-persister odl-mdsal-models odl-netconf-notifications-api odl-netconf-client odl-netconf-netty-util odl-netconf-util odl-netconf-mapping-api odl-netconf-api odl-lmax odl-netty odl-mdsal-broker odl-mdsal-remoterpc-connector odl-mdsal-distributed-datastore odl-mdsal-clustering-commons odl-mdsal-broker-local odl-mdsal-common odl-mdsal-binding-runtime odl-mdsal-binding-base odl-aaa-shiro odl-ovsdb-library odl-config-all odl-ovsdb-southbound-impl  odl-ovsdb-southbound-api management ssh kar war http package region config standard pax-war pax-http-whiteboard pax-http pax-jetty odl-mdsal-apidocs odl-restconf-noauth odl-restconf odl-netconf-connector odl-openflowplugin-nxm-extensions odl-lispflowmapping-models odl-lispflowmapping-southbound odl-lispflowmapping-inmemorydb odl-lispflowmapping-mappingservice odl-yangtools-yang-parser odl-yangtools-common odl-yangtools-yang-data odl-openflowjava-protocol odl-protocol-framework odl-aaa-authn odl-openflowplugin-app-lldp-speaker odl-openflowplugin-app-config-pusher odl-openflowplugin-nsf-model odl-openflowplugin-nsf-services  odl-openflowplugin-flow-services odl-openflowplugin-southbound odl-aaa-api odl-akka-persistence odl-akka-leveldb odl-akka-clustering odl-akka-system odl-akka-scala odl-config-netty

SETUP SF
sudo apt-get update -y
sudo apt-get install autoconf libtool git python3-flask libssl-dev openssl libnetfilter-queue-dev python3-pip python3-flask   -y
sudo pip3 install sfc paramiko flask
git clone https://git.opendaylight.org/gerrit/p/sfc.git --branch stable/beryllium
cd sfc/sfc-py
sudo ./start_agent.sh <CONTROLLER_IP>:8181

MANUAL CREATION OF OVS VxLAN PORT 
sudo ovs-vsctl add-port s11 sff0-dpl -- set interface sff0-dpl type=vxlan options:remote_ip=flow options:dst_port=6633 options:key=flow options:nsp=flow options:nsi=flow options:nshc1=flow options:nshc2=flow options:nshc3=flow options:nshc4=flow
