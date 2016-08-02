import pprint
from enum import Enum
pp = pprint.PrettyPrinter(indent=2)

class NodeTemplate():
    """
    node_name : name of this node template as defined in the parent topology template
    node_dict = the dictionary representing this node
    node_type = this node type
    description = node template description
    properties = node template properties
    requirements = nodetemplate requirements
    """

    def __init__(self, node_name, node_dict):
        self.node_name = node_name
        self.node_dict = node_dict
        self.node_type = None
        self.description = node_dict['description'] if 'description' in node_dict.keys() else None
        self.properties = node_dict['properties'] if 'properties' in node_dict.keys() else None
        self.requirements = node_dict['requirements'] if 'requirements' in node_dict.keys() else None

    def get_type(self):
        return self.node_type

    def get_name(self):
        return self.node_name

    def get_description(self):
        return self.description

    def get_properties(self):
        return self.properties

    def get_requirements(self):
        return self.requirements

    def print_self(self, prefix=""):
        print (prefix, self.node_name)
        print(prefix, "\ttype:")
        print(prefix, "\t",self.node_type)
        print(prefix, "\tdescription:")
        print(prefix, "\t",self.description)
        print(prefix, "\tproperties:")
        print(prefix, "\t",self.properties)
        print(prefix, "\trequirements:")
        print(prefix, "\t",self.requirements)

class NodeType(Enum):
    VNF = "tosca.nodes.nfv.VNF"
    FP = "tosca.nodes.nfv.FP"
    VL = "tosca.nodes.nfv.VL"
    CP = "tosca.nodes.nfv.CP"
    VDU = "tosca.nodes.nfv.VDU"


