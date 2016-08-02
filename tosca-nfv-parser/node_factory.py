from virtual_link import VirtualLink
from virtual_network_function import VirtualNetworkFunction
from connection_point import ConnectionPoint
from forwarding_path import ForwardingPath
from vdu import VDU

TOSCA_NFV_PREFIX = "tosca.nodes.nfv."

class NodeFactory():

    # Factory method
    @staticmethod
    def getNodeTemplate(node_name, node_type, node_dict):
        if (TOSCA_NFV_PREFIX + "VNF" in node_type):
            return VirtualNetworkFunction(node_name, node_dict)
        elif (TOSCA_NFV_PREFIX + "FP" in node_type):
            return ForwardingPath(node_name, node_dict)
        elif (TOSCA_NFV_PREFIX + "VL" in node_type):
            return VirtualLink(node_name, node_dict)
        elif (TOSCA_NFV_PREFIX + "CP" in node_type):
            return ConnectionPoint(node_name, node_dict)
        elif (TOSCA_NFV_PREFIX + "VDU" in node_type):
            return VDU(node_name, node_dict)
        else:
            print("Unrecognized node type")
            return None