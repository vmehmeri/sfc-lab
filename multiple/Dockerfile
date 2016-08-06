FROM ubuntu:14.04
MAINTAINER Victor Mehmeri
RUN apt-get update
RUN apt-get install python git -y
COPY . /home/root
CMD python /home/root/pox/pox.py pox.multiple.py
