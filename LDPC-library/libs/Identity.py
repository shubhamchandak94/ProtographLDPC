import itertools
from libs.TannerGraph import TannerGraph

'''
A class for the handling of Identity type matrices in TannerGraph form. It is important to note the distinction between
identity matrices and identity type matrices. Identity type matrices are regular matrices whose length and width are the
same and who's columns and rows share a weightage of exactly 1. Identity type matrix entries are restricted in
value (all must carry a value of 1), but are not as heavily restricted in position as they would be in an Identity Matrix.
'''

class Identity(TannerGraph):

    # parameters:
    #   args: list, the necessary arguments necessary to construct an identity matrix
    def __init__(self, args):

        TannerGraph.__init__(self, args)

        # args describes length of identity matrix
        if len(args) == 1:
            for i in range(int(args[0])):
                self.tanner_graph[i] = [i]

            self.height = int(args[0])
            self.width = self.height

        # returns a graph who's matrix contains an entry in the location arg[i] of column i for all columns.
        elif len(args) > 1:

            max_row = max(args)
            for i in range(max_row):
                self.tanner_graph[i] = []

            for i in range(len(args)):
                self.tanner_graph[i] = [args[i]]

            self.height = max_row + 1
            self.width = self.height

    # parameters:
    #   width: the width of every matrix contained in this set
    # return:
    #   list, a list containing all possible permutation matrices of width = width
    # NOTE: this function is not very useful in practice for large width since the
    # time and space complexity grows according to width! (factorial)
    @staticmethod
    def permutation_set(width):
        indices = list(range(width))
        return [Identity(permutation) for permutation in itertools.permutations(indices)]
