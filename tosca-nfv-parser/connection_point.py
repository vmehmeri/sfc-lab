from node_template import NodeTemplate

class ConnectionPoint(NodeTemplate):
    def __init__(self, node_name, node_dict):
        NodeTemplate.__init__(self, node_name, node_dict)


    def get_virtual_binding(self):
        for req in self.requirements:
            if 'virtualBinding' in req.keys():
                vdu_dict = req['virtualBinding']
                return vdu_dict['node']
        return None