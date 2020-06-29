from TannerGraph import TannerGraph

class Protograph(TannerGraph):

    # args : list 1 locations in matrix
    def __init__(self, args):
        TannerGraph.__init__(self, args, ldpc="protograph")

