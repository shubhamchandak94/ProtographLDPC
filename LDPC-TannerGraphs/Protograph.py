
import Utils
from TannerGraph import TannerGraph

class Protograph(TannerGraph):

    # args : list 1 locations in matrix
    def __init__(self, args):
        TannerGraph.__init__(self, args)

        self.tanner_graph = TannerGraph.create_graph(args)

        self.height = len(self.tanner_graph)
        self.width = TannerGraph.get_width(self.tanner_graph)

