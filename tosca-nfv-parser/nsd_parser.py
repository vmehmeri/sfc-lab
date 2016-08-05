import codecs
import os
import xml.etree.cElementTree as ET
import pprint
import time
import yaml
from topology_template import TopologyTemplate
from node_template import NodeType

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
        print("reading ", filename)
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

    def parseAll(self):
        fp_acl_dict = {}
        fp_nodes_tuples = [] # list of (FP, nodes) tuples
        fps = {}

        try:
            nsd_tpl = self.topology_templates['NSD001']
        except KeyError as k:
            print("A main topology template with ID NSD001 was not found.")
            return

        fp_tpls = nsd_tpl.get_node_templates_by_type(NodeType.FP)

        for fp_tpl in fp_tpls:
            fps[fp_tpl.get_name()] = fp_tpl.get_path()
            acl = fp_tpl.get_acl_policy()
            fp_acl_dict[fp_tpl.get_name()] = acl
        for fp_name in fps.keys():
            print("path:",fp_name)
            fp = fps[fp_name]

            nodes=[] # list of forwarding nodes dictionary
            for path_node in fp:
                if "CP" in path_node:
                    node = {}
                    node['name'] = "NSD001_%s" % path_node
                    node['domain'] = "cloud" if path_node == "CP01" else "cpe"
                    nodes.append(node)
                elif "VNF" in path_node:
                    node={}
                    vnf_node = nsd_tpl.get_node_template_by_name(path_node)
                    node['name'] = vnf_node.get_name() + "_CP_DP"
                    node['domain'] = vnf_node.get_vdu().get_domain()
                    node['image'] = vnf_node.get_vdu().get_image()
                    nodes.append(node)
            fp_nodes_tuples.append((fp_name,nodes))

        self._write_to_file(fp_acl_dict, fp_nodes_tuples)


    def _write_to_file(self, fp_acl_dict, fp_nodes_tuples):
        root = ET.Element("service-config")
        for fp_nodes_tuple in fp_nodes_tuples:
            fp_name = fp_nodes_tuple[0]
            acl_dict_list = fp_acl_dict[fp_name]
            fp_tag = ET.SubElement(root,"forwarding-path")
            ET.SubElement(fp_tag, "name").text = fp_name
            acl_tag = ET.SubElement(fp_tag, "acl")

            for acl_dict in acl_dict_list:
                for key in acl_dict.keys():
                    ET.SubElement(acl_tag, key.replace("_","-")).text = str(acl_dict[key])

            #Fill in forwarding nodes
            forwarding_nodes = fp_nodes_tuple[1]
            print("forwarding_nodes: ", forwarding_nodes)
            for node in forwarding_nodes:
                node_tag = ET.SubElement(fp_tag, "node")
                ET.SubElement(node_tag, "name").text = node['name']
                ET.SubElement(node_tag, "domain").text = node['domain']
                if 'image' in node.keys():
                    ET.SubElement(node_tag, "image").text = node['image']

        tree = ET.ElementTree(root)
        self._indent(root)
        tree.write("service_config.xml")

    def _indent(self, elem, level=0):
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self._indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i