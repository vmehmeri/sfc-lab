from node_template import NodeTemplate, NodeType

class VirtualLink(NodeTemplate):
    def __init__(self, node_name, node_dict):
        NodeTemplate.__init__(self, node_name, node_dict)
        self.node_type = NodeType.VL