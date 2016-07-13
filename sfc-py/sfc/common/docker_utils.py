import docker

from docker import Client

docker_client = Client(base_url='unix://var/run/docker.sock')

def create_sf_container(image='vmehmeri/sf',name='sf'):
    try:
      container = docker_client.create_container(image=image, name=name, detach=False) #command='sudo python /home/root/vxlan_tool.py -i eth0 -d forward -v on')
    except :
      for cntr in docker_client.containers():
        if ("/"+name) in cntr['Names']:
          print ("Found existing container with same name (Id #%s). Removing it..." % cntr['Id'])
          stop_sf_container(cntr['Id'])
          remove_sf_container(cntr['Id'])
          print ("Recreating...")
          container = docker_client.create_container(image=image, name=name, detach=False)
        else:
          #TODO create specific exception for this
          raise Exception('Could not create SF container')
    return container


def start_sf_container(container):
    response = docker_client.start(container=container)
    return response

def stop_sf_container(container):
    response = docker_client.stop(container=container)
    return response

def remove_sf_container(container):
    response = docker_client.remove_container(container=container, force=True)
    return response

def attach_to_sf_container(container):
    docker_client.attach(container=container, stdout=True, stderr=True)

def test_start_sf_container():
    print ("Creating container")
    ctr = create_sf_container()
    print (ctr)
    print ("Starting container")
    print (start_sf_container(ctr))
    #attach_to_sf_container(ctr)
    input('Press any key to continue: ')

    print ("Stopping container")
    print (stop_sf_container(ctr))
    print ("Removing container")
    print (remove_sf_container(ctr))
