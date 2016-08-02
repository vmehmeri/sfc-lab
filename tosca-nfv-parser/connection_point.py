from node_template import NodeTemplate, NodeType

class ConnectionPoint(NodeTemplate):
    def __init__(self, node_name, node_dict):
        NodeTemplate.__init__(self, node_name, node_dict)
        self.node_type = NodeType.CP


    def get_virtual_binding(self):
        for req in self.requirements:
            if 'virtualBinding' in req.keys():
                vdu_dict = req['virtualBinding']
                return vdu_dict['node']
        return None