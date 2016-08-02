from node_template import NodeTemplate
from node_factory import NodeFactory
from node_template import NodeType
from substitution_mappings import SubstitutionMappings

class TopologyTemplate():


    def __init__(self, tpl_dict):
        self.tpl_dict = {}
        self.inputs = {}
        self.node_templates = {}
        self.topology_templates = {}
        self.tpl_dict = tpl_dict
        self._find_node_templates()

    def _find_node_templates(self):
        node_tpls_root_dict = self.tpl_dict['topology_template']['node_templates']

        for node_name in node_tpls_root_dict.keys():
            node_type = node_tpls_root_dict[node_name]['type']
            print( "Found node template %s of type %s" % (node_name, node_type) )
            #if ("tosca.nodes.nfv.VNF" in node_type):
            #    # TODO: verify
            #    self.topology_templates[node_name] = TopologyTemplate(SubstitutionMappings.getSubTemplate(node_type))
            #else:
            self.node_templates[node_name] = NodeFactory.getNodeTemplate(node_name, node_type, node_tpls_root_dict[node_name])

    def get_node_templates(self):
        return self.node_templates

    def get_node_template_by_name(self, node_name):
        if node_name in self.node_templates.keys():
            return self.node_templates[node_name]
        else:
            return None

    def get_node_templates_by_type(self, node_type):
        node_tpls = []
        for node in self.node_templates.values():
            if node.get_type() == node_type:
                node_tpls.append(node)
        return node_tpls

    def print_self(self):
        for node in self.node_templates:
            node.print_self()

    def get_dict(self):
        return self.tpl_dict