
import Utils
from TannerGraph import TannerGraph

class ProtographLDPC(TannerGraph):

    # args: protograph, growth factor
    def __init__(self, args):
        TannerGraph.__init__(self, args)

        self.width = args[0].width * args[1]
        self.height = args[0].height * args[1]

        self.tanner_graph = ProtographLDPC.expanded_protograph(args[1], args[0])

    @staticmethod
    def expanded_protograph(protograph, factor):
        None

    # """
    # Assuming:
    # - nonparallel connections
    # - coordinate weight no greater than 1 at any location
    # """
    # @staticmethod
    # def expanded_protograph(t, protograph):
    #
    #     # initiate expanded map
    #     expanded_graph = {}
    #
    #     # populate map
    #     reverse_mapping = TannerGraph.transpose(protograph.tanner_graph, protograph.width)
    #     for check in range(protograph.height * t):
    #         expanded_graph[check] = []
    #     for var_node in range(protograph.width * t):
    #         location_in_protograph = int(var_node / t)
    #         keys_in_protograph = reverse_mapping[location_in_protograph]
    #         for key in keys_in_protograph:
    #             expanded_graph[(key * t) + (var_node % t)].append(var_node)
    #
    #     # shuffle appropriate sections within map
    #
    #
    #     return expanded_graph
    #
    # # because this method shuffles like groups within extended graphs, each row in rows has the same length
    # @staticmethod
    # def permute(rows):
    #     cols = []
    #     for i in range(len(rows[0])):
    #         col = []
    #         for row in rows:
    #             col.append(row[i])
    #         cols.append(col)
    #
    #     for i in range(len(cols)):
    #         cols[i] = Utils.random_list(cols[i], len(cols[i]))
    #
    #     transposed = []
    #     for i in range(len(cols[0])):
    #         row = []
    #         for col in cols:
    #             row.append(col[i])
    #         transposed.append(row)




