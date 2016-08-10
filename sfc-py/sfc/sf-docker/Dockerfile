FROM ubuntu:14.04
MAINTAINER Victor Mehmeri
RUN apt-get update 
RUN apt-get install python -y 
COPY . /home/root
CMD python /home/root/vxlan_tool.py -i eth1 -d forward -v on
