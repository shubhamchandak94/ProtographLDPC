
import Utils
from Identity import Identity
from RegularLDPC import RegularLDPC
from TannerGraph import TannerGraph

'''
- A class for the handling of ProtogrpahLDPC matrices in Tanner Graph form

The tanner graph is stored as a dictionary, row indices (check nodes) are mapped to lists of column indices (variable 
nodes) to indicate bipartite connections

args: input to enable construction. input follows the following construction patern: args[0] = Protograph object 
containing the Protograph to be lifted. args[1] depicts the factor by which to lift the given protograph.

The implemented constructions work as follows:

construction = permutation
given a protograph p and lift factor f, a blank matrix is constructed of the dimension width = p.width * f and 
height = p.height * f. For each position (r, c) where r and c are both divisible by f, the scope [r => r + f, c => c + f]
is populated with a submatrix. This submatrix is a result of the sum of n permutation matrices of width f, where n is
defined by the position at row = r / f, column = c / f on the supplied protograph.

construction = regular
given a protograph p and lift factor f, a blank matrix is constructed of the dimension width = p.width * f and 
height = p.height * f. For each position (r, c) where r and c are both divisible by f, the scope [r => r + f, c => c + f]
is populated with a regular LDPC matrix graph, who's row and column weightage is defined by the protograph's value
at row = r / f, column = c / f/
'''

class ProtographLDPC(TannerGraph):

    # parameters:
    #   args: list, args[0] = protograph to be lifted, args[1] = lift factor
    # return:
    #   a fully lifted Protograph LDPC code
    def __init__(self, args, construction):
        TannerGraph.__init__(self, args, construction=construction)

        self.construction = construction
        self.protograph = args[0]
        self.factor = args[1]
        self.maximum_allowable_protograph_node = self.factor

        self.width = args[0].width * args[1]
        self.height = args[0].height * args[1]

        self.permutation_set = None

        if construction == "permutation":
            # do not alter this set with external methods
            self.permutation_set = Identity.permutation_set(self.factor)
            # self.permutation_set = Utils.random_list(self.permutation_set, len(self.permutation_set))

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

                    if construction == "permutation":
                        expanded.insert(ProtographLDPC.submatrix(permutation_set, protograph.get(r / factor, c / factor)), [r, c])
                    elif construction == "regular":
                        expanded.insert(RegularLDPC([factor, factor, protograph.get(r / factor, c / factor)], "populate-columns"), [r, c])

        return expanded.tanner_graph

    '''
    Returns a sum of permutation matrices in the TannerGraph form
    '''
    # parameters:
    #   permutation_set: the set of all possible permutation matrices to use in the summation
    #   num_matrices: the number of matrices to sum up. This of course is bounded by the lifting factor of the protograph
    #       as all permutation matrices are of dimension width = factor, height = factor
    @staticmethod
    def submatrix(permutation_set, num_matrices):

        available_indices = list(range(0, len(permutation_set)))
        available_indices = Utils.random_list(available_indices, len(available_indices))

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
