from Protograph import Protograph


class TannerGraph:

    def __init__(self, args, construction=None, ldpc=None):

        self.args = args
        self.construction = construction

        # args: constraints for regular ldpc matrix
        if ldpc == "regularLDPC":

            self.width = None
            self.height = None

            self.tanner_graph = {}

        # args: list of protograph points
        # this is just a protograph, not a protographLDPC
        elif ldpc == "protograph":

            self.tanner_graph = TannerGraph.create_graph(args)

            self.height = len(self.tanner_graph)
            self.width = TannerGraph.get_width(self.tanner_graph)

        elif ldpc == "protographLDPC":

            self.tanner_graph = {}

            self.width = args[0].width * args[1]
            self.height = args[0].height * args[1]


    @staticmethod
    def create_graph(points):
        tanner_graph = {}
        for point in points:
            if point[0] not in tanner_graph:
                tanner_graph[point[0]] = []
            if point[1] not in tanner_graph[point[0]]:
                tanner_graph[point[0]].append(point[1])
        return tanner_graph

    '''
    traverses the dictionary to find identical key values. These correspond to repeated parity check equations which
    could undermine the code's performance.
    '''

    @staticmethod
    def has_repeated_rows(tanner_graph):
        for i in range(0, len(tanner_graph) - 1):
            for j in range(i + 1, len(tanner_graph)):
                if tanner_graph[i] == tanner_graph[j]:
                    print("row " + str(i) + " and row " + str(j) + " are identical")
                    return True
        return False

    '''
    the equivalent of transposing a matrix, if that matrix were represented by a bipartite graph. This allows for more
    diverse methods of matrix construction.
    '''

    @staticmethod
    def transpose(tanner_graph, new_height):
        new_graph = {}
        for i in range(new_height):
            new_graph[i] = []
            for j in tanner_graph:
                if tanner_graph.get(j).count(i) == 1:
                    new_graph.get(i).append(j)
        return new_graph

    '''
    because this program stores ldpc parity information in the form of tanner graphs, this provides a way to construct
    the appropriate matrix provided the tanner graph
    '''

    @staticmethod
    def get_matrix_representation(tanner_graph):
        matrix = []
        for i in range(len(tanner_graph)):
            row = []
            if i in tanner_graph:
                for j in range(max(tanner_graph[i]) + 1):
                    if j in tanner_graph[i]:
                        row.append(1)
                    else:
                        row.append(0)
            matrix.append(row)
        TannerGraph.normalize(matrix)
        return matrix

    @staticmethod
    def get_width(tanner_graph):
        max = 0
        for row in tanner_graph:
            for index in tanner_graph[row]:
                if index > max:
                    max = index
        return max + 1

    @staticmethod
    def normalize(arr):
        new_length = TannerGraph.largest_row(arr)
        for i in range(len(arr)):
            arr[i] = arr[i] + [0] * (new_length - len(arr[i]))

    @staticmethod
    def largest_row(arr):
        largest = 0
        for row in arr:
            if len(row) > largest:
                largest = len(row)
        return largest
