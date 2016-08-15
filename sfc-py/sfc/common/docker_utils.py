import docker
import json

from docker import Client
from time import sleep

docker_client = Client(base_url='unix://var/run/docker.sock')

def create_sf_container(image='vmehmeri/sf',name='sf',recreate_if_exists=False):
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
          raise Exception('Failed to create SF container')
    return container


def start_sf_container(container):
    docker_client.start(container=container)

def stop_sf_container(container):
    found = False
    ctr = None

    if type(container) is str:
        ctr = container
    elif 'Id' in container.keys():
        ctr = container['Id']

    #Check if container is actually running

    print("Stopping container %s" % ctr)
    for container in docker_client.containers():
        print(container['Names'])
        if '/'+ctr in container['Names'] or ctr == container['Id']:
            found = True
            break

    if (found == True):
        docker_client.stop(container=container)
    else:
        print("Container is not running.")

def remove_sf_container(container):
    try:
        docker_client.remove_container(container=container, force=True)
    except:
        pass

def attach_to_sf_container(container):
    docker_client.attach(container=container, stdout=True, stderr=True)

def inspect(container):
    return docker_client.inspect_container(container)

def get_container_ip_address(container):
    ctr_dict = inspect(container)
    return ctr_dict['NetworkSettings']['Networks']['vnf-net']['IPAddress']

def get_vnf_network_id(container):
    ctr_dict = inspect(container)
    return ctr_dict['NetworkSettings']['Networks']['vnf-net']['NetworkID']

def add_container_to_vnf_network(container, ip_addr):
    net_id = None
    for nw in docker_client.networks():
        #print(json.dumps(nw,sort_keys=True, indent=4 ))

        if nw['Name'] == "vnf-net":
            net_id = nw['Id']

    if net_id == None:
        raise Exception("vnf-net not found")

    docker_client.connect_container_to_network(container=container, net_id=net_id, ipv4_address=ip_addr)


def test():
    print ("Creating container")
    ctr = create_sf_container()
    print ("Starting container")
    print (start_sf_container(ctr))
    #print (get_container_ip_address(ctr))
    input('Press any key to continue: ')

    print ("Stopping container")
    print (stop_sf_container(ctr))
    print ("Removing container")
    print (remove_sf_container(ctr))

if __name__ == "__main__":
    test()
