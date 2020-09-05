"""

A parent of all LDPC codes included in this library

This class provides a structure which all LDPC codes can manipulate in their individual constructions.
The tanner_graph attribute presents a dictionary where row indices are mapped to lists of column indices.
This structure is populated in the respective subclasses. It is a requirement of all subclasses to define
the width, height, and tanner_graph attributes of this superclass, as intermediary functions rely on these
fields to function appropriately

The Tanner (Bipartite) graph representation describes the same code as the corresponding parity check matrix.
Each row contained within the structural dictionary describes a row in the corresponding matrix: the key value
indicates the index of the row in the matrix, and the value list describes the locations of the entries
contained in that matrix row. Unlisted values are assumed to be empty and therefore zero in the matrix representation

"""

import random


class TannerGraph:

    # All subclasses must implement height, width, tanner_graph definitions
    # parameters:
    #   args: list, contains any possible arguments a subclass might require for their respective constructions
    #   construction: if a subclass implements multiple constructions, this field identifies the construction used by a subclass instance
    # return:
    #   a TannerGraph object with the tanner_graph dictionary instantiated empty
    def __init__(self, args, construction=None):

        self.args = args
        self.construction = construction

        self.width = None
        self.height = None

        self.tanner_graph = {}

    # parameters:
    #   row: int, the row r contained as a key by self.tanner_graph
    #   value: int, the value which self.tanner_graph.get(row) must append to itself
    # return:
    #   None, appends value internally
    def append(self, row, value):
        self.tanner_graph[row].append(value)

    # parameters:
    #   row: int, row index to query
    # return:
    #   list, the calue associated with the row parameter in self.tanner_graph
    def getRow(self, row):
        return self.tanner_graph[row]

    # Adds another row below the existing rows in self.tanner_graph. This corresponds to increasing the number
    # of parity bits and reducing the number of message bits. In this sense, an n/k code is transformed into
    # an n/k-1 code. This row is irrelevant until population, as it is initially empty (corresponding to a row
    # 0s in the matrix representation
    # return:
    #   None
    def addRow(self):
        self.tanner_graph[len(self.tanner_graph)] = []

    # return:
    #   a list of row indices contained in the Graph
    def keys(self):
        return list(self.tanner_graph.keys())

    # WARNING: This function performs insertion without warning if data is being overriden
    # parameters:
    #   row_index: int, the index of the row to be appended (location along the height of the matrix)
    #   row: list, the actual row to insert
    def put(self, row_index, row):
        self.tanner_graph[row_index] = row

    # return:
    #   the number of rows (either populated or not) described by this Tanner Graph
    def __len__(self):
        return len(self.tanner_graph)

    # If Two graphs overlap, it is indicated that both graphs contain one or more entries in the same location.
    # parameters:
    #   other: TannerGraph, the comparative graph
    # return:
    #   boolean value: indicating if self and other overlap
    def overlaps(self, other):

        if len(self.tanner_graph.keys()) <= len(other.keys()):
            smaller = self
            larger = other
        else:
            smaller = other
            larger = self

        for i in range(len(smaller)):
            for entry in smaller.getRow(i):
                if entry in larger.getRow(i):
                    return True

        return False

    # Performs an insertion of one smaller TannerGraph into another. This is described more easily in terms of code matrices.
    # Matrix code m can be inserted into matrix code n at location (i, j) if i + m.width < n.width and j + m.height < n.height.
    # Code M would replace all entries and non entries in the scope of rows j -> j + m.height and columns i -> m.width with its
    # own relative entries and non entries
    # parameters:
    #   other: TannerGraph, the graph which self must absorb
    #   location: list, the [row, col] values at which the insertion is to occur
    # return:
    #   None, all changes are made in self internally
    def insert(self, other, location):  # location: [row, column]

        # clears graph
        for r in range(other.height):
            c = 0
            while c < len(self.tanner_graph[r + location[0]]):
                if location[1] <= self.tanner_graph[r + location[0]][c] < location[1] + other.width:
                    self.tanner_graph[r + location[0]].pop(c)
                    c -= 1

                c += 1

        # populates graph
        for r in range(other.height):
            for c in other.tanner_graph[r]:
                if location[1] + c not in self.tanner_graph[location[0] + r]:
                    self.tanner_graph[location[0] + r].append(location[1] + c)

        # no errors thrown for out of bounds

    # Equivalent to the process of summing two code matrices. The summation is performed given the two matrices do not
    # overlap. If one matrix is smaller than the other, the larger matrix will contain all the changes and is returned.
    # The summation in this case will occur in the scope of rows: i -> i + smaller.height, columns: j -> j + smaller.width
    # given location: [i, j]
    # parameters:
    #   other: TannerGraph, the second tanner graph involved in the summation
    #   location: list [r, c], the coordinates where the summation is to start in the larger graph
    def absorb_nonoverlapping(self, other, location):

        if self.overlaps(other):
            print("cannot combine matrices, they overlap")
            return None

        if len(self.tanner_graph.keys()) <= len(other.keys()):
            smaller = self
            larger = other
        else:
            smaller = other
            larger = self

        for r in range(smaller.height):
            for c in smaller.getRow(r):
                larger.getRow(r + location[0]).append(c + location[1])

        return larger

    def permute_rows(self, permutation_list=None):

        if permutation_list is None:
            permutation_list = random.sample(range(self.height), self.height)
        else:
            if len(permutation_list) != self.height:
                print("cannot perform graph row permutation: invalid permutation list")
                return

        for i in range(len(permutation_list)):
            self.swap_rows(i, permutation_list[i])

        return None

    # swaps two rows given row indices
    def swap_rows(self, i, j):
        temp = self.tanner_graph[i]
        self.tanner_graph[i] = self.tanner_graph[j].copy()
        self.tanner_graph[j] = temp

    # randomly shuffles the columns of the code
    def permute_columns(self, permutation_list=None):

        if permutation_list is None:
            permutation_list = random.sample(range(self.width), self.width)
        else:
            if len(permutation_list) != self.width:
                raise RuntimeError("cannot perform graph row permutation: invalid permutation list")

        # we first transpose the graph and then permute the rows and then transpose again
        self.tanner_graph = transpose(self.tanner_graph, self.width)
        self.height, self.width = self.width, self.height
        self.permute_rows(permutation_list)

        self.tanner_graph = transpose(self.tanner_graph, self.width)
        self.height, self.width = self.width, self.height

    # swaps two columns given column indices
    def swap_columns(self, i, j):
        for row in self.tanner_graph:
            for e in range(len(self.getRow(row))):
                if self.getRow(row)[e] == i:
                    self.tanner_graph[row][e] = j
                elif self.getRow(row)[e] == j:
                    self.tanner_graph[row][e] = i

    # return:
    #   returns the matrix representation of this TannerGraph instance
    def as_matrix(self):
        return get_matrix_representation(self.tanner_graph)


