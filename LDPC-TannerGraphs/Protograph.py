import Utils
from TannerGraph import TannerGraph


class Protograph(TannerGraph):
    """
    This TannerGraph subclass constructs the tanner_graph dictionary as a dictionary of lists of ProtographEntry objects.
    This allows each entry to have an entry value not necessarily equal to 1.
    """

    # parameters:
    #   args: list(list()), a list of entries where each entry is a list of length three. These entry lists contain
    #   their row value at position 0, column value at position 1, and value at position 2
    # return:
    #   a fully constructed Protograph object
    def __init__(self, args):
        TannerGraph.__init__(self, args)

        self.tanner_graph = Protograph.create_protograph(args)

        self.height = len(self.tanner_graph)
        self.width = self.get_width()

    # return:
    #   the width of a protograph tanner_graph (the superclass get_width does not work here as entry values should no longer by inferred)
    def get_width(self):
        max = 0
        for row in self.tanner_graph:
            for entry in self.getRow(row):
                if entry.index > max:
                    max = entry.index
        return max + 1

    '''
    Constructs a protograph object from the supplied point list
    '''

    # parameters:
    #   points: list, the list of points defining the protograph
    # return:
    #   the tanner_graph which represents the Protograph object
    @staticmethod
    def create_protograph(points):

        protograph = TannerGraph(None)

        num_rows = 0
        for entry in points:
            if entry[0] + 1 > num_rows:
                num_rows = entry[0] + 1

        for row in range(num_rows):
            protograph.addRow()

        for entry in points:
            protograph.getRow(entry[0]).append(ProtographEntry(entry[1], entry[2]))

        return protograph.tanner_graph

    # parameters:
    #   r: int, row index of fetched entry
    #   c: int, col index of fetched entry
    # return:
    #   the value of the entry at location [r, c] in self.tanner_graph
    def get(self, r, c):
        row = self.getRow(r)
        for entry in row:
            if entry.index == c:
                return entry.value
        return 0


'''
This class represents a protograph entry; it allows for entry values to be greater than 1 
'''


class ProtographEntry:

    def __init__(self, index, value):
        self.value = value
        self.index = index
