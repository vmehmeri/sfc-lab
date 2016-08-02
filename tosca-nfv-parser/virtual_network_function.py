from node_template import NodeTemplate

class VirtualNetworkFunction(NodeTemplate):


    def __init__(self, node_name, node_dict):
        NodeTemplate.__init__(self, node_name, node_dict)
        self.node_type = node_dict['type']
        self.node_templates = {}

    def add_node_template(self, node_name, node_template):
        print("Adding node template ", node_name)
        self.node_templates[node_name] = node_template
        print(node_template)

    def get_node_templates(self):
        return self.node_templates

    def get_node_template_by_name(self, node_name):
        if node_name in self.node_templates.keys():
            return self.node_templates[node_name]
        else:
            return None

    def get_dp_connection_point(self):
        return self.get_node_template_by_name('CP_DP')

    def get_mgmt_connection_point(self):
        return self.get_node_template_by_name('CP_MGMT')

    def get_vdu(self):
        return self.get_node_template_by_name('VDU1')

    def print_self(self, prefix=""):
        print(prefix, self.node_name)
        print(prefix, "\ttype:")
        print(prefix, "\t", self.node_type)
        print(prefix, "\tdescription:")
        print(prefix, "\t", self.description)
        print(prefix, "\tproperties:")
        print(prefix, "\t", self.properties)
        print(prefix, "\trequirements:")
        print(prefix, "\t", self.requirements)

        for node_tpl in self.node_templates.values():
            node_tpl.print_self("\t")