# parameters:
#   row: int, number of rows to initializes in this Tanner Graph
#   width: int, width of Graph
#   height: int, height of Graph
# return:
#   Empty Tanner Graph instantiation with width, height attributes defined
def make_graph(rows, width, height):
    graph = TannerGraph(None)

    graph.width = width
    graph.height = height

    for i in range(rows):
        graph.addRow()

    return graph


'''
Traverses the dictionary to find identical key values. These correspond to repeated parity check equations which
could undermine the code's performance.
'''


# parameters:
#   tanner_graph: TannerGraph.tanner_graph dictionary
# returns:
#   boolean indicating whether or not the dict contains repeated list values
def has_repeated_rows(tanner_graph):
    for i in range(0, len(tanner_graph) - 1):
        for j in range(i + 1, len(tanner_graph)):
            if tanner_graph[i] == tanner_graph[j]:
                print("row " + str(i) + " and row " + str(j) + " are identical")
                return True
    return False


'''
The equivalent of transposing a matrix, if that matrix were represented by a bipartite graph. This allows for more
diverse methods of matrix construction.
'''


# parameters:
#   tanner_graph: Tanner.tanner_graph dictionary, the graph to be transposed
# returns:
#   TannerGraph.tanner_graph attribute representing the transposed dictionary
def transpose(tanner_graph, new_height):
    new_graph = {i: [] for i in range(new_height)}
    for row in tanner_graph:
        for col in tanner_graph[row]:
            new_graph[col].append(row)
    return new_graph


'''
Because this program stores ldpc parity information in the form of tanner graphs, this provides a way to construct
the appropriate matrix provided the tanner graph
'''


# parameters:
#   tanner_graph: Tanner.tanner_graph dictionary, the dict object for which a representation must be made
# returns:
#   matrix, list(list()) where 1s represent entries and 0s represent lack of thereof
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
    normalize(matrix)
    return matrix


'''
Because only rows are directly indexed in the first level of the tanner_graph, the width of a tanner_graph dict
is not inherently directly stored anywhere. The dictionary's lists must be traversed to find the maximum index.
The max + 1 indicates the width of the tanner_graph
'''


# parameters:
#   tanner_graph: Tanner.tanner_graph dictionary of which the width must be found
# return:
#   int, width of the tanner_graph
def get_width(tanner_graph):
    max = 0
    for row in tanner_graph:
        for index in tanner_graph[row]:
            if index > max:
                max = index
    return max + 1


'''
Performs a circular right shift of all elements in a given list
'''


# parameters:
#   row: list, a list to be right shifted. This list is commonly a row of a TannerGraph in library implementations
#   width: int, the cap to the right-shift. If the width is surpassed by any element, that element is reset to 0
def right_shift_row(row, width):
    for i in range(len(row)):
        if row[i] == width - 1:
            row[i] = 0
        else:
            row[i] += 1


'''
Given a list of lists, this method normalizes all sublists to the same size by populating smaller sublists with 0s.
This method is intended to normalize matrix representations for aesthetic purposes
'''


# parameters:
#   arr: list(list()), array to be normalized
# return:
#   list(list()) normalized 2d list
def normalize(arr):
    new_length = largest_row(arr)
    for i in range(len(arr)):
        arr[i] = arr[i] + [0] * (new_length - len(arr[i]))


'''
Iteratively finds the length of the longest sublist contained in a list of lists.
'''


# parameters:
#   arr: list, list to be queried
# return:
#   int, length of larges sublist in an array
def largest_row(arr):
    largest = 0
    for row in arr:
        if len(row) > largest:
            largest = len(row)
    return largest


'''
analyzes a given code with a few print statements
'''


# parameters:
#   TannerGraph, graph to be analyzed
#   printCode, whether to display the entire code (suitable only for small matrices)
def analyze(code, printCode=False):
    print()
    print("arguments: " + str(code.args))
    print("code construction: " + code.construction)

    matrix = code.as_matrix()

    if printCode:
        print("code as graph")
        print(code.tanner_graph)

        print("code as matrix: ")
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


'''
Displays a TannerGraph object in matrix form
'''


# parameters:
#   graph: TannerGraph
def printm(graph):
    m = graph.as_matrix()
    for line in m:
        print(line)
