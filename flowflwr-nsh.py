import os
from difflib import *
from time import sleep
import subprocess
import re

POLLING_INTERVAL=0.5
cmd='ovs-ofctl'
remove_info=['idle_age', 'hard_timeout', 'n_bytes']

#cmd = "sudo ovs-ofctl dump-flows br-sfc -OOpenFlow13 | grep n_packets=[^0]"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def dump_flows(bridge_name, protocol='OpenFlow10'):
    __p = subprocess.Popen([cmd, 'dump-flows', bridge_name, '-O%s' % protocol], stdout=subprocess.PIPE)
    _p = subprocess.Popen(['grep', '-o', 'table=.*'], stdin=__p.stdout, stdout=subprocess.PIPE)
    p = subprocess.Popen(['grep', 'packets=[0-9][0-9]*'], stdin=_p.stdout, stdout=subprocess.PIPE)
    out = p.stdout.read()

    __p = subprocess.Popen([cmd, 'dump-flows', bridge_name, '-O%s' % protocol], stdout=subprocess.PIPE)
    _p = subprocess.Popen(['grep', '-o', 'table=.*'], stdin=__p.stdout, stdout=subprocess.PIPE)
    p = subprocess.Popen(['grep', 'packets=[0-9][0-9]*'], stdin=_p.stdout, stdout=subprocess.PIPE)
    _n_packets = subprocess.Popen(['grep','-o', 'packets=[0-9][0-9]*'], stdin=p.stdout, stdout=subprocess.PIPE)
    n_packets = subprocess.Popen(['grep','-o', '[0-9][0-9]*'], stdin=_n_packets.stdout, stdout=subprocess.PIPE)
    n_packets = n_packets.stdout.read()

    #Remove unwanted info
    for info in remove_info:
        out = re.sub("%s=[0-9]*," % info ,"",out)

    out = re.sub(",  ",":",out)
    return out, n_packets


while True:
    out1, n_packets1 = dump_flows('s1', 'OpenFlow10')
    sleep(POLLING_INTERVAL)
    out2, n_packets2 = dump_flows('s1', 'OpenFlow10')

    out2arr = out2.splitlines()

    n_packets1arr = n_packets1.splitlines()
    n_packets2arr = n_packets2.splitlines()

    for i in range(0, min(len(n_packets1arr),len(n_packets2arr))):
        if len(out2arr) == len(n_packets1arr) and n_packets1arr[i] != n_packets2arr[i]:
            if "set_nsp" in out2arr[i]:
                print bcolors.HEADER + "[CLSF FLOW HIT]" + bcolors.ENDC, out2arr[i]
            else if "nsp=" in out2arr[i]:
                print bcolors.OKBLUE + "[SFF FLOW HIT]" + bcolors.ENDC, out2arr[i]
            else:
                print bcolors.OKGREEN + "[FLOW HIT]" + bcolors.ENDC, out2arr[i]
