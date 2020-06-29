
import Utils
from TannerGraph import TannerGraph

class ProtographLDPC(TannerGraph):

    # args: protograph, growth factor
    def __init__(self, args, construction):
        TannerGraph.__init__(self, args, construction=construction, ldpc="protographLDPC")
        self.tanner_graph = ProtographLDPC.expand_protograph(args[1], args[0])

    """
    Assuming:
    - nonparallel connections
    - coordinate weight no greater than 1 at any location
    """
    @staticmethod
    def expand_protograph(t, protograph):
        reverse_mapping = TannerGraph.transpose(protograph.tanner_graph, protograph.width)
        expanded_graph = {}
        for check in range(protograph.height * t):
            expanded_graph[check] = []
        for var_node in range(protograph.width * t):
            location_in_protograph = int(var_node / t)
            keys_in_protograph = reverse_mapping[location_in_protograph]
            for key in keys_in_protograph:
                expanded_graph[(key * t) + (var_node % t)].append(var_node)
        return expanded_graph


