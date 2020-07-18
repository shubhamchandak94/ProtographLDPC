
import Utils
from Identity import Identity
from TannerGraph import TannerGraph

class ProtographLDPC(TannerGraph):

    # args: protograph, growth factor
    def __init__(self, args):
        TannerGraph.__init__(self, args)

        self.protograph = args[0]
        self.factor = args[1]
        self.maximum_allowable_protograph_node = self.factor

        self.width = args[0].width * args[1]
        self.height = args[0].height * args[1]

        # do not alter this set with external methods
        self.permutation_set = Identity.permutation_set(self.factor)
        # self.permutation_set = Utils.random_list(self.permutation_set, len(self.permutation_set))

        self.tanner_graph = ProtographLDPC.expanded_protograph(self.protograph, self.permutation_set, self.factor)

    @staticmethod
    def expanded_protograph(protograph, permutation_set, factor):

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
                    expanded.insert(ProtographLDPC.submatrix(permutation_set, protograph.get(r / factor, c / factor)), [r, c])

        return expanded.tanner_graph


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




