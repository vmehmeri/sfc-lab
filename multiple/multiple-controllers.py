import docker
import json

from docker import Client
from time import sleep
import sys

docker_client = Client(base_url='unix://var/run/docker.sock')

def create_pox_container(name, image='vmehmeri/pox',recreate_if_exists=False):
    container = None
    try:
      container = docker_client.create_container(image=image, name=name, detach=False)
    except :
      for cntr in docker_client.containers():
        if ("/"+name) in cntr['Names']:
          print ("Found existing container with same name (Id #%s). " % cntr['Id'])
          if (recreate_if_exists):
            print("Stopping...")
            stop_sf_container(cntr['Id'])
            remove_sf_container(cntr['Id'])
            sleep(3);
            print ("Recreating...")
            container = docker_client.create_container(image=image, name=name, detach=False)
          else:
            return cntr['Id']
        else:
          #TODO create specific exception for this
          raise Exception('Could not create SF container')
    return container


def start_container(container):
    response = docker_client.start(container=container)
    return response

def stop_container(container):
    response = docker_client.stop(container=container)
    return response

def remove_container(container):
    response = docker_client.remove_container(container=container, force=True)
    return response

def inspect(container):
    return docker_client.inspect_container(container)

def get_container_ip_address(container):
    ctr_dict = inspect(container)
    return ctr_dict['NetworkSettings']['Networks']['bridge']['IPAddress']

#def get_vnf_network_id(container):
#    ctr_dict = inspect(container)
#    return ctr_dict['NetworkSettings']['Networks']['vnf-net']['NetworkID']

#def add_container_to_vnf_network(container, ip_addr):
#    net_id = None
#    for nw in docker_client.networks():
#        #print(json.dumps(nw,sort_keys=True, indent=4 ))
#
#        if nw['Name'] == "vnf-net":
#            net_id = nw['Id']
#
#    if net_id == None:
#        raise Exception("vnf-net not found")
#
#    docker_client.connect_container_to_network(container=container, net_id=net_id, ipv4_address=ip_addr)

def stop_and_remove_all(containers):
    for cntr_name in containers.keys():
        cntr_id = containers[cntr_name]['id']
        print("Stopping container %s" % cntr_name)
        stop_container(cntr_id)
        print("Removing container %s" % cntr_name)
        remove_container(cntr_id)
        sleep(1)

def test():
    containers = {}
    for indx in range(0,int(sys.argv[1])):
        name = "pox_%d" % indx
        containers[name] = {}
        containers[name]['id'] = create_pox_container(name=name)
        containers[name]['started'] = True if start_container(containers[name]['id']) is None else False
        print("Started container ", name, " - ", get_container_ip_address(containers[name]['id']))
        sleep(1)
    return containers

def output_log(container_id):
    docker_client.logs(container=container_id, stream=True, tail="all", follow=True)

if __name__ == "__main__":
    ctrs = {}
    ctrs = test()
