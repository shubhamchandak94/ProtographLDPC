import Utils
from TannerGraph import TannerGraph


class Protograph(TannerGraph):

    # this graph contains a list of entries, not positions. entries have both value and position attributes
    # args : list 1 locations in matrix
    def __init__(self, args):
        TannerGraph.__init__(self, args)

        self.tanner_graph = Protograph.create_protograph(args)

        self.height = len(self.tanner_graph)
        self.width = self.get_width()

    # @staticmethod
    # def create_protograph(points):
    #     tanner_graph = {}
    #     for point in points:
    #         if point[0] not in tanner_graph:
    #             tanner_graph[point[0]] = []
    #         if point[1] not in tanner_graph[point[0]]:
    #             tanner_graph[point[0]].append(point[1])
    #     return tanner_graph

    def get_width(self):
        max = 0
        for row in self.tanner_graph:
            for entry in self.getRow(row):
                if entry.index > max:
                    max = entry.index
        return max + 1

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

    def get(self, r, c):
        row = self.getRow(r)
        for entry in row:
            if entry.index == c:
                return entry.value
        return 0

class ProtographEntry:

    def __init__(self, index, value):
        self.value = value
        self.index = index
