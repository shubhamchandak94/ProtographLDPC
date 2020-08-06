
import numpy as np

import Utils
from Identity import Identity
from RegularLDPC import RegularLDPC

from TannerGraph import *

'''
- A class for the handling of ProtogrpahLDPC matrices in Tanner Graph form

The tanner graph is stored as a dictionary, row indices (check nodes) are mapped to lists of column indices (variable
nodes) to indicate bipartite connections

args: input to enable construction. input follows the following construction pattern: args[0] = Protograph object
containing the Protograph to be lifted. args[1] depicts the factor by which to lift the given protograph.

The construction argument indicates the algorithm to be employed in the construction of protograph submatrices. These
submatrices are defined by the following scope: (rows: r => r + f, columns: c => c + f) for all (r, c) where r % f == 0
and c % f == 0. f is the supplied protograph lift factor.

The implemented constructions work as follows:

construction = permutation
This submatrix is a result of the sum of n permutation matrices of width f, where n is
defined by the position at row = r / f, column = c / f on the supplied protograph.

construction = regular
This submatrix is a regular LDPC matrix graph whose row and column weightage is defined by the protograph's value
at row = r / f, column = c / f.

construction = quasi-cyclic
Given a list of n randomly chosen indices, where n is defined by the value of the protogrpah at (r, c) and n is
bounded by the width of the submatrix, this list represents the entries for the first row of the code. For every
subsequent row in the submatrix, that row is defined by the circular right shift of the previous row.

'''

class ProtographLDPC(TannerGraph):

    # parameters:
    #   args: list, args[0] = protograph to be lifted, args[1] = lift factor
    # return:
    #   a fully lifted Protograph LDPC code
    def __init__(self, args, construction, width_provided=False):
        TannerGraph.__init__(self, args, construction=construction)

        self.construction = construction
        self.protograph = args[0]

        if width_provided:
            self.factor = args[1] / self.protograph.width
            if self.factor - int(self.factor) != 0:
                print("cannot generate provided protograph with provided code length")
                print("accepted code lengths: x for all x % " + str(self.protograph.width) + " = 0")
                return
            self.factor = int(args[1] / self.protograph.width)
        else:
            self.factor = args[1]

        self.maximum_allowable_protograph_node = self.factor

        self.width = self.protograph.width * self.factor
        self.height = self.protograph.height * self.factor

        self.permutation_set = None
        if construction == "permutation":
            # do not alter this set with external methods
            self.permutation_set = Identity.permutation_set(self.factor)

        self.tanner_graph = ProtographLDPC.expanded_protograph(self.protograph, self.factor, self.construction, permutation_set=self.permutation_set)

    '''
    This method provides a means by which a given protograph can be lifted by a given factor. This method cannot identify
    if a supplied permutation set does not fit the provided lift factor, so if unsure, do not supply this method with a
    permutation set. The option to provide your own set is for the purposes of not creating redundant objects.
    '''
    # parameters:
    #   protograph: Protograph, the protograph code which must be lifted
    #   factor: the factor by which to lift the protograph
    #   permutation_set: the set containing all possible permutation matrices of width = factor
    #       in TannerGraph classof Identity form
    # return:
    #   ProtographLDPC, fully expanded
    @staticmethod
    def expanded_protograph(protograph, factor, construction, permutation_set=None):

        if permutation_set is None and construction == "permutation":
            permutation_set = Identity.permutation_set(factor)

        expanded = TannerGraph(None)
        for i in range(protograph.height * factor):
            expanded.addRow()

        for r in range(0, len(expanded), factor):
            for c in range(0, protograph.width * factor, factor):

                if protograph.get(r / factor, c / factor) > factor:
                    print("invalid protograph value for given lift factor")
                    return None

                elif protograph.get(r / factor, c / factor) == 0:
                    continue

                else:

                    expanded.insert(ProtographLDPC.submatrix(
                        submatrix_construction=construction,
                        factor=factor,
                        permutation_set=permutation_set,
                        num_matrices=protograph.get(r / factor, c / factor)
                    ), [r, c])

        return expanded.tanner_graph

    # parameters:
    #   permutation_set: the set of all possible permutation matrices to use in the summation
    #   num_matrices: the number of matrices to sum up. This of course is bounded by the lifting factor of the protograph
    #       as all permutation matrices are of dimension width = factor, height = factor
    #   factor: the lifting factor by which the associated protograph is to be lifted by
    #   submatrix_construction: the algorithm through which the submatrix is constructed
    # returns:
    #   submatrix: TannerGraph, graph to be inserted into the eventual code
    @staticmethod
    def submatrix(submatrix_construction="regular", factor=None, permutation_set=None, num_matrices=None):

        if submatrix_construction == "permutation":
            available_indices = np.random.choice(len(permutation_set), len(permutation_set), replace=False)

            start = permutation_set[available_indices[0]]
            taken = [available_indices[0]]

            if num_matrices == 1:
                return start

            for i in range(num_matrices - 1):

                for j in range(len(available_indices) - 1):
                    if not start.overlaps(permutation_set[available_indices[j + 1]]) and available_indices[j + 1] not in taken:
                        start = start.absorb_nonoverlapping(permutation_set[available_indices[j + 1]], [0, 0])
                        taken.append(available_indices[j + 1])
                        break

            return start

        elif submatrix_construction == "regular":
            return RegularLDPC([factor, factor, num_matrices], "populate-rows")

        elif submatrix_construction == "quasi-cyclic":

            qc_graph = make_graph(factor, factor, factor)

            indices = list(np.random.choice(factor, num_matrices, replace=False))
            qc_graph = construct_stepwise_submatrix(indices, qc_graph)

            return qc_graph

        elif submatrix_construction == "permuted-quasi-cyclic":

            graph = make_graph(factor, factor, factor)

            indices = list(range(0, num_matrices))
            graph = construct_stepwise_submatrix(indices, graph)

            graph.permute_rows()
            graph.permute_columns()

            return graph


'''
Constructs a submatrix graph from a series of right shifts of an originating index list. This method provides the
base implementation for the quasi-cyclic and permuted-quasi-cyclic constructions.
'''
# parameters:
#   start_indices: list(int), the indices on which the right shift cycle is to initiate upon
#   graph: TannerGraph, the graph to build the cycles on
# return:
#   TannerGraph, graph: the graph argument is returned after construction
def construct_stepwise_submatrix(start_indices, graph):

    for i in range(graph.width):
        new = start_indices.copy()
        graph.put(i, new)

        right_shift_row(new, graph.width)
        start_indices = new

    return graph
