import codecs
import os
import xml.etree.cElementTree as ET
import pprint
import yaml
from topology_template import TopologyTemplate

from os import listdir
from os.path import isfile, join

_catalogue = [f for f in listdir("yaml/") if isfile(join("yaml/", f))]

pp = pprint.PrettyPrinter(indent=2)


def _get_templates():
    """
    This will read all files under yaml directory
    :return:
    """
    tpls = []

    for filename in _catalogue:
        f = codecs.open("yaml/"+filename, encoding='utf-8', errors='strict')
        tpls.append(f.read())

    return tpls


def log(obj):
    """
    Print out obj
    :param obj: object to be printed
    :return:
    """
    pp.pprint(obj)

def dict_compare(d1, d2):
    """
    Utility function to compare two dicts
    :param d1: dictionary 1
    :param d2: dictionary 2
    :return: added diff (d1 - d2), removed diff (d2 - d1), modified diff, same diff
    """
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o: (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    same = set(o for o in intersect_keys if d1[o] == d2[o])
    return added, removed, modified, same

class NsdParser():
    def __init__(self):
        self.tosca_templates = _get_templates()
        self.topology_dictionaries = {} #map [ID, Dictionary]
        self.topology_templates = {} #map [ID, TopologyTemplate]
        self.substitution_map = {}

        for tpl in self.tosca_templates:
            tpl_dict = yaml.load(tpl)
            tpl_id = tpl_dict['metadata']['ID']
            self.topology_dictionaries[tpl_id] = tpl_dict
            self.topology_templates[tpl_id] = TopologyTemplate(tpl_dict)

        #Find substitution mappings in template files
        for tpl_id in self.topology_dictionaries.keys():
            if 'substitution_mappings' in self.topology_dictionaries[tpl_id]['topology_template'].keys():
                #Get the node type associated with the substitution mappings
                node_type = self.topology_dictionaries[tpl_id]['topology_template']['substitution_mappings']['node_type']
                print ("adding template ID %s to substitution mappings" % tpl_id)
                self.substitution_map[node_type] = self.topology_templates[tpl_id]

        #Look for node templates whose node_type is associated with a substitution map
        #(i.e, node templates that are actually topology templates) then load its own
        # node templates
        for topo_tpl in self.topology_templates.values():
            for node_name in topo_tpl.get_node_templates().keys():
                node_template = topo_tpl.get_node_templates()[node_name]
                if node_template.get_type() in self.substitution_map.keys():
                    print ("Found substitution map for node type ", node_template.get_type())
                    sub_topo_tpl = self.substitution_map[node_template.get_type()]
                    for sub_node_tpl in sub_topo_tpl.get_node_templates().values():
                        node_template.add_node_template(sub_node_tpl.get_name(), sub_node_tpl)

    #def get_node_dict_from_nsd(self, nsd_dict, node_name):
    #    nsd_node_tpls_dict = nsd_dict['topology_template']['node_templates']
    #    node_dict_from_nsd = nsd_node_tpls_dict[node_name]

    #    return node_dict_from_nsd

    def print_all(self):
        for topo_tpl_id in self.topology_templates.keys():
            print(topo_tpl_id,":")
            node_tpls = self.topology_templates[topo_tpl_id].get_node_templates()
            for node_tpl_name in node_tpls.keys():
                node_tpls[node_tpl_name].print_self()

    def test(self):

        nsd_tpl = self.topology_templates['NSD001']
        fp = nsd_tpl.get_node_template_by_name('Forwarding path1').get_path()
        print("path:",fp)
        nodes=[]
        for path_node in fp:
            if "CP" in path_node:
                node = {}
                node['name'] = "NSD001_%s" % path_node
                node['domain'] = "cloud" if path_node == "CP01" else "cpe"
                nodes.append(node)
            elif "VNF" in path_node:
                node={}
                vnf_node = nsd_tpl.get_node_template_by_name(path_node)
                node['name'] = "VNFD001_CP_DP"
                node['domain'] = vnf_node.get_vdu().get_domain()
                nodes.append(node)

        self.write_to_file(nodes)


    def write_to_file(self, nodes):
        root = ET.Element("forwarding-path")

        for node in nodes:
            node_tag = ET.SubElement(root, "node")
            ET.SubElement(node_tag, "name").text = node['name']
            ET.SubElement(node_tag, "domain").text = node['domain']

        tree = ET.ElementTree(root)
        tree.write("service_config.xml")

