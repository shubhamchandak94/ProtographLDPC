class TannerGraph:

    def __init__(self, args, construction=None):

        self.args = args
        self.construction = construction

        self.width = None
        self.height = None

        self.tanner_graph = {}


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

    # returns matrix representation of this graph
    def as_matrix(self):
        return TannerGraph.get_matrix_representation(self.tanner_graph)

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

    def overlaps(self, other):

        smaller = None
        larger = None
        if len(list(self.tanner_graph.keys())) <= len(list(other.keys())):
            smaller = self
            larger = other
        else:
            smaller = other
            larger = self

        for i in range(len(smaller)):
            for entry in smaller[i]:
                if entry in larger[i]:
                    return True

        return False


    @staticmethod
    def analyze(code):

        print()
        print("arguments: " + str(code.args))
        print("code construction: " + code.construction)

        print("code as graph")
        print(code.tanner_graph)

        print("code as matrix: ")
        matrix = code.as_matrix()
        for line in matrix:
            print(line)

        row_weights = []
        for line in matrix:
            row_weights.append(line.count(1))

        col_weights = []
        for c in range(len(matrix[0])):

            col_weight = 0
            for r in range(len(matrix)):
                if matrix[r][c] == 1:
                    col_weight += 1

            col_weights.append(col_weight)

        row_weights = list(dict.fromkeys(row_weights))
        col_weights = list(dict.fromkeys(col_weights))

        print("row weights: " + str(row_weights))
        print("col weights: " + str(col_weights))

        print("width: " + str(code.width))
        print("height: " + str(code.height))
        print()
