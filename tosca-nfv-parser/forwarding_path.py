from node_template import NodeTemplate

class ForwardingPath(NodeTemplate):

    def __init__(self, node_name, node_dict):
        NodeTemplate.__init__(self, node_name, node_dict)
        self.path = []

        for req_dict in self.requirements:
            if 'forwarder' in req_dict.keys():
                self.path.append(req_dict['forwarder'])

    def get_path(self):
        """
        Get Forwarding Path as a list of forwarding nodes
        :return: list representing path
        """
        return self.path

