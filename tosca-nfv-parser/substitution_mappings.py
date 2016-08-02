
map = {}

class SubstitutionMappings():

    @staticmethod
    def addMapping(node_type, topology_dict):
        """
        Add an entry to the map node_type (e.g. tosca.nodes.nfv.VNF) -> topology template dictionary
        :param node_type:
        :param topology_dict:
        :return:
        """
        map[node_type] = topology_dict

    @staticmethod
    def getSubTemplate(node_type):
        if node_type in map.keys():
            return map[node_type]
        else:
            return None