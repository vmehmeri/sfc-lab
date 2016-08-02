from node_template import NodeTemplate

class VDU(NodeTemplate):
    def __init__(self, node_name, node_dict):
        NodeTemplate.__init__(self, node_name, node_dict)
        self.domain = None

    def get_domain(self):
        if 'constraint' in self.node_dict.keys():
            if 'domain' in self.node_dict['constraint']:
                return self.node_dict['constraint']['domain']
        return None
