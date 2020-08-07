import os
from TannerGraph import *

'''
This TannerGraph subclass constructs the tanner_graph dictionary as a dictionary of lists of ProtographEntry objects.
This allows each entry to have an entry value not necessarily equal to 1.

Protographs can be read from predefined files in the following format:
code_width code height
transmitted_bits [list of transmitted indices]
dense/sparse
matrix

if the switch indicates a dense matrix, the matrix section represents the

Entries are considered non-zero positions in the Protograph's matrix representation
each entry is listed in the file as follows:
row in matrix, column in matrix, value in matrix
    integers are all single-space separated

If puncturing is to be used in the transmission of codewords, call the generate_protograph_dir() function
to create a directory, in place of the existing protograph template file, which contains the information needed
for decoding punctured messages. The protograph constructor readable template is moved into this directory.
'''


class Protograph(TannerGraph):

    # parameters:
    #   args:
    #     - list(string) where the contained string is the filepath of the predefined protograph
    # return:
    #   a fully constructed Protograph object
    def __init__(self, args):
        TannerGraph.__init__(self, args)

        parsed_file = read_sparse_array_from_file(args[0])
        array = parsed_file[0]

        self.height = parsed_file[1][0]
        self.width = parsed_file[1][1]

        self.transmitted_bits = parsed_file[2]

        self.tanner_graph = Protograph.create_tanner_graph_for_protograph(array)

        actual_height = len(self.tanner_graph)
        actual_width = self.get_width()

        if self.width != actual_width or self.height != actual_height:
            print("given height and/or width values inconsistent with provided protograph matrix")

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
    not in TannerGraph as Protographs are the only TannerGraphs who's values can be greater than 1.
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
    This method takes a protograph template (given in the format specified in the class docs) and generates a directory
    containing the template itself, as well as a .transmitted file containing the transmitted bits per codeword. To
    create protograph objects, the constructor for this class understands the template format: pass the filepath of the
    template, not the protograph directory
    '''

    # parameters:
    #   filepath: string, path of protograph template
    #   protograph_factor: int, factor by which the protograph is to be expanded by
    @staticmethod
    def generate_protograph_dir(filepath, protograph_factor):

        try:
            contents = open(filepath, 'r').read().split('\n')
        except Exception:
            print("could not find or process specified protograph file")
            return

        dirname = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        protograph_dir = os.path.join(dirname, filename)
        os.remove(filepath)
        os.mkdir(protograph_dir)

        protograph_bits_transmitted = [int(i) for i in contents[1].split(' ')[1:]]
        transmitted_bits = []

        for i in protograph_bits_transmitted:
            for j in range(i * protograph_factor, i * protograph_factor + protograph_factor):
                transmitted_bits.append(j)

        transmitted_bits = [str(i) for i in transmitted_bits]
        transmitted_bits = ' '.join(transmitted_bits)

        f = open(os.path.join(protograph_dir, filename), 'w')
        f.write('\n'.join(contents))

        f = open(os.path.join(protograph_dir, '.transmitted'), 'w')
        f.write('factor: ' + str(protograph_factor) + '\n' + 'total bits before transmission: ' + str(
            int(contents[0].split(' ')[1]) * protograph_factor) + '\n' + transmitted_bits)


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
def read_sparse_array_from_file(filepath):
    file_matrix = []

    f = open(filepath, 'r')
    entries = f.read().split('\n')  # either list of direct entries of list of rows in protograph

    switch = entries[2]
    dimensions = [int(i) for i in entries[0].split(' ')]
    transmitted_bits = [int(i) for i in entries[1].split(' ')[1:]]
    entries = entries[3:]

    for entry in entries:
        file_matrix.append([int(i) for i in entry.split(' ')])

    if switch == "sparse":
        output_matrix = file_matrix

    elif switch == "dense":

        protograph_array = []

        for r in range(len(file_matrix)):
            for c in range(len(file_matrix[r])):
                protograph_array.append([r, c, file_matrix[r][c]])

        output_matrix = protograph_array

    else:
        print("invalid protograph switch")
        return

    return output_matrix, dimensions, transmitted_bits


'''
This class represents a protograph entry; it allows for entry values to be greater than 1
'''


class ProtographEntry:

    def __init__(self, index, value):
        self.value = value
        self.index = index
