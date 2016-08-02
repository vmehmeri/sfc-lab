from node_template import NodeTemplate, NodeType

class VDU(NodeTemplate):
    def __init__(self, node_name, node_dict):
        NodeTemplate.__init__(self, node_name, node_dict)
        self.node_type = NodeType.VDU
        self.domain = None


    def get_domain(self):
        if 'constraint' in self.node_dict.keys():
            if 'domain' in self.node_dict['constraint']:
                return self.node_dict['constraint']['domain']
        return None

    def get_image(self):
        return self.properties['image']