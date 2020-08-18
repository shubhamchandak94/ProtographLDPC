from libs.TannerGraph import *

'''
This subclass constructs the tanner_graph dictionary as a dictionary of lists of ProtographEntry objects.
This allows each entry to have an entry value not necessarily equal to 1.

Protographs can be read from predefined files in the following format:
n_checks (height) n_bits (width) # protograph dimensions
transmitted_bits [list of transmitted indices (1-indexed)] # optional, only needed when puncturing
dense/sparse # mode
matrix

if the switch indicates a dense matrix, the matrix section consists of n_checks lines each containing n_bits 
space-separated values representing the edge weight for that connection. This representation directly represents
the protograph in matrix form.

For the sparse mode, entries are non-zero positions in the Protograph's matrix representation
each entry is listed in the file as follows:
row in matrix, column in matrix, value in matrix
    integers are all single-space separated, positions are 1-indexed
'''


class Protograph(TannerGraph):

    # parameters:
    #   args:
    #     - protograph_file: filepath of the predefined protograph
    # return:
    #   a fully constructed Protograph object
    def __init__(self, protograph_file):
        TannerGraph.__init__(self, [protograph_file])

        parsed_file = read_protograph_array_from_file(protograph_file)

        array = parsed_file[0]

        self.height = parsed_file[1][0]
        self.width = parsed_file[1][1]

        self.transmitted_bits = parsed_file[2]  # this is None for no puncturing

        self.tanner_graph = Protograph.create_tanner_graph_for_protograph(array)

        actual_height = len(self.tanner_graph)
        actual_width = self.get_width()

        if self.width != actual_width or self.height != actual_height:
            raise RuntimeError("given height and/or width values inconsistent with provided protograph matrix")

    # return:
    #   the width of a protograph tanner_graph (the superclass get_width does not work here as entry values should no longer by inferred)
    def get_width(self):
        max = -1
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
    def create_tanner_graph_for_protograph(graph):

        protograph = TannerGraph(None)

        num_rows = 0
        for entry in graph:
            if entry[0] + 1 > num_rows:
                num_rows = entry[0] + 1

        for row in range(num_rows):
            protograph.addRow()

        for entry in graph:
            protograph.getRow(entry[0]).append(ProtographEntry(entry[1], entry[2]))

        return protograph.tanner_graph

    '''
    This method allows the protograph to be queried as if was defined by a matrix structure. This is necessary here and
    not in TannerGraph as Protographs are the only TannerGraphs whose values can be greater than 1.
    '''

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

    # parameters:
    #   row: int, row of the protograph to analyze
    # return:
    #   max_index: int, maximum index value of all ProtographEntries contained in the row
    def get_max_index(self, row):
        row = self.tanner_graph[row]
        max_index = 0
        for i in range(len(row)):
            if row[i].index > max_index:
                max_index = row[i].index
        return max_index

    # parameters:
    #   index: int, index to be queried
    #   row: int, index in graph of row to be queried
    # return:
    #   boolean: does index exist in row
    def contains_index(self, index, row):
        pulled = self.tanner_graph[row]
        for e in pulled:
            if e.index == index:
                return True
        return False

    def as_matrix(self):
        return get_matrix_representation(self)


'''
Because the superclass as_matrix method cannot work with ProtographEntry objects, Protograph.py must redefine
the construction of its matrix form.
'''


# parameters:
#   protograph: Protograph, the protograph to generate a matrix of
# return:
#   list(list()) representing the protograph code's matrix form
def get_matrix_representation(protograph):
    matrix = []
    for i in range(protograph.height):
        row = []
        if i in protograph.tanner_graph:
            for j in range(protograph.get_max_index(i) + 1):
                if protograph.contains_index(j, i):
                    row.append(protograph.get(i, j))
                else:
                    row.append(0)
        matrix.append(row)
    normalize(matrix)
    return matrix


def write_protograph_to_file(protograph, filepath):
    return None


# parameters:
#   filepath: String, filepath which contains predefined protograph
# return: tuple
#   output_matrix: list, when fed into the protograph constructor a Protograph object is created
#   dimensions: tuple, 2 elements (height, width) describing dimension of protograph
#   transmitted_bits: list, describing indices of transmitted bits in protograph
def read_protograph_array_from_file(filepath):
    f = open(filepath, 'r')
    lines = [line.rstrip('\n') for line in f.readlines()]
    dimensions = [int(i) for i in lines[0].split(' ')]
    if lines[1].split(' ')[0] == "transmitted_bits":
        # subtract 1 for 1-indexed to 0-indexed
        transmitted_bits = [int(i) - 1 for i in lines[1].split(' ')[1:]]
        switch = lines[2]
        matrix_entries = lines[3:]
    else:
        transmitted_bits = None
        switch = lines[1]
        matrix_entries = lines[2:]

    if switch == "sparse":
        output_matrix = []
        for entry in matrix_entries:
            r, c, value = [int(i) for i in entry.split(' ')]
            # 1 indexed to 0 indexed
            r -= 1
            c -= 1
            output_matrix.append([r, c, value])

    elif switch == "dense":
        protograph_array = []
        file_matrix = []
        for entry in matrix_entries:
            file_matrix.append([int(i) for i in entry.split(' ')])
        for r in range(len(file_matrix)):
            for c in range(len(file_matrix[r])):
                protograph_array.append([r, c, file_matrix[r][c]])
        output_matrix = protograph_array
    else:
        raise RuntimeError("invalid protograph format option specified")

    return output_matrix, dimensions, transmitted_bits


'''
This class represents a protograph entry; it allows for entry values to be greater than 1
'''


class ProtographEntry:

    def __init__(self, index, value):
        self.value = value
        self.index = index
