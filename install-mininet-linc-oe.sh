#!/bin/bash

cd
git clone git://github.com/mininet/mininet
cd mininet
wget 'https://wiki.onosproject.org/download/attachments/4164175/multi_controller.patch?version=1&modificationDate=1443649770762&api=v2' -O multi_controller.patch
git apply multi_controller.patch
sudo ./util/install.sh -3fnv
# role back CPqD to a version known to work
cd
cd ~/ofsoftswitch13/
make clean
git reset --hard 8d3df820f7487f541b3f5862081a939aad76d8b5
sudo make install
# Install LINC-OE
cd
git clone https://github.com/FlowForwarding/LINC-Switch.git linc-oe
cd linc-oe
sed -i s/3000/300000/ rel/files/vm.args
cp rel/files/sys.config.orig rel/files/sys.config
make
cd
git clone https://github.com/FlowForwarding/LINC-config-generator.git
cd LINC-config-generator
cp priv/* .
make